import logging
from hashlib import sha1

from django.conf import settings
from django.db import models

from backend.transactions.enums import Currencies, AccountStatuses

logger = logging.getLogger(__name__)


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

    # TODO: should be dropped in case allowing a few wallets in same currency
    class Meta:
        unique_together = ('account', 'currency')

    def __str__(self):
        return f'{self.account.user} ({self.money})' \
               f'{self.wallet_lookup} ' \
               f'- {self.get_status_display().name}'
