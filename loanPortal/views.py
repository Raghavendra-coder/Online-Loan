from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, UpdateForm, LoanForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import User, Loan, UserLoan, Profile, AccuracyTable
from .train_model import get_approval_probability, train_model
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            login(request, user)
            role = user.role
            if role == 'Admin':
                return HttpResponseRedirect(reverse('home'))
            elif role == 'Agent':
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('home'))
    context = {
        'form': form,
    }
    return render(request, "user_login.html", context)


def user_signup(request):
    role = request.GET.get('role')
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            if role == 'admin':
                user_role = 'Admin'
            elif role == 'agent':
                user_role = 'Agent'
            else:
                user_role = 'Customer'
            user.role = user_role
            user.save()
            return HttpResponseRedirect(reverse('cong'))
    context = {
        'form': form,
    }
    return render(request, 'user_signup.html', context)


def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def update_profile(request):
    form = UpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse(user_login))
    context = {
        'form': form,
    }
    return render(request, 'update_profile.html', context)


def loan_form(request):
    form = LoanForm()
    user = request.user
    loans = Loan.objects.all()
    print("111")
    if request.method == 'POST':
        print("222")
        form = LoanForm(request.POST)
        if form.is_valid():
            print("333")
            loan = form.save(commit=False)
            print("444")
            r = form.cleaned_data['loan_type'].interest
            print(r, 'r')
            p = form.cleaned_data['principle']
            t = form.cleaned_data['tenure']
            print(type(r), type(t), type(p))
            si = float((p * r * t) / 100.0)
            amount = float(p + si)
            e = float(amount / t)
            e = round(e, 2)
            loan.emi = e
            loan.user = user
            loan.save()
            print(p, r, t, si, e, amount)
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
    context = {
        'form': form,
        'user': user,
        'loans': loans,
    }
    return render(request, 'loan_form.html', context)


def calculate_emi(request):
    r = request.GET.get('loan_type')
    p = request.GET.get('principle')
    t = request.GET.get('tenure')
    if r and p and t:
        p, t, r = float(p), float(t), int(r)
        loan = Loan.objects.filter(pk=r).first()
        if loan:
            rate = loan.interest
            si = (p * rate * t) / 100.0
            amount = p + si
            e = amount / t
            e = "{:.2f}".format(e)
            data = {
                'status': True,
                'e': e,
            }
        else:
            data = {
                'status':False,
                'message': 'Loan type incorrect'
            }

    else:
        data = {
            'status': False,
        }
    return JsonResponse(data)


def request_loan(request):
    loans = UserLoan.objects.all()
    searched_filter = request.GET.get('filter')
    searched_value = request.GET.get('value')

    if searched_filter and searched_value:
        if searched_filter == '1':
            loans = loans.filter(loan_type__name=searched_value)
        elif searched_filter == '2':
            loans = loans.filter(date=searched_value)
        elif searched_filter == '3':
            loans = loans.filter(updated_date=searched_value)
    context = {
        'loans': loans,
    }
    return render(request, 'request_loan.html', context)


def loan_status(request, pk):
    loan = UserLoan.objects.filter(pk=pk).first()
    user = loan.user.profile
    prob = get_approval_probability(loan.principle, user.married, user.dependents, user.education, user.self_employed,
                                    user.income, user.credit_history, user.gender)
    # get_approval_probability(UserLoan)
    # probability = AccuracyTable.objects.order_by('-created_on').first()
    # accuracy = probability.accuracy
    if prob == 1:
        messages.success(request, f'This form has high probability of approval')
    else:
        messages.error(request, 'this loan may not be approved')
    form = LoanForm(instance=loan)
    i_loan = Loan.objects.all()
    if request.method == 'POST':
        loan.loan_status = 'Rq'
        loan.save()
        return HttpResponseRedirect(reverse('request_loan'))
    context = {
        'loan': loan,
        'form': form,
        'i_loan': i_loan,
    }
    return render(request, 'loan_status.html', context)


def requested_loan(request):
    loans = UserLoan.objects.filter(Q(loan_status="Rq") | Q(loan_status='Ap') | Q(loan_status="Rj"))
    searched_filter = request.GET.get('filter')
    searched_value = request.GET.get('value')
    if searched_filter and searched_value:
        if searched_filter == '1':
            loans = loans.filter(loan_type__name=searched_value)
        elif searched_filter == '2':
            loans = loans.filter(date=searched_value)
        elif searched_filter == '3':
            loans = loans.filter(updated_date=searched_value)
    context = {
        'loans': loans,
    }
    return render(request, "requested_loan.html", context)


def approve_loan(request, pk):
    loan = UserLoan.objects.filter(pk=pk).first()
    if request.method == 'POST':
        loan.loan_status = 'Ap'
        loan.save()
        return HttpResponseRedirect(reverse('requested_loan'))
    context = {
        'loan': loan,
    }
    return render(request, "approve_loan.html", context)


def reject_loan(request, pk):
    UserLoan.objects.filter(pk=pk).update(loan_status="Rj")

    return HttpResponseRedirect(reverse('requested_loan'))


def my_loan(request):
    loan = UserLoan.objects.filter(user=request.user)
    context = {
        'loan': loan,
    }
    return render(request, 'my_loan.html', context)


def list_user(request):
    user = User.objects.all()
    context = {
        'user': user,
    }
    return render(request, 'list_user.html', context)


def remove_user(request, pk):
    User.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('list_user'))


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def cong(request):
    return render(request, 'cong.html')


def Train(request):
    train_model()
    return HttpResponseRedirect(reverse('requested_loan'))



