from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User, Account

# Create your views here.


##### USER #####
def register(request):
    msg = None
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile_number = form.cleaned_data['mobile_number']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, password=password1, is_user=True)
            user.save()
            Account.objects.create(user=user, mobile_number=mobile_number)

            msg = 'User Created'
            return redirect('api/transaction/')

        else:
            msg = 'Form is not valid'
    else:
        form = SignupForm()
    return render(request, 'rvm/authentication/register.html', {'form': form, 'msg': msg})
