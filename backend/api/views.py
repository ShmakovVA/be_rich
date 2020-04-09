import json
import logging

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from backend.api.paginators import LimitedOffsetPaginator
from backend.transactions.enums import TransactionTypes
from backend.transactions.exceptions import TransactionError
from backend.transactions.forms import DoTransactionForm
from backend.transactions.models import Transaction, Wallet, Account
from backend.transactions.serializers import (
    TransactionSerializer,
    AccountSerializer,
    WalletSerializer
)

logger = logging.getLogger(__name__)


class PaginatedModelViewSet(viewsets.ModelViewSet):
    pagination_class = LimitedOffsetPaginator
    user = None
    is_superuser = False

    def get_queryset(self):
        self.get_user()
        return super(PaginatedModelViewSet, self).get_queryset()

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
        return Response(serializer.data, status=HTTP_200_OK)


class AccountListSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        qs = super(AccountListSet, self).get_queryset()
        if self.request.user.is_superuser:
            return self.queryset
        self.queryset = qs.filter(pk=self.request.user.account.pk)
        return self.queryset

    @action(detail=False, methods=['POST'])
    def do_transaction(self, request, *args, **kwargs):
        account = request.user.account
        form = DoTransactionForm(request.data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            from_wallet = cleaned_data['wallet_from']
            to_wallet = cleaned_data['wallet_to']
            amount = cleaned_data['amount']
            message = cleaned_data['message']
        else:
            logger.error(f'Transaction form has errors: {form.errors}')
            return Response({'error': 'Wrong parameters for transaction'},
                            status=HTTP_200_OK)
        try:
            transaction = account.init_transaction(
                wallet_id_from=from_wallet,
                wallet_id_to=to_wallet,
                amount=amount,
                message=message
            )
        except TransactionError as e:
            logger.error(f'Transaction was aborted: {e}')
            return Response({'error': e.message}, status=HTTP_200_OK)
        except Exception as e:
            logger.error(f'Fatal error: {e}')
            return Response({'error': str(e)},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(TransactionSerializer(transaction).data,
                            status=HTTP_200_OK)


class WalletListSet(PaginatedModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        qs = super(WalletListSet, self).get_queryset()
        if self.is_superuser:
            return self.queryset
        self.queryset = qs.filter(account=self.user.account)
        return self.queryset


# TODO: Make it filterable via 3 party like  django-rest-framework-filters ?
class TransactionListSet(PaginatedModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def filter_queryset_by_user(self, qs):
        account = self.user.account
        q_from = Q(from_wallet__account=account)
        q_to = Q(to_wallet__account=account)
        return qs.filter(q_from | q_to)

    def get_queryset(self):
        qs = super(TransactionListSet, self).get_queryset()
        # TODO: add checks/validation for sort_by / filters
        sort_by = self.request.query_params.get('sort_by', None)
        filters = self.request.query_params.get('filters', None)

        if not self.is_superuser:
            qs = self.filter_queryset_by_user(qs)

        if filters is not None:
            filters = json.loads(filters)
            if 'status' in filters and not filters['status'].isnumeric():
                filters['type'] = TransactionTypes.get(filters['status'])
            if 'amount' in filters:
                filters['amount'] = float(filters['amount'])
            if 'to_wallet' in filters:
                filters['to_wallet'] = Wallet.objects.filter(
                    wallet_id=filters['to_wallet']).first()
            if 'from_wallet' in filters:
                filters['from_wallet'] = Wallet.objects.filter(
                    wallet_id=filters['from_wallet']).first()
            qs = qs.filter(**filters)

        if sort_by is not None:
            qs = qs.order_by(sort_by)

        self.queryset = qs
        return self.queryset
