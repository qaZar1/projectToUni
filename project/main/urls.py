from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("relevance", views.relevance, name='relevance'),
    path("geography", views.geography, name='geography'),
    path("skills", views.skills, name='skills'),
    path("recentVacancies", views.recentVacancies, name='recent'),
]
