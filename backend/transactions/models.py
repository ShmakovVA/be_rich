from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from .enums import Currencies, AccountStatuses, TransactionStatuses


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


class Wallet(models.Model):
    status = models.PositiveSmallIntegerField(
        default=AccountStatuses.ACTIVE, choices=AccountStatuses.choices()
    )
    account = models.ForeignKey('Account',
                                on_delete=models.CASCADE)
    currency = models.PositiveSmallIntegerField(
        default=Currencies.USD, choices=Currencies.choices()
    )
    money = models.FloatField(default=0.0)
    wallet_id = models.CharField(max_length=255, blank=True)

    def wallet_id_generate(self):
        account_email = self.account.user.email
        wallet_id = self.pk
        secret = settings.SECRET_KEY
        key = f'{account_email}{wallet_id}{secret}'.encode('utf-8')
        return sha1(key).hexdigest()

    @property
    def wallet_lookup(self):
        return f'***{self.wallet_id[20:]} ({self.get_currency_display().name})'

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

    class Meta:
        unique_together = ('account', 'currency')

    def __str__(self):
        return f'{self.account.user} ({self.money})' \
               f'{self.wallet_lookup} ' \
               f'- {self.get_status_display().name}'


class Transaction(models.Model):
    from_wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                    related_name='transaction_from')
    to_wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                  related_name='transaction_to')
    fee = models.ForeignKey('Transaction', null=True, blank=True,
                            on_delete=models.CASCADE)
    amount = models.FloatField()
    message = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        default=TransactionStatuses.PENDING,
        choices=TransactionStatuses.choices()
    )

    def __str__(self):
        return f'{self.registered_at} : ' \
               f'{self.from_wallet} -> {self.to_wallet}' \
               f' - {self.get_status_display().name}'
