from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:page>/', views.recipes, name='recipes'),
    path('ajouter-recette/', views.ajouter_recette, name='ajouter_recette'),
    path('', views.accueil, name='accueil_recipes'),
]