import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import ChatMessage  # Importa el modelo

def chatbot_view(request):
    return render(request, 'api/chatbot.html')


@csrf_exempt
def enviar_mensaje_a_rasa(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_message = body.get("message")

            if not user_message:
                return JsonResponse({"error": "No se recibió ningún mensaje"}, status=400)

            # Guardar mensaje del usuario
            try:
                ChatMessage.objects.create(sender="user", message=user_message)
            except Exception as e:
                return JsonResponse({"error": f"Error al guardar mensaje: {str(e)}"}, status=500)

            # Enviar mensaje a Rasa
            rasa_response = requests.post(
                "http://localhost:5005/webhooks/rest/webhook",
                json={"sender": "user", "message": user_message},
            )

            if rasa_response.status_code == 200:
                responses = rasa_response.json()
                bot_responses = []

                for response in responses:
                    if "text" in response:
                        bot_responses.append({"text": response["text"]})
                        # Guardar respuesta del bot
                        ChatMessage.objects.create(sender="bot", message=response["text"])

                return JsonResponse(bot_responses, safe=False, status=200)

            return JsonResponse({"error": "Error al conectar con Rasa"}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)



'''
@csrf_exempt
def enviar_mensaje_a_rasa(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_message = body.get("message")

            if not user_message:
                return JsonResponse({"error": "No se recibió ningún mensaje"}, status=400)

            # Enviar mensaje al servidor de Rasa
            rasa_response = requests.post(
                "http://localhost:5005/webhooks/rest/webhook",
                json={"sender": "user", "message": user_message},
            )

            # Procesar la respuesta de Rasa
            if rasa_response.status_code == 200:
                responses = rasa_response.json()
                bot_responses = []

                for response in responses:
                    response_data = {}
                    if "text" in response:
                        response_data["text"] = response["text"]
                    if "image" in response:
                        response_data["image"] = response["image"]
                    bot_responses.append(response_data)

                return JsonResponse(bot_responses, safe=False, status=200)

            else:
                return JsonResponse({"error": "Error al conectar con Rasa"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
'''

from django.http import JsonResponse
from .models import ChatMessage

def obtener_mensajes_guardados(request):
    if request.method == "GET":
        mensajes = ChatMessage.objects.order_by('-timestamp')  # Orden por tiempo
        datos = [{"sender": mensaje.sender, "message": mensaje.message, "timestamp": mensaje.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for mensaje in mensajes]
        return JsonResponse(datos, safe=False)

from django.http import JsonResponse
from calculos.models import Ingrediente




def crear_ingrediente(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ingrediente = Ingrediente.objects.create(
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            precio=data["precio"]
        )
        return JsonResponse({"message": "Ingrediente creado"}, status=201)

