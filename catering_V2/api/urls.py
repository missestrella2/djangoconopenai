# api/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    chatbot_view,
    crear_ingrediente,
    GPTInteractionView,
    GPTDatabaseInteractionView,
    IngredienteViewSet,
    RecetaViewSet,
    RecetaIngredienteViewSet,
    CateringViewSet,
    CateringRecetaViewSet
)

# 1. Rutas "normales" que ya tenías
urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot'),
    path('ingredientes/', crear_ingrediente, name='crear_ingrediente'),  # Endpoint custom para crear ingrediente
    path('chatbot/gpt/', GPTInteractionView.as_view(), name='gpt_interaction'),
    path('openapi/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='swagger-ui'),
    # Si tienes más rutas personalizadas, agrégalas aquí
]

# 2. Crea un Router y registra los ViewSets
router = DefaultRouter()
router.register(r'ingredientes-viewset', IngredienteViewSet, basename='ingredientes-viewset')
router.register(r'recetas', RecetaViewSet, basename='recetas')
router.register(r'receta-ingredientes', RecetaIngredienteViewSet, basename='receta-ingredientes')
router.register(r'caterings', CateringViewSet, basename='caterings')
router.register(r'catering-recetas', CateringRecetaViewSet, basename='catering-recetas')

# 3. Agrega las rutas generadas por el router a urlpatterns
urlpatterns += router.urls
