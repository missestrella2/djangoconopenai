from django.db import models
from decimal import Decimal

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=100, default='ejemplo: gramos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.marca})" if self.marca else self.nombre

    def delete(self, *args, **kwargs):
        if RecetaIngrediente.objects.filter(ingrediente=self).exists():
            raise ValueError(f"No se puede eliminar el ingrediente '{self.nombre}' porque está asociado a una o más recetas.")
        super().delete(*args, **kwargs)


class Receta(models.Model):
    nombre = models.CharField(max_length=100)
    porciones = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if CateringReceta.objects.filter(receta=self).exists():
            raise ValueError(f"No se puede eliminar la receta '{self.nombre}' porque está asociada a uno o más caterings.")
        super().delete(*args, **kwargs)


# Tabla intermedia para definir ingredientes en recetas
class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE, related_name="ingredientes")
    ingrediente = models.ForeignKey(
        Ingrediente, on_delete=models.CASCADE, related_name="recetas")
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad_necesaria} {self.ingrediente.unidad} de {self.ingrediente.nombre} para {self.receta.nombre}"

class Catering(models.Model):
    nombre = models.CharField(max_length=100, default="Catering genérico")
    cantidad_personas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.cantidad_personas} personas)"


class CateringReceta(models.Model):
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE, related_name="recetas")
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE)
    porciones = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.receta.nombre} en {self.catering.nombre} ({self.porciones} porciones)"