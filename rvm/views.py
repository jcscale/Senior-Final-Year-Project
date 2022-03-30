from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, PinForm
from django.contrib.auth import login, authenticate
from .models import User, Account
from formtools.wizard.views import SessionWizardView

# Create your views here.


##### USER #####
def admin_login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage_home')
            else:
                msg = 'Account does not exist'
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'rvm/adminpage/login.html', context)


def adminpage_home(request):
    return render(request, 'rvm/adminpage/home.html')


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
            return redirect('login')

        else:
            msg = 'Form is not valid'
    else:
        form = SignupForm()
    return render(request, 'rvm/user/register.html', {'form': form, 'msg': msg})


def user_login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_user:
                login(request, user)
                return redirect('user_home')
            else:
                msg = 'Account does not exist'

    context = {
        'form': form,
        'msg': msg
    }

    return render(request, 'rvm/user/login.html', context)


class RegisterWizard(SessionWizardView):
    template_name = 'rvm/user/wizard.html'

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)
        return render(self.request, 'rvm/user/done.html', {'form_data': form_data})


def process_form_data(form_list):
    form_data = [form.cleaned_data for form in form_list]

    first_name = form_data[0]['first_name']
    last_name = form_data[0]['last_name']
    mobile_number = form_data[0]['mobile_number']
    username = form_data[0]['username']
    password1 = form_data[0]['password1']
    password2 = form_data[0]['password2']
    pin_number = form_data[1]['pin_number']

    user = User.objects.create_user(
        first_name=first_name, last_name=last_name, username=username, password=password1, is_user=True)
    user.save()
    Account.objects.create(
        user=user, mobile_number=mobile_number, pin_number=pin_number)

    msg = 'User Created'
    context = {
        "msg": msg,
        "form_data": form_data
    }
    return context


def done(request):
    return render(request, 'rvm/user/done')


def user_home(request):
    return render(request, 'rvm/user/home.html')
