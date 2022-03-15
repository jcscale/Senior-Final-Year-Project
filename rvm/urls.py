from django.urls import path
from . import views
from .forms import SignupForm, PinForm


urlpatterns = [
    ##### USER #####
    path('register/', views.register, name='register'),
    path('', views.user_login_view, name='login'),
    path('home', views.user_home, name='user_home'),

    path('register2/', views.RegisterWizard.as_view([SignupForm, PinForm])),
    path('done', views.done, name='done')
]
