from django.urls import path, include
from rest_framework import routers

from backend.transactions.views import (
    TransactionListSet,
    AccountListSet,
    WalletListSet
)

router = routers.SimpleRouter()
router.register(r'accounts', AccountListSet, 'accounts')
router.register(r'wallets', WalletListSet, 'wallets')
router.register(r'transactions', TransactionListSet, 'transactions')

urlpatterns = [
    path('', include(router.urls)),
]
