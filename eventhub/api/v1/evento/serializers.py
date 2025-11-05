from rest_framework import serializers
from .models import Evento, Asistente, Comentario
from django.contrib.auth.models import User

# Serializador del Asistente (para listar en el evento)
class AsistenteSerializer(serializers.ModelSerializer):
    # Muestra el nombre del usuario en lugar del ID
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Asistente
        fields = ('id', 'usuario', 'nombre_completo', 'fecha_registro')
        read_only_fields = ('usuario', 'fecha_registro') # El usuario se asigna en la vista

    def get_nombre_completo(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name} ({obj.usuario.username})"


# Serializador para el Comentario
class ComentarioSerializer(serializers.ModelSerializer):
    autor_username = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = Comentario
        fields = ('id', 'evento', 'autor', 'autor_username', 'contenido', 'puntuacion', 'creado_en')
        read_only_fields = ('evento', 'autor', 'creado_en')


# Serializador principal de Evento
class EventoSerializer(serializers.ModelSerializer):
    organizador_username = serializers.ReadOnlyField(source='organizador.username')

    class Meta:
        model = Evento
        fields = ('id', 'nombre', 'fecha', 'descripcion', 'organizador', 'organizador_username', 'creado_en')
        read_only_fields = ('organizador',)

# Serializador para actualización parcial de Evento
class EventoPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        # Solo los campos permitidos en la actualización parcial (Req. 4)
        fields = ('nombre', 'fecha')
        extra_kwargs = {
            'nombre': {'required': False},
            'fecha': {'required': False},
        }

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        # Garantizamos que el email y username son únicos
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # Es CRÍTICO usar create_user para hashear la contraseña
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user