from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#import Question by model

@login_required
def index(request):
    return render(request, 'main/home.html', {})
