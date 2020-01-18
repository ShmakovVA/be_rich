import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from backend.transactions.models import Wallet
from backend.transactions.serializers import WalletSerializer

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {'error': 'Please provide both username and password'},
            status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {'error': 'Please provide both username and password'},
            status=HTTP_400_BAD_REQUEST)

    User(username=username, email=username, password=password)
    user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def test(request):
    token = request.query_params.get("token")
    filter = request.query_params.get("token")
    try:
        token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        logger.error(f'Wrong Token: {token}')
        return Response(
            {'error': 'Please provide both username and password'},
            status=HTTP_404_NOT_FOUND)
    else:
        account = token.user.account
        test_data = WalletSerializer(
            Wallet.objects.filter(account=account), many=True
        ).data
        return Response(test_data, status=HTTP_200_OK)
