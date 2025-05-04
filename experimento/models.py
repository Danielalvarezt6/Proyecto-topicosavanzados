from django.db import models

from django.db import models

class RegistroEnsayo(models.Model):
    numero_ensayo = models.IntegerField()
    presiono_a = models.BooleanField()
    tiempo_reaccion = models.FloatField(null=True, blank=True)  # en segundos
    hubo_estimulo_negativo = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ensayo {self.numero_ensayo} - {'Evitó' if self.presiono_a else 'No evitó'}"

