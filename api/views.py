from os import stat
from django.http.response import Http404
from django.shortcuts import render
from rvm.models import Deposit, Account
from .serializers import DepositSerializer, AccountSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics, status
from rest_framework.response import Response

# Create your views here.


# class TransactionMixinView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class AccountList(APIView):
    def get(self, request, format=None):
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)


class AccountDetail(APIView):
    def get_object(self, slug):
        try:
            return Account.objects.get(slug=slug)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        account = self.get_object(slug)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def post(self, request, slug, format=None):
        account = self.get_object(slug)
        serializer = AccountSerializer(account, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
