from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_experimento, name='experimento'),
    path('guardar/', views.guardar_resultado, name='guardar_resultado'),
    path('resultados/', views.ver_resultados, name='ver_resultados'),
    path('descargar/', views.descargar_csv, name='descargar_csv'),
]
