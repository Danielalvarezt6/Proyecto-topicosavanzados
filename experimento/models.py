from django.db import models
from django.contrib.auth.models import User

class RegistroEnsayo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_ensayo = models.IntegerField()
    presiono_a = models.BooleanField()
    tiempo_reaccion = models.FloatField(null=True, blank=True)  # en segundos
    hubo_estimulo_negativo = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ensayo {self.numero_ensayo} por {self.user.username} - {'Evitó' if self.presiono_a else 'No evitó'}"

# Nuevo modelo para el experimento completo
class RegistroExperimentoCompleto(models.Model):
    FASE_CHOICES = [
        ('Pavloviana', 'Fase Pavloviana'),
        ('Instrumental', 'Fase Instrumental'),
        ('Extincion', 'Fase Extinción'),
    ]
    ESTIMULO_CHOICES = [
        ('triangulo', 'Triángulo'),
        ('cuadrado', 'Cuadrado'),
    ]
    RESPUESTA_CHOICES = [
        ('tecla_espacio', 'Tecla Espacio'),
        ('timeout', 'Timeout'),
    ]
    CONSECUENCIA_CHOICES = [
        ('sonido_aversivo', 'Sonido Aversivo'),
        ('sonido_neutro', 'Sonido Neutro'),
        ('ninguna', 'Ninguna'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fase = models.CharField(max_length=15, choices=FASE_CHOICES)
    numero_ensayo = models.IntegerField()
    estimulo = models.CharField(max_length=10, choices=ESTIMULO_CHOICES)
    respuesta = models.CharField(max_length=15, choices=RESPUESTA_CHOICES)
    tiempo_reaccion_ms = models.FloatField(null=True, blank=True) # Store in milliseconds
    consecuencia = models.CharField(max_length=20, choices=CONSECUENCIA_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Ensayo {self.numero_ensayo} ({self.fase}) - {self.estimulo} -> {self.respuesta}"
