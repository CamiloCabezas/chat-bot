from django.urls import path
from .views import CargarembeddingsMasivos, ResponderMesanjes   # Asegúrate de importar tu view

urlpatterns = [
    path('api/cargar-embeddings/', CargarembeddingsMasivos.as_view(), name='cargar_embeddings'),
    path("api/pregunta-resuelta/", ResponderMesanjes.as_view(), name="responder_pregunta")
]