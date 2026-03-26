from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

user_model = get_user_model()

def login(request):
    if request.method == 'POST':
        pass

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_model.objects.create_user(
            username=username,
            password=password
        )
        return redirect('/')
    return render(request, 'register.html')

def logout(request):
    pass