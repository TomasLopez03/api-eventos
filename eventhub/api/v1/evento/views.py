from rest_framework import viewsets, mixins, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .models import Evento, Asistente, Comentario
from .serializers import EventoSerializer, EventoPatchSerializer, AsistenteSerializer, ComentarioSerializer, UserSerializer
from .permissions import IsOrganizerOrReadOnly 

# Paginación personalizada 
from rest_framework.pagination import LimitOffsetPagination
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10 
    max_limit = 50

# Paginación para listados grandes
from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100



class EventoViewSet(viewsets.ModelViewSet):
    """
    Gestiona la lista, creación, detalle, actualización y eliminación de eventos.
    - GET /v1/eventos: Lista de todos los eventos (Req. 1).
    - POST /v1/eventos: Crea un nuevo evento (Req. 2).
    - GET /v1/eventos/42: Detalle de un evento específico (Req. 3).
    - PATCH /v1/eventos/42: Actualización parcial (Req. 4).
    - DELETE /v1/eventos/42: Eliminación de un evento (Req. 5, 11).
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # Permisos: Leer libremente, solo autenticados pueden crear,
    # solo el organizador puede editar/eliminar (Necesita el permiso IsOrganizerOrReadOnly)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options'] # Limita los métodos


    # Asigna automáticamente el usuario autenticado como 'organizador' al crear
    def perform_create(self, serializer):
        serializer.save(organizador=self.request.user)

    # Usa un serializer específico para el PATCH para documentación de drf-spectacular 
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return EventoPatchSerializer
        return EventoSerializer


#Obtener todos los asistentes
class AsistenteListView(generics.ListAPIView):
    """
    Lista todos los asistentes registrados para un evento específico.
    """
    serializer_class = AsistenteSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden ver la lista
    pagination_class = StandardResultsSetPagination # Paginación estándar

    # Filtrado y ordenamiento por nombre 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario'] 

    def get_queryset(self):
        # Filtra los asistentes por el ID del evento en la URL
        evento_id = self.kwargs['evento_pk']
        return Asistente.objects.filter(evento_id=evento_id).select_related('usuario')


#Registrar un nuevo asistente
class AsistenteCreateView(generics.CreateAPIView):
    """
    Registra al usuario actual como asistente para un evento.
    """
    serializer_class = AsistenteSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden registrarse

    def post(self, request, *args, **kwargs):
        evento_id = self.kwargs['evento_pk']
        user = request.user

        # Evitar doble registro
        if Asistente.objects.filter(evento_id=evento_id, usuario=user).exists():
            return Response(
                {"detail": "Ya estás registrado como asistente para este evento."},
                status=status.HTTP_409_CONFLICT # 409 Conflict es un buen código para esto
            )

        try:
            evento = Evento.objects.get(pk=evento_id)
        except Evento.DoesNotExist:
            # En caso de que el evento no exista 
            return Response(
                {"detail": "Evento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Crea el objeto Asistente
        Asistente.objects.create(evento=evento, usuario=user)
        # Retorna 201 Created con el detalle
        return Response(
            {"detail": "Registro de asistencia exitoso."},
            status=status.HTTP_201_CREATED
        )


#Obtener comentarios
class ComentarioListView(generics.ListAPIView):
    """
    Lista todos los comentarios para un evento específico, con paginación limite/offset.
    """
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Se permite la lectura pública
    pagination_class = CustomLimitOffsetPagination 

    def get_queryset(self):
        # Filtra los comentarios por el ID del evento en la URL
        evento_id = self.kwargs['evento_pk']
        return Comentario.objects.filter(evento_id=evento_id).select_related('autor')


# Crear un comentario
class ComentarioCreateView(generics.CreateAPIView):
    """
    Crea un nuevo comentario para un evento específico.
    """
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden comentar

    def perform_create(self, serializer):
        evento_id = self.kwargs['evento_pk']
        try:
            evento = Evento.objects.get(pk=evento_id)
        except Evento.DoesNotExist:
            raise Response(
                {"detail": "Evento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        # Asigna el evento de la URL y el usuario autenticado
        serializer.save(evento=evento, autor=self.request.user)


class UserRegisterView(generics.CreateAPIView):
    """
    Permite el registro de nuevos usuarios en el sistema.
    Endpoint: /api/v1/usuarios/registro
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # CUALQUIER persona puede registrarse, incluso sin token
    permission_classes = [AllowAny]