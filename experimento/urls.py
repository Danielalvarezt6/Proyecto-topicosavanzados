from django.urls import path
from . import views

app_name = 'experimento'

urlpatterns = [
    path('', views.vista_experimento, name='vista_experimento'),
    path('guardar/', views.guardar_resultado, name='guardar_resultado'),
    path('guardar_completo/', views.guardar_resultado_completo, name='guardar_resultado_completo'),
    path('resultados/', views.ver_resultados, name='ver_resultados'),
    path('descargar/', views.descargar_csv, name='descargar_csv'),
]
