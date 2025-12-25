from importlib.resources import files
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST #ce décorateur permet de restreindre une vue à une méthode HTTP spécifique
from django.http import HttpResponse, JsonResponse
from .forms import RecipeForm
from .models import Recipe, Photo
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required

def accueil(request): 
    # Affiche la page d'accueil des recettes
    return render(request, "recipes/accueil.html")
 
def recipes(request, page):
    #vérifie que la page demandée est bien dans la liste des pages autorisées, sinon lève une 404
    pages_autorisees = ['entrees', 'desserts', 'plats_principaux', 'boissons', 'divers']
    if page not in pages_autorisees:
        raise Http404 ("Page introuvable")

    # Filtrage des recettes selon la catégorie
    category_map = {
        'entrees': 'entree',
        'desserts': 'dessert',
        'plats_principaux': 'plat_principal',
        'boissons': 'boisson',
    }
    recipes = []
    if page in category_map:
        recipes = Recipe.objects.filter(category=category_map[page]).order_by('-created_at')
    return render(request, f"{page}.html", {'recipes': recipes, 'page': page})


def ajouter_recette(request):
    if request.method == 'POST': # L'utilisateur a soumis le formulaire
        form = RecipeForm(request.POST, request.FILES)
        # appeler getlist() pour obtenir la liste de fichiers uploadés
        files = request.FILES.getlist('photos')

        if form.is_valid(): # Vérifie que les données sont valides
            recipe = form.save(commit=False)
            recipe.author = request.user if request.user.is_authenticated else None
            recipe.save()
            if len(files) > 10:
                form.add_error(None, "Maximum 10 photos autorisées.")
            else:
                for f in files:
                    try:
                        Photo.objects.create(recipe=recipe, image=f)
                    except NameError:
                        # Photo n'existe pas : ignorer ou gérer différemment
                        pass
                return redirect('accueil_recipes')
                # Première visite sur la page → on affiche un formulaire vide
    else:
       form = RecipeForm()

    # Affiche la page avec le formulaire (vide ou rempli en cas d'erreur)
    return render(request, 'ajouter_recette.html', {'form': form})

def recette_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recette_detail.html', {'recipe': recipe})

@require_POST #La méthode upload_photo ne répond qu'aux requêtes POST, sinon faudrait écrire un code.
def upload_photo(request):

    file = request.FILES.get('photo') or request.FILES.get('file') # Récupère le fichier uploadé
    if not file:
         return JsonResponse({'error': 'Aucun fichier reçu (champ "image")'}, status=400)
        
    # validation type MIME
    if not file.content_type.startswith('image/'):
        return JsonResponse({'error': 'Invalid file type. Only images are allowed.'}, status=400)

    #validation taille fichier (ex: max 5MB)
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    if file.size > MAX_SIZE:
        return JsonResponse({'error': 'Le fichier est trop volumineux.'}, status=400)
    
    #enregistrement du fichier
    uploader = request.user if request.user.is_authenticated else None #
    photo = Photo.objects.create(image=file, recipe=None, uploader=uploader)

    # construire URL de l'image accessible
    url = request.build_absolute_uri(settings.MEDIA_URL + photo.image.name)
    return JsonResponse({'url': url, 'photo_id': photo.id})

@login_required
def modifier_recette(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponse("Vous n'êtes pas autorisé à modifier cette recette.", status=403)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes:recette_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'modifier_recette.html', {'form': form, 'recipe': recipe})