from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings # on peut aussi importer le module settings

# Create your models here.

Categories = [
    ('entree', 'Entrée'),
    ('dessert', 'Dessert'),
    ('plat_principal', 'Plat principal'),
    ('boisson', 'Boisson'),
    ]

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    category= models.CharField(max_length=20, choices=Categories, default='plat_principal')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) #Pour lier la recette à un utilisateur, on_delete=models.SET_NULL pour ne pas supprimer la recette si l'utilisateur est supprimé
    ingredients = models.TextField()
    instructions = RichTextUploadingField()  # HTML + images uploadées via CKEditor
    created_at = models.DateTimeField(auto_now_add=True)
    
    CATEGORIES = [
        ('entree', 'Entrée'),
        ('plat_principal', 'Plat principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    ]

    def __str__(self):
        return self.title

class Photo(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='photos', on_delete=models.SET_NULL, null=True, blank=True) # Permet de lier la photo à une recette, on_delete=models.SET_NULL pour ne pas supprimer la photo si la recette est supprimée
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) #Pour lier la photo à un utilisateur, on_delete=models.SET_NULL pour ne pas supprimer la photo si l'utilisateur est supprimé
    image = models.ImageField(upload_to='recipe_photos/')
    caption = models.CharField(max_length=200, blank=True)
    optimized = models.BooleanField(default=False) # Indique si la photo a été optimisée
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.recipe.title}" if self.recipe else f"Photo #{self.id} (no recipe)" # Gestion du cas où recipe pourrait être None
