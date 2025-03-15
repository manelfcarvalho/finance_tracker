from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('transactions:dashboard')  # Redireciona para o dashboard após registro
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('transactions:dashboard') 
    return render(request, 'home.html')
 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('transactions:dashboard')  # Redireciona para o dashboard após login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para login após logout
