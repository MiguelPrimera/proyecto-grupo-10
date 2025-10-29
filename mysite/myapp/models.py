from django.db import models
from datetime import time

# Create your models here.

class Publicacion(models.Model):
    OPCIONES = [
        ('op1', 'Opción 1'),
        ('op2', 'Opción 2'),
        ('op3', 'Opción 3'),
    ]
    
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    opcion = models.CharField(max_length=10, choices=OPCIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


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
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

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
    


