from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# El modelo de Evento 
class Evento(models.Model):
    
    nombre = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# El modelo de Asistente 
class Asistente(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='asistentes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asistencias')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un usuario solo puede ser asistente una vez por evento.
        unique_together = ('evento', 'usuario')
        ordering = ['usuario__first_name', 'usuario__last_name'] 

    def __str__(self):
        return f"{self.usuario.username} se registra en {self.evento.nombre}"

# El modelo de Comentario/Reseña 
class Comentario(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_realizados')
    contenido = models.TextField()
    puntuacion = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Puntuación de 1 a 5, si aplica como reseña"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.evento.nombre}"