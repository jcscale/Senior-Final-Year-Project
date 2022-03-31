from django.urls import path
from . import views
from .forms import SignupForm, PinForm


urlpatterns = [
    ##### ADMIN #####
    path('adminpage/', views.admin_login_view, name='adminpage'),
    path('adminpage_home/', views.adminpage_home, name='adminpage_home'),
    path('stream', views.stream, name='stream'),

    ##### USER #####
    path('register/', views.register, name='register'),
    path('', views.user_login_view, name='login'),
    path('home', views.user_home, name='user_home'),

    path('register2/',
         views.RegisterWizard.as_view([SignupForm, PinForm]), name='register2'),
    path('done', views.done, name='done')
]
