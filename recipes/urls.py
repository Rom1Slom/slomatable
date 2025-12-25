from django.urls import path, include
from . import views

app_name = 'recipes'

urlpatterns = [
    path('ajouter-recette/', views.ajouter_recette, name='ajouter_recette'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),  # <-- ENDPOINT AJAX
    path('', views.accueil, name='accueil_recipes'),
    path('detail/<int:pk>/', views.recette_detail, name='recette_detail'),
    path('<str:page>/', views.recipes, name='recipes'),
]