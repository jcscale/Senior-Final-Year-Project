import decimal
from os import stat
from django.http.response import Http404
from django.shortcuts import render
from rvm.models import Deposit, Account, Withdraw
from .serializers import DepositSerializer, AccountSerializer, WithdrawSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics, serializers, status
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

    # def post(self, request, slug, format=None):
    #     account = self.get_object(slug)
    #     serializer = AccountSerializer(account, data=request.data)
    #     print(request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositListView(APIView):
    def get(self, request, format=None):
        deposit = Deposit.objects.all()
        serializer = DepositSerializer(deposit, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            mobile = Account.objects.filter(
                mobile_number=serializer.data['mobile_number']).exists()
            if mobile == True:
                user = Account.objects.get(
                    mobile_number=serializer.data['mobile_number'])
                print(user)
                Account.objects.filter(user=user.user).update(previous_number_of_bottles=serializer.data['number_of_bottles'], previous_credits_earned=serializer.data['credits_earned'], total_number_of_bottles=int(
                    user.total_number_of_bottles)+int(serializer.data['number_of_bottles']), total_credits_earned=decimal.Decimal(user.total_credits_earned)+decimal.Decimal(serializer.data['credits_earned']))
            else:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):
    def get(self, request, format=None):
        withdraw = Withdraw.objects.all()
        serializer = WithdrawSerializer(withdraw, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            user = Account.objects.get(
                mobile_number=serializer.validated_data['mobile_number'], pin_number=serializer.validated_data['pin_number'])
            if serializer.validated_data['amount'] <= decimal.Decimal(user.total_credits_earned):
                withdraw = decimal.Decimal(
                    user.total_credits_earned) - serializer.validated_data['amount']
                Account.objects.filter(user=user.user).update(
                    total_credits_earned=withdraw)
                # print(user.total_credits_earned)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Failed": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
