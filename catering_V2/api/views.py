import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from django.middleware.csrf import get_token
from django.conf import settings  # Para obtener la API key de OpenAI
import openai  # Librería de OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from calculos.models import Ingrediente
from .models import ChatMessage  # Importa el modelo de historial de chat


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai  # Asegúrate de que openai está instalado
from .models import ChatMessage

class GPTInteractionView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "")

        if not user_message:
            return Response({"error": "No se recibió ningún mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Llamada a OpenAI
            #openai.api_key = "TU_API_KEY_AQUÍ"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}]
            )
            gpt_response = response['choices'][0]['message']['content']

            # Guardar mensaje en la base de datos
            ChatMessage.objects.create(sender="user", message=user_message)
            ChatMessage.objects.create(sender="bot", message=gpt_response)

            return Response({"user_message": user_message, "gpt_response": gpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




### VISTA PARA EL CHATBOT (RENDERIZA HTML) ###
def chatbot_view(request):
    """Renderiza la página del chatbot con el token CSRF"""
    csrf_token = get_token(request)
    return render(request, 'api/chatbot.html', {"csrf_token": csrf_token})


### ENDPOINT PARA CREAR INGREDIENTES ###


@csrf_exempt  # Esto permite que reciba POST sin problemas de CSRF
def crear_ingrediente(request):
    """
    Crea un ingrediente en la base de datos de Django.
    """
    if request.method == "POST":  # Verifica que es una solicitud POST
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
                nombre=nombre, marca=marca, cantidad=cantidad, unidad=unidad, precio=precio
            )

            return JsonResponse({"message": "Ingrediente creado correctamente"}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Error al crear ingrediente: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)  # Solo acepta POST



###  ENDPOINT PARA GPT QUE CONSULTA LA BASE DE DATOS ###
class GPTDatabaseInteractionView(APIView):
    """
    Endpoint que consulta la base de datos de ingredientes y envía la información a OpenAI
    para que sugiera recetas o consejos.
    """
    def post(self, request):
        # Obtener mensaje del usuario
        user_message = request.data.get("message", "")

        if not user_message:
            return Response({"error": "No se recibió ningún mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener ingredientes de la base de datos
            ingredientes = Ingrediente.objects.all().values("nombre", "cantidad", "unidad", "precio")

            # Formatear los ingredientes en texto para OpenAI
            ingredientes_texto = "\n".join([
                f"{ing['nombre']}: {ing['cantidad']} {ing['unidad']} - ${ing['precio']}"
                for ing in ingredientes
            ])

            # Crear el prompt para OpenAI
            prompt = f"""Tienes los siguientes ingredientes disponibles:
            {ingredientes_texto}
            Usuario pregunta: {user_message}
            Responde con una sugerencia de recetas o consejos de uso."""

            # Llamar a OpenAI
            openai.api_key = settings.OPENAI_API_KEY  # Asegurar que la API key está en settings.py
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            gpt_response = response['choices'][0]['message']['content']

            # Guardar interacción en la base de datos
            ChatMessage.objects.create(sender="user", message=user_message)
            ChatMessage.objects.create(sender="bot", message=gpt_response)

            return Response({
                "user_message": user_message,
                "gpt_response": gpt_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from django.shortcuts import render
from django.middleware.csrf import get_token

def chatbot_view(request):
    csrf_token = get_token(request)  # Genera el token CSRF
    return render(request, 'api/chatbot.html', {"csrf_token": csrf_token})

