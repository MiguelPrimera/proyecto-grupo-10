from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dia(models.Model):
    nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre


class Piso(models.Model):
    numero = models.IntegerField(unique=True)

    def __str__(self):
        return f"Piso {self.numero}"


class Sala(models.Model):
    nombre = models.CharField(max_length=10)
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, related_name="salas")

    def __str__(self):
        return f"Sala {self.nombre} - Piso {self.piso.numero}"


class Bloque(models.Model):
    nombre = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.nombre


class Disponibilidad(models.Model):
    dia = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name="disponibilidades")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="disponibilidades")
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name="disponibilidades")
    estado = models.CharField(max_length=10, choices=[("Libre", "Libre"), ("Ocupada", "Ocupada")])

    class Meta:
        unique_together = ("dia", "sala", "bloque")

    def __str__(self):
        return f"{self.sala} - {self.dia} - {self.bloque}: {self.estado}"

class Publicaciones(models.Model):

    titulo = models.CharField(max_length=100)
    contenido = models.TextField(max_length=700)
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE, related_name='publicaciones')
    cupos_maximos = models.PositiveIntegerField(default=1)
    cupos_disponibles = models.PositiveIntegerField(editable=False)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cupos_disponibles = self.cupos_maximos
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class UnionGrupo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE, related_name='participantes')

    class Meta:
        unique_together = ('usuario', 'publicacion')

    def __str__(self):
        return f"{self.usuario.username} → {self.publicacion.titulo}"