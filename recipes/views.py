from django.shortcuts import render
from django.http import HttpResponse
from .forms import RecipeForm
from django.http import Http404

def accueil(request):
    return render(request, "recipes/accueil.html")

def recipes(request, page):
    pages_autorisees = ['entrees', 'desserts', 'plats_principaux', 'boissons', 'divers']
    
    if page not in pages_autorisees:
        raise Http404 ("Page introuvable")

    return render(request, f"{page}.html")


def ajouter_recette(request):
    if request.method == 'POST': # L'utilisateur a soumis le formulaire
        form = RecipeForm(request.POST) # On remplit le formulaire avec les données envoyées
        if form.is_valid(): # Vérifie que les données sont valides
            # Logique pour enregistrer la recette
            titre = form.cleaned_data['title']
            ingredients = form.cleaned_data['ingredients']
            instructions = form.cleaned_data['instructions']

            return HttpResponse("Recette ajoutée avec succès !")
            
    else:# Première visite sur la page → on affiche un formulaire vide
        form = RecipeForm()

    # Affiche la page avec le formulaire (vide ou rempli en cas d'erreur)
    return render(request, 'ajouter_recette.html', {'form': form})

