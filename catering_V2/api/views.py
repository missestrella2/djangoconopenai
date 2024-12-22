import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


def chatbot_view(request):
    return render(request, 'api/chatbot.html')

#@csrf_exempt

def enviar_mensaje_a_rasa(request):
    if request.method == "POST":
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
