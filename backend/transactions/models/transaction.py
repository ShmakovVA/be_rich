import logging

from django.db import models

from backend.transactions.enums import TransactionTypes

logger = logging.getLogger(__name__)


class TransactionManager(models.Manager):
    def wallet_income(self, wallet_id, exclude_internal=False):
        return self.filter(to_wallet=wallet_id)

    def wallet_outcome(self, wallet_id, exclude_internal=False):
        return self.filter(from_wallet=wallet_id)


class Transaction(models.Model):
    from_wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                    related_name='transaction_from')
    to_wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                  related_name='transaction_to')
    fee = models.ForeignKey('Transaction', null=True, blank=True,
                            on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, decimal_places=3, max_digits=16)
    message = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        default=TransactionTypes.INTERNAL,
        choices=TransactionTypes.choices()
    )

    objects = TransactionManager()

    # TODO: would be nice to roll it back
    def roll_back(self):
        pass

    def __str__(self):
        return f'{self.registered_at} : ' \
               f'{self.from_wallet} -> {self.to_wallet}' \
               f' - {self.get_status_display().name}'
