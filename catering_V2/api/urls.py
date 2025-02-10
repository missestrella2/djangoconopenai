from django.urls import path
from . import views
from .views import GPTDatabaseInteractionView  # Importamos la nueva vista con OpenAI
from .views import crear_ingrediente  # Importa la función correctamente
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import GPTInteractionView  # Asegúrate de importar la vista

urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('ingredientes/', crear_ingrediente, name='crear_ingrediente'),
    path('openapi/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='swagger-ui'),
    path('chatbot/gpt/', GPTInteractionView.as_view(), name='gpt_interaction'),
]




