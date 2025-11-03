from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe
import re

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 6}),
            'instructions': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_instructions(self):
        value = self.cleaned_data.get('instructions', '') or ''
        # compte occurrences de balises <img ...> dans le HTML
        img_count = len(re.findall(r'<img\b', value, flags=re.IGNORECASE))
        if img_count > 5:
            raise ValidationError("Maximum 5 images autorisées dans les instructions (actuellement : %d)." % img_count)
        return value
        