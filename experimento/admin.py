from django.contrib import admin
# Importar los modelos de la app experimento
from .models import RegistroExperimentoCompleto

# Register your models here.

# Registrar el modelo para que aparezca en el admin
admin.site.register(RegistroExperimentoCompleto)
