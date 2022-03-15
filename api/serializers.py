from rest_framework import serializers
from rvm.models import Deposit, Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['mobile_number', 'previous_credits_earned',
                  'previous_number_of_bottles']


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['mobile_number', 'credits_earned',
                  'number_of_bottles', 'date']
