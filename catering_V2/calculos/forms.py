from django import forms
from .models import Ingrediente, Receta, RecetaIngrediente

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'marca', 'cantidad', 'unidad', 'precio']

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre']

class RecetaIngredienteForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente', 'cantidad_necesaria']

from django import forms
from .models import Catering


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'porciones']  # Incluir el campo porciones

from django import forms
from .models import Catering, CateringReceta

class CateringForm(forms.ModelForm):
    class Meta:
        model = Catering
        fields = ['nombre', 'cantidad_personas']

class CateringRecetaForm(forms.ModelForm):
    class Meta:
        model = CateringReceta
        fields = ['receta', 'porciones']

