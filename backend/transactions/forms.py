from django import forms
from django.conf import settings


class DoTransactionForm(forms.Form):
    wallet_from = forms.CharField(max_length=50)
    wallet_to = forms.CharField(max_length=50)
    amount = forms.FloatField(min_value=1,
                              max_value=settings.MAX_TRANSACTION_AMOUNT)
    message = forms.CharField(max_length=50)
