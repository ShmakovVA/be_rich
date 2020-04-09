from django.contrib.auth.models import User
from rest_framework import serializers

from backend.transactions.enums import (
    Currencies,
    AccountStatuses,
    TransactionTypes
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
        fields = ('id', 'account', 'amount', 'currency_', 'status', 'wallet_id')

    account = AccountSerializer()
    status = serializers.SerializerMethodField()
    currency_ = serializers.SerializerMethodField()

    def get_status(self, obj):
        return AccountStatuses.name(obj.status)

    def get_currency_(self, obj):
        return Currencies.name(obj.currency)


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    from_wallet = WalletSerializer()
    to_wallet = WalletSerializer()
    fee_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'registered_at', 'type', 'from_wallet', 'to_wallet',
                  'amount', 'fee_amount', 'message')

    def get_type(self, obj):
        return TransactionTypes.name(obj.type)

    def get_fee_amount(self, obj):
        fee_value = TransactionSerializer(obj.fee).data.get('amount', None)
        return fee_value or '-'
