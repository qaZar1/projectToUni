from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def relevance(request):
    return render(request, 'main/geography.html')

def geography(request):
    return render(request, 'main/geography.html')

def skills(request):
    return HttpResponse("<h4>Навыки</h4>")

def recentVacancies(request):
    return HttpResponse("<h4>Последние вакансии</h4>")