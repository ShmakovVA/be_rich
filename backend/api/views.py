import logging

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from backend.api.paginators import LimitedOffsetPaginator
from backend.transactions.models import Transaction, Wallet, Account
from backend.transactions.serializers import (
    TransactionSerializer,
    AccountSerializer,
    WalletSerializer
)

logger = logging.getLogger(__name__)


class PaginatedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitedOffsetPaginator
    user = None
    is_superuser = False

    def get_queryset(self):
        self.get_user()
        return super(PaginatedReadOnlyModelViewSet, self).get_queryset()

    def get_user(self):
        self.user = self.request.user
        self.is_superuser = self.user.is_superuser

    def list(self, request, **kwargs):
        qs = self.queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# TODO: Make it filterable and sortable
class TransactionListSet(PaginatedReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_superuser:
            return self.queryset
        account = self.user.account
        q_from = Q(from_wallet__account=account)
        q_to = Q(to_wallet__account=account)
        self.queryset = qs.filter(q_from | q_to)
        return self.queryset


class AccountListSet(PaginatedReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_superuser:
            return self.queryset
        self.queryset = qs.filter(pk=self.user.account.pk)
        return self.queryset


class WalletListSet(PaginatedReadOnlyModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_superuser:
            return self.queryset
        self.queryset = qs.filter(account=self.user.account)
        return self.queryset


@api_view(["POST"])
@permission_classes((AllowAny,))
def do_transaction(request):
    # token = request.query_params.get("token")
    # filter = request.query_params.get("token")
    # try:
    #     token = Token.objects.get(key=token)
    # except Token.DoesNotExist:
    #     logger.error(f'Wrong Token: {token}')
    #     return Response(
    #         {'error': 'Please provide both username and password'},
    #         status=HTTP_404_NOT_FOUND)
    # else:
    #     account = token.user.account
    #     test_data = WalletSerializer(
    #         Wallet.objects.filter(account=account), many=True
    #     ).data
    #     return Response(test_data, status=HTTP_200_OK)
    return Response({}, status=HTTP_200_OK)
