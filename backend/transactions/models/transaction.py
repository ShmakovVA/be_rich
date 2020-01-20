import logging

from django.db import models

from backend.transactions.enums import TransactionStatuses

logger = logging.getLogger(__name__)


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
        default=TransactionStatuses.FINISHED,
        choices=TransactionStatuses.choices()
    )

    # TODO: would be nice to roll it back
    def roll_back(self):
        pass

    def __str__(self):
        return f'{self.registered_at} : ' \
               f'{self.from_wallet} -> {self.to_wallet}' \
               f' - {self.get_status_display().name}'
