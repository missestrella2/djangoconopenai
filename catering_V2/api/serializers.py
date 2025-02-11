# api/serializers.py

from rest_framework import serializers
from calculos.models import Ingrediente, Receta, RecetaIngrediente, Catering, CateringReceta

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = '__all__'

class RecetaIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaIngrediente
        fields = '__all__'

class CateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catering
        fields = '__all__'

class CateringRecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringReceta
        fields = '__all__'
