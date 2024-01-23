from django.shortcuts import render
from .models import Relevance, Geography, Skills
# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def relevance(request):
    rel = Relevance.objects.all()
    return render(request, 'main/relevance.html', {'relevance':rel})

def geography(request):
    geo = Geography.objects.all()
    return render(request, 'main/geography.html', {'geography':geo})

def skills(request):
    skill = Skills.objects.all()
    return render(request, 'main/skills.html', {'skills':skill})

def recentVacancies(request):
    return render(request, 'main/recent.html')
