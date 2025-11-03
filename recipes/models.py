from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = RichTextUploadingField()  # HTML + images uploadées via CKEditor
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

