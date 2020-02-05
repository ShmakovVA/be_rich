from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Transaction, Wallet, Account


class WalletListInline(TabularInline):
    model = Wallet
    extra = 0
    fields = ('wallet_id', 'currency', 'amount', 'status')


class TransactionListInline(TabularInline):
    model = Transaction
    extra = 0
    max_num = 50
    fields = ('from_wallet', 'to_wallet', 'amount', 'message')
    fk_name = 'from_wallet'


class AccountAdmin(admin.ModelAdmin):
    fields = ('status', 'user', 'registered')
    readonly_fields = ('registered',)
    inlines = [WalletListInline, ]


class WalletAdmin(admin.ModelAdmin):
    fields = ('account', 'status', 'currency', 'amount', 'wallet_id')
    readonly_fields = ('wallet_id', 'currency',)
    inlines = [TransactionListInline, ]


class TransactionAdmin(admin.ModelAdmin):
    fields = ('from_wallet', 'to_wallet', 'fee', 'amount', 'message', 'type')
    readonly_fields = fields


admin.site.register(Account, AccountAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
