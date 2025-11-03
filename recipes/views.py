from importlib.resources import files
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .forms import RecipeForm
from .models import Recipe
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
            if len(files) > 10:
                form.add_error(None, "Maximum 10 photos autorisées.")
            else:
                recipe = form.save()
                for f in files:
                    Photo.objects.create(recipe=recipe, image=f)
                return redirect('recipes', 'accueil')
            
    else:# Première visite sur la page → on affiche un formulaire vide
        form = RecipeForm()

    # Affiche la page avec le formulaire (vide ou rempli en cas d'erreur)
    return render(request, 'ajouter_recette.html', {'form': form})

def recette_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recette_detail.html', {'recipe': recipe})