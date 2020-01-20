from django.urls import path, include
from rest_framework import routers

from .views import do_transaction
from .views import (
    TransactionListSet,
    AccountListSet,
    WalletListSet
)

router = routers.SimpleRouter()
router.register(r'accounts', AccountListSet, 'accounts')
router.register(r'wallets', WalletListSet, 'wallets')
router.register(r'transactions', TransactionListSet, 'transactions')

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/register/', include('rest_auth.registration.urls')),
    path('do_transaction', do_transaction),
    path('', include(router.urls)),
]
