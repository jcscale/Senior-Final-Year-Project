from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, PinForm
from django.contrib.auth import login, authenticate
from .models import Deposit, User, Account
from formtools.wizard.views import SessionWizardView
from django.db.models import Sum, Count
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse

from itertools import groupby
from operator import attrgetter
from django.db.models.functions import TruncDate

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
    bottles = Deposit.objects.aggregate(Sum('number_of_bottles'))[
        'number_of_bottles__sum']
    credits = Deposit.objects.aggregate(Sum('credits_earned'))[
        'credits_earned__sum']
    deposit_records = Deposit.objects.filter().values('date').order_by(
        'date').annotate(bottles=Sum('number_of_bottles'), credits=Sum('credits_earned'))

    total_bottles = Deposit.objects.all()[1:].values('number_of_bottles')
    total_credits = Deposit.objects.all()[1:].values('credits_earned')
    total_not_bottles = Deposit.objects.all()[1:].values('not_bottle')

    bottle_count = 0
    credit_count = 0
    not_bottle_count = 0
    for key, value in enumerate(total_bottles):
        bottle_count += value['number_of_bottles']
    for key, value in enumerate(total_credits):
        credit_count += value['credits_earned']
    for key, value in enumerate(total_not_bottles):
        not_bottle_count += value['not_bottle']

    records = Deposit.objects.all().order_by("date")
    # records = Deposit.objects.annotate(
    #     created_at_date=TruncDate('date'),).order_by("date")
    # groupedset = groupby(records, attrgetter('created_at_date'))

    bottle = Deposit.objects.aggregate(Sum('number_of_bottles'))[
        'number_of_bottles__sum']
    not_bottle = Deposit.objects.aggregate(Sum('not_bottle'))[
        'not_bottle__sum']
    try:
        arr = []
        for i in Deposit.objects.all():
            arr.append(i)

        print(arr)
        print(len(arr))
        arr.reverse()
        arr.pop()
        print(arr)
    except:
        pass

    print(records)

    print(bottles)
    print(credits)
    print(deposit_records)
    context = {
        'qs': deposit_records,
        'qs2': records,
        'qs3': arr,
        'bottle': bottle,
        "not_bottle": not_bottle,
        "credits": credits,
        "bottle_count": bottle_count,
        'credit_count': credit_count,
        'not_bottle_count': not_bottle_count
    }
    return render(request, 'rvm/adminpage/home3.html', context)


def event_stream():
    initial_data = ""

    while True:
        arr = []
        deposit_records = Deposit.objects.filter().values('date').order_by(
            '-id').annotate(bottles=Sum('number_of_bottles'), credits=Sum('credits_earned'), not_bottle=Sum('not_bottle'))
        bottle = Deposit.objects.aggregate(Sum('number_of_bottles'))[
            'number_of_bottles__sum']
        # deposit_records = Deposit.objects.order_by(
        #     "-id").values("number_of_bottles", "credits_earned", "date")
        data = json.dumps(list(deposit_records) +
                          list(str(bottle)), cls=DjangoJSONEncoder)
        # print(data)
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)


def stream(request):
    response = StreamingHttpResponse(event_stream())
    response['Content-Type'] = 'text/event-stream'
    return response


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
