from rest_framework import serializers
from rvm.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['mobile_number', 'credits_earned',
                  'number_of_bottles', 'date']
