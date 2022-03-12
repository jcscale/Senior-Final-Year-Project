from django.urls import path
from . import views


urlpatterns = [
    ##### USER #####
    path('register/', views.register, name='register')
]
