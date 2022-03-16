from rest_framework import serializers
from rvm.models import Deposit, Account, Withdraw


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['mobile_number', 'previous_credits_earned',
                  'previous_number_of_bottles', 'slug']


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['mobile_number', 'credits_earned',
                  'number_of_bottles', 'date']


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['mobile_number', 'pin_number', 'amount']
