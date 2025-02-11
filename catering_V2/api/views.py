from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings
import openai

from .serializers import (
    IngredienteSerializer, RecetaSerializer,
    RecetaIngredienteSerializer, CateringSerializer,
    CateringRecetaSerializer
)
from calculos.models import (
    Ingrediente, Receta, RecetaIngrediente,
    Catering, CateringReceta
)
from .models import ChatMessage  # Asegúrate de que existe en `api/models.py`


def chatbot_view(request):
    """Renderiza la página del chatbot con el token CSRF."""
    csrf_token = get_token(request)
    return render(request, 'api/chatbot.html', {"csrf_token": csrf_token})


class GPTInteractionView(APIView):
    """
    Recibe un mensaje vía POST y devuelve la respuesta de GPT-4.
    """
    def post(self, request):
        user_message = request.data.get("message", "")
        if not user_message:
            return Response({"error": "No se recibió ningún mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}]
            )
            gpt_response = response['choices'][0]['message']['content']

            # Guardar la interacción en la base de datos
            ChatMessage.objects.create(sender="user", message=user_message)
            ChatMessage.objects.create(sender="bot", message=gpt_response)

            return Response({
                "user_message": user_message,
                "gpt_response": gpt_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GPTDatabaseInteractionView(APIView):
    """
    Consulta los ingredientes en la BD y construye un prompt para sugerir recetas o consejos a través de GPT-4.
    """
    def post(self, request):
        user_message = request.data.get("message", "")
        if not user_message:
            return Response({"error": "No se recibió ningún mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener ingredientes de la base de datos
            ingredientes = Ingrediente.objects.all().values("nombre", "cantidad", "unidad", "precio")

            # Formatear la lista de ingredientes
            ingredientes_texto = "\n".join([
                f"{ing['nombre']}: {ing['cantidad']} {ing['unidad']} - ${ing['precio']}"
                for ing in ingredientes
            ])

            # Crear el prompt
            prompt = (
                f"Tienes los siguientes ingredientes disponibles:\n"
                f"{ingredientes_texto}\n"
                f"Usuario pregunta: {user_message}\n"
                "Responde con una sugerencia de recetas o consejos de uso."
            )

            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            gpt_response = response['choices'][0]['message']['content']

            # Guardar la interacción
            ChatMessage.objects.create(sender="user", message=user_message)
            ChatMessage.objects.create(sender="bot", message=gpt_response)

            return Response({
                "user_message": user_message,
                "gpt_response": gpt_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
#  ModelViewSets para manejar CRUD completo de todos los modelos
#

class IngredienteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar ingredientes.
    Permite GET, POST, PUT y DELETE automáticamente.
    """
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer


class RecetaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar recetas.
    """
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer


class RecetaIngredienteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la relación entre recetas e ingredientes.
    """
    queryset = RecetaIngrediente.objects.all()
    serializer_class = RecetaIngredienteSerializer


class CateringViewSet(viewsets.ModelViewSet):
    """
    API para gestionar caterings.
    """
    queryset = Catering.objects.all()
    serializer_class = CateringSerializer


class CateringRecetaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la relación entre caterings y recetas.
    """
    queryset = CateringReceta.objects.all()
    serializer_class = CateringRecetaSerializer

from django.http import FileResponse, JsonResponse
import os

def descargar_schema_txt(request):
    """
    Devuelve el archivo OpenAPI Schema en formato .txt
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../openapi_schema.txt")  # Ruta en la raíz
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), content_type="text/plain")
    return JsonResponse({"error": "Archivo no encontrado"}, status=404)

def descargar_prompt_txt(request):
    """
    Devuelve el archivo prompt_gpt Schema en formato .txt
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../prompt_gpt.txt")  # Ruta en la raíz
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), content_type="text/plain")
    return JsonResponse({"error": "Archivo no encontrado"}, status=404)