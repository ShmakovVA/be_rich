import logging
from hashlib import sha1

from django.conf import settings
from django.db import models, transaction

from backend.transactions.enums import Currencies, AccountStatuses
from backend.transactions.exceptions import (
    NotYourWalletError,
    NotEnoughMoneyError
)

logger = logging.getLogger(__name__)


class WalletManager(models.Manager):
    def get_wallet(self, wallet_id, account_id=None):
        wallet = self.get(wallet_id=wallet_id)
        if account_id is not None:
            if wallet.account.pk != account_id:
                raise NotYourWalletError(NotYourWalletError.message)
        return wallet


class Wallet(models.Model):
    status = models.PositiveSmallIntegerField(
        default=AccountStatuses.ACTIVE, choices=AccountStatuses.choices()
    )
    account = models.ForeignKey('Account',
                                on_delete=models.CASCADE)
    currency = models.PositiveSmallIntegerField(
        default=Currencies.USD, choices=Currencies.choices()
    )
    amount = models.DecimalField(default=0.0, decimal_places=3, max_digits=16)
    wallet_id = models.CharField(max_length=255, blank=True)

    objects = WalletManager()

    def wallet_id_generate(self):
        account_email = self.account.user.email
        wallet_id = self.pk
        secret = settings.SECRET_KEY
        key = f'{account_email}{wallet_id}{secret}'.encode('utf-8')
        return sha1(key).hexdigest()

    @property
    def wallet_lookup(self):
        return f'***{self.wallet_id[20:]} ({self.get_currency_display().name})'

    @classmethod
    def deposit(cls, id, amount):
        with transaction.atomic():
            wallet = (cls.objects.select_for_update(of=('self',)).get(id=id))
            wallet.amount += amount
            wallet.save()
        return wallet

    @classmethod
    def withdraw(cls, id, amount):
        with transaction.atomic():
            wallet = (cls.objects.select_for_update(of=('self',)).get(id=id))
            if wallet.amount < amount:
                raise NotEnoughMoneyError(NotEnoughMoneyError.message)
            wallet.amount -= amount
            wallet.save()
        return wallet

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            super(Wallet, self).save(force_insert=False, force_update=False,
                                     using=None, update_fields=None)
            Wallet.objects.filter(pk=self.pk).update(
                wallet_id=self.wallet_id_generate())
        else:
            super(Wallet, self).save(force_insert=False, force_update=False,
                                     using=None, update_fields=None)

    # TODO: should be dropped in case allowing a few wallets in same currency
    class Meta:
        unique_together = ('account', 'currency')

    def __str__(self):
        return f'{self.account.user} ({self.amount})' \
               f'{self.wallet_lookup} ' \
               f'- {self.get_status_display().name}'
