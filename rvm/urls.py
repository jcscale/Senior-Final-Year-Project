from django.urls import path
from . import views


urlpatterns = [
    ##### USER #####
    path('register/', views.register, name='register'),
    path('', views.user_login_view, name='login'),
    path('home', views.user_home, name='user_home')
]
