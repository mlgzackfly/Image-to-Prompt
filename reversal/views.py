# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'reversal/index.html')


def app(request):
    return render(request, 'reversal/app.html')


def about(request):
    return render(request, 'reversal/about.html')