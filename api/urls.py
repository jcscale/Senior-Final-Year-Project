from django.urls import path
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<str:slug>', views.AccountDetail.as_view()),
    # path('transaction', views.TransactionMixinView.as_view(), name='transaction'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
