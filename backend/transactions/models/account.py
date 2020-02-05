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
from backend.transactions.enums import TransactionTypes
from backend.transactions.exceptions import (
    NotYourWalletError,
    MissingSystemWalletError,
    MissingReceiverWalletError
)
from backend.transactions.models.transaction import Transaction
from backend.transactions.models.wallet import Wallet

logger = logging.getLogger(__name__)


class AccountManager(models.Manager):
    def system_account(self):
        try:
            account = self.get(user__is_superuser=True)
        except Account.DoesNotExist:
            account = None
        except Account.MultipleObjectsReturned:
            account = self.filter(user__is_superuser=True).last()
        return account

    def system_wallet(self, currency):
        account = self.system_account()
        if account is not None:
            try:
                wallet = account.wallet_set.get(currency=currency)
            except Wallet.DoesNotExist:
                wallet = None
            return wallet

    def create(self, *args, **kwargs):
        instance = super(AccountManager, self).create(*args, **kwargs)
        instance._init_wallets()
        return instance


class Account(models.Model):
    status = models.PositiveSmallIntegerField(
        default=AccountStatuses.ACTIVE, choices=AccountStatuses.choices()
    )
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    registered = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    def _init_wallets(self):
        for currency in Currencies:
            Wallet.objects.create(currency=currency, account=self)
        usd_wallet = self.wallet_set.filter(currency=Currencies.USD).first()
        usd_wallet.amount = 100.0
        usd_wallet.save()

    # TODO: might be nice to run it as a task via message broker
    #  (and make model cleaner)
    @transaction.atomic
    def init_transaction(self, wallet_id_from, wallet_id_to, amount, message):
        # TODO: There are should be currency conversion (ignored for now)
        #  or restricted transactions between wallets in different curencies
        try:
            sender_wallet = Wallet.objects.get_wallet(wallet_id=wallet_id_from,
                                                      account_id=self.pk)
        except NotYourWalletError as e:
            logger.error(f'Wallet {wallet_id_from} is not your wallet!')
            raise e
        except Wallet.DoesNotExist as e:
            logger.error(f'Wallet {wallet_id_from} does not exist!')
            raise e

        system_wallet = Account.objects.system_wallet(
            currency=sender_wallet.currency)
        if system_wallet is None:
            logger.error(f'System (fee) wallet was not found!')
            raise MissingSystemWalletError(MissingSystemWalletError.message)

        receiver_wallet = Wallet.objects.get_wallet(wallet_id=wallet_id_to)
        if receiver_wallet is None:
            logger.error(f'Wallet {wallet_id_to} doesn`t exist!')
            raise MissingReceiverWalletError(MissingReceiverWalletError.message)

        is_internal_transaction = self == receiver_wallet.account
        fee_amount = amount * settings.SYSTEM_FEE
        amount_with_fee = fee_amount + amount
        total_amount = amount if is_internal_transaction else amount_with_fee
        transaction_type = TransactionTypes.INTERNAL \
            if is_internal_transaction else TransactionTypes.EXTERNAL

        Wallet.withdraw(id=sender_wallet.pk, amount=total_amount)
        Wallet.deposit(id=receiver_wallet.pk, amount=amount)

        fee = None
        if not is_internal_transaction:
            Wallet.deposit(id=system_wallet.pk, amount=fee_amount)
            fee = Transaction.objects.create(from_wallet=sender_wallet,
                                             to_wallet=system_wallet,
                                             message=f'fee for '
                                                     f'{sender_wallet.account}',
                                             amount=fee_amount,
                                             type=TransactionTypes.FEE)

        transaction = Transaction.objects.create(from_wallet=sender_wallet,
                                                 to_wallet=receiver_wallet,
                                                 fee=fee,
                                                 message=message,
                                                 amount=amount,
                                                 type=transaction_type)

        return transaction

    def __str__(self):
        return f'{self.user} - {self.get_status_display().name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()
