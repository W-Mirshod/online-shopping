from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from shopping.forms import LoginForm, RegistrationForm


def sign_up(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.save()
            login(request, user)
            return redirect('index')

    else:
        register_form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': register_form})


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    print(1)
    if request.method == 'GET':
        logout(request)
        return redirect('logout_page')
    return render(request, 'shopping/home.html')


def logout_page(request):
    return render(request, 'authentication/logout.html')
