from rest_framework import generics
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from backend.transactions.models import Transaction, Wallet, Account
from backend.transactions.paginators import LimitedOffsetPaginator
from backend.transactions.serializers import (
    TransactionSerializer,
    AccountSerializer,
    WalletSerializer
)


class TransactionListSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    pagination_class = LimitedOffsetPaginator

    def list(self, request, **kwargs):
        qs = self.queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class AccountListSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = LimitedOffsetPaginator

    def list(self, request, **kwargs):
        qs = self.queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class WalletListSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = LimitedOffsetPaginator

    def list(self, request, **kwargs):
        qs = self.queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
