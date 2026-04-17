from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/tickets/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/tickets/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('/login/')

