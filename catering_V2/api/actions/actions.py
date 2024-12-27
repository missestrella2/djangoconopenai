# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionElegirOpcion(Action):
    def name(self):
        return "action_elegir_opcion"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text').lower()

        if "ingrediente" in user_message:
            dispatcher.utter_message(text="Entendido. Vamos a agregar un ingrediente. ¿Cómo se llama?")
            return [SlotSet("opcion", "ingrediente")]
        elif "receta" in user_message:
            dispatcher.utter_message(text="Perfecto. Vamos a registrar una receta. ¿Cuál es el nombre de la receta?")
            return [SlotSet("opcion", "receta")]
        elif "catering" in user_message:
            dispatcher.utter_message(text="Muy bien. Empecemos a crear un catering. ¿Cómo se llamará?")
            return [SlotSet("opcion", "catering")]
        else:
            dispatcher.utter_message(text="Lo siento, no entendí. Por favor elige entre las opciones disponibles.")
            return []


from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import requests

class ActionGuardarIngrediente(Action):
    def name(self):
        return "action_guardar_ingrediente"

    def run(self, dispatcher, tracker, domain):
        nombre = tracker.get_slot("nombre_ingrediente")
        cantidad = tracker.get_slot("cantidad")
        precio = tracker.get_slot("precio")

        # Enviar datos al backend de Django
        response = requests.post(
            "http://127.0.0.1:8000/api/ingredientes/",
            json={"nombre": nombre, "cantidad": cantidad, "precio": precio}
        )

        if response.status_code == 201:
            dispatcher.utter_message(
                text=f"Ingrediente guardado con éxito: {nombre}, {cantidad}, ${precio}."
            )
        else:
            dispatcher.utter_message(
                text="Hubo un problema al guardar el ingrediente. Inténtalo de nuevo."
            )

        return []


