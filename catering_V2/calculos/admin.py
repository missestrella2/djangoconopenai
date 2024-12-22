from django.contrib import admin
from .models import Ingrediente, Receta, RecetaIngrediente, Catering

admin.site.register(Ingrediente)
admin.site.register(Receta)
admin.site.register(RecetaIngrediente)
admin.site.register(Catering)
