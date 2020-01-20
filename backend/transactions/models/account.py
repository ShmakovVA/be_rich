import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.transactions.enums import (
    Currencies,
    AccountStatuses
)
from backend.transactions.exceptions import NotEnoughMoneyError
from backend.transactions.models.wallet import Wallet

logger = logging.getLogger(__name__)


class Account(models.Model):
    status = models.PositiveSmallIntegerField(
        default=AccountStatuses.ACTIVE, choices=AccountStatuses.choices()
    )
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    registered = models.DateTimeField(auto_now_add=True)

    def init_wallets(self):
        for currency in Currencies:
            Wallet(currency=currency, account=self).save()
        self.wallet_set.filter(currency=Currencies.USD).update(money=100.0)

    # TODO: might be nice to run it as a task via message broker
    #  (and make model cleaner)
    @transaction.atomic
    def init_transaction(self, wallet_id_from, wallet_id_to, amount, message):
        # TODO: There are should be currency conversion (ignored for now)
        #  or restricted transactions between wallets in different curencies
        try:
            sender_wallet = self.wallet_set.get(wallet_id=wallet_id_from)
        except Wallet.DoesNotExist:
            logger.log(f'Wallet {wallet_id_from} is not your wallet!')
            raise
        else:
            system_wallet = Wallet.objects.get(
                account__user__is_superuser=True,
                account__user__username='root',
                currency=sender_wallet.currency
            )
            try:
                reciever_wallet = Wallet.objects.get(wallet_id=wallet_id_to)
            except Wallet.DoesNotExist:
                logger.log(f'Wallet {wallet_id_to} or '
                           f'{wallet_id_from} doesn`t exist!')
                raise
            else:
                fee = None
                if self == reciever_wallet.account:  # no fee
                    fee_amount = 0.0
                else:
                    fee_amount = amount * settings.SYSTEM_FEE
                    if sender_wallet.money >= amount + fee_amount:
                        fee = Transaction(from_wallet=sender_wallet,
                                          to_wallet=system_wallet,
                                          message=f'fee for '
                                                  f'{sender_wallet.account}',
                                          amount=fee_amount)
                        fee.save()

                if sender_wallet.money >= amount + fee_amount:
                    Transaction(from_wallet=sender_wallet,
                                to_wallet=reciever_wallet,
                                fee=fee,
                                message=message,
                                amount=amount).save()
                else:
                    error_message = f'You have not enough money in ' \
                                    f'{wallet_id_from}.'
                    logger.error(error_message)
                    raise NotEnoughMoneyError(error_message)

            sender_wallet.money -= amount + fee_amount
            reciever_wallet.money += amount
            system_wallet.money += fee_amount
            Wallet.objects.bulk_update([sender_wallet,
                                        reciever_wallet,
                                        system_wallet], fields=['money'])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            super(Account, self).save(force_insert=False, force_update=False,
                                      using=None, update_fields=None)
            self.init_wallets()
        else:
            super(Account, self).save(force_insert=False, force_update=False,
                                      using=None, update_fields=None)

    def __str__(self):
        return f'{self.user} - {self.get_status_display().name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()
