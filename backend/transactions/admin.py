from django.contrib import admin

from .models import Transaction, Wallet, Account


class AccountAdmin(admin.ModelAdmin):
    fields = ('status', 'user', 'registered')
    readonly_fields = ('registered',)


class WalletAdmin(admin.ModelAdmin):
    fields = ('account', 'status', 'currency', 'money', 'wallet_id')
    readonly_fields = ('wallet_id', 'currency',)


class TransactionAdmin(admin.ModelAdmin):
    fields = ('from_wallet', 'to_wallet', 'fee', 'amount', 'message', 'status')
    readonly_fields = fields


admin.site.register(Account, AccountAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
