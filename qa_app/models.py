# qa_app/models.py
from django.db import models

class ChatMessage(models.Model):
    # Rename user_id to room_id to avoid the "user_id_id" error
    room_id = models.CharField(max_length=255) 
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
