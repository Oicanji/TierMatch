from django.shortcuts import render, redirect
from .forms import RegisterForm

from django.contrib.auth.models import User

def register(request):
    if User.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})