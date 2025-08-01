from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

class QuestionAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    embedding = models.JSONField()
    
    def __str__(self):
        return self.question[:50]
    

class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.session_id)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{'User' if self.is_user else 'Bot'} : {self.text[:50]}"
    
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    sucursal = models.CharField(max_length=100)
    
    def __str__(self):
        return f"usuario {self.id} - Sucursal {self.sucursal}"


class UsuarioMensaje(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.ForeignKey(Message, on_delete=models.CASCADE)
    fecha_asociacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario} <> {self.mensaje}"