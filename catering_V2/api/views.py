# api/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from decimal import Decimal
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
# Asegúrate de que exista un modelo ChatMessage en api/models.py,
# o ajusta este import según corresponda a tu proyecto
from .models import ChatMessage


def chatbot_view(request):
    """Renderiza la página del chatbot con el token CSRF."""
    csrf_token = get_token(request)
    return render(request, 'api/chatbot.html', {"csrf_token": csrf_token})


@csrf_exempt
def crear_ingrediente(request):
    """
    Crea un ingrediente en la base de datos de Django.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extraer datos
            nombre = data.get("nombre", "")
            marca = data.get("marca", None)
            cantidad = Decimal(data.get("cantidad", "0"))
            unidad = data.get("unidad", "g")
            precio = Decimal(data.get("precio", "0"))

            # Guardar en la base de datos
            Ingrediente.objects.create(
                nombre=nombre,
                marca=marca,
                cantidad=cantidad,
                unidad=unidad,
                precio=precio
            )

            return JsonResponse({"message": "Ingrediente creado correctamente"}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Error al crear ingrediente: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


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
#  A continuación, los ModelViewSet para un CRUD completo en toda la BD
#

class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

class RecetaIngredienteViewSet(viewsets.ModelViewSet):
    queryset = RecetaIngrediente.objects.all()
    serializer_class = RecetaIngredienteSerializer

class CateringViewSet(viewsets.ModelViewSet):
    queryset = Catering.objects.all()
    serializer_class = CateringSerializer

class CateringRecetaViewSet(viewsets.ModelViewSet):
    queryset = CateringReceta.objects.all()
    serializer_class = CateringRecetaSerializer
