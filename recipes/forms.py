from django import forms

class RecipeForm(forms.Form):
    title = forms.CharField(max_length=100)
    ingredients = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    photos = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)


#forms.FileField : crée un champ pour l’envoi de fichiers (images, PDF, etc.).
#widget=forms.ClearableFileInput(attrs={'multiple': True}) : Utilise un widget qui permet à l’utilisateur de sélectionner plusieurs fichiers à la fois (grâce à l’attribut HTML multiple).
#Le widget « ClearableFileInput » permet aussi de supprimer un fichier déjà envoyé lors de la modification d’un formulaire.
#required=False : rend ce champ optionnel (l’utilisateur peut ne pas envoyer de photo).