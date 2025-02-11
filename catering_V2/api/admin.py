from django.contrib import admin
from .models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "message", "created_at")  # Reemplaza 'timestamp' por 'created_at'

admin.site.register(ChatMessage, ChatMessageAdmin)
