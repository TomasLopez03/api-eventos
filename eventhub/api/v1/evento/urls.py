from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventoViewSet,
    AsistenteListView,
    AsistenteCreateView,
    ComentarioListView,
    ComentarioCreateView,
    UserRegisterView
)

# Router para los recursos principales de Evento
router = DefaultRouter()
router.register(r'v1/eventos', EventoViewSet, basename='evento')

urlpatterns = [
    # Rutas principales de Evento
    path('', include(router.urls)),

    path('v1/usuarios/registro', UserRegisterView.as_view(), name='user-register'),
    # Recursos Anidados de Asistentes (Req. 6, 8)
    # GET /v1/eventos/{id}/asistentes
    path('v1/eventos/<int:evento_pk>/asistentes', AsistenteListView.as_view(), name='asistente-list'),
    # POST /v1/eventos/{id}/asistentes
    path('v1/eventos/<int:evento_pk>/asistentes/registro', AsistenteCreateView.as_view(), name='asistente-registro'),

    # Recursos Anidados de Comentarios (Req. 7, 9)
    # GET /v1/eventos/{id}/comentarios
    path('v1/eventos/<int:evento_pk>/comentarios', ComentarioListView.as_view(), name='comentario-list'),
    # POST /v1/eventos/{id}/comentarios
    path('v1/eventos/<int:evento_pk>/comentarios/crear', ComentarioCreateView.as_view(), name='comentario-crear'),
]