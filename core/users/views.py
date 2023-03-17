from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from .forms import RegisterForm, LoginForm


# Create your views here.

def signup(request, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("crm:index")
        else:
            context['RegisterForm'] = form

    return render(request, 'users/signup/register.html', context)


def signin(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('user:profile')
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect('destination')
                return redirect('user:profile')
        else:
            context['LoginForm'] = form
    return render(request, 'users/signin/login.html', context)


def signout(request):
    logout(request)
    return redirect("crm:index")


def get_redirect_if_exists(request):
    reroute = None
    if request.GET:
        if request.GET.get('next'):
            reroute = str(request.GET.get('next'))
    return reroute


def profile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    else:
        return render(request, 'users/signin/profile.html')
