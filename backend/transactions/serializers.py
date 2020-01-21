from django.contrib.auth.models import User
from rest_framework import serializers

from backend.transactions.enums import (
    Currencies,
    AccountStatuses,
    TransactionStatuses
)
from backend.transactions.models import Transaction, Account, Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    user = UserSerializer()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return AccountStatuses.name(obj.status)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'account', 'money', 'currency_', 'status', 'wallet_id')

    account = AccountSerializer()
    status = serializers.SerializerMethodField()
    currency_ = serializers.SerializerMethodField()

    def get_status(self, obj):
        return AccountStatuses.name(obj.status)

    def get_currency_(self, obj):
        return Currencies.name(obj.currency)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    status = serializers.SerializerMethodField()
    from_wallet = WalletSerializer()
    to_wallet = WalletSerializer()

    def get_status(self, obj):
        return TransactionStatuses.name(obj.status)
