from django.shortcuts import render
from rvm.models import Transaction
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Create your views here.


class TransactionMixinView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
