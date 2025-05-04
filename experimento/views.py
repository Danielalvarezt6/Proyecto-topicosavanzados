from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import RegistroEnsayo
import csv

def vista_experimento(request):
    return render(request, 'experimento/experimento.html')

def guardar_resultado(request):
    if request.method == 'POST':
        datos = request.POST
        RegistroEnsayo.objects.create(
            numero_ensayo=datos['numero_ensayo'],
            presiono_a=datos['presiono_a'] == 'true',
            tiempo_reaccion=float(datos['tiempo_reaccion']) if datos['tiempo_reaccion'] else None,
            hubo_estimulo_negativo=datos['hubo_estimulo_negativo'] == 'true',
        )
        return JsonResponse({'estado': 'ok'})
    return JsonResponse({'estado': 'error'}, status=400)

def ver_resultados(request):
    resultados = RegistroEnsayo.objects.all().order_by('fecha')
    return render(request, 'experimento/resultados.html', {'resultados': resultados})

def descargar_csv(request):
    respuesta = HttpResponse(content_type='text/csv')
    respuesta['Content-Disposition'] = 'attachment; filename="resultados_experimento.csv"'

    escritor = csv.writer(respuesta)
    escritor.writerow(['Ensayo', 'Presionó A', 'Tiempo de Reacción', 'Hubo Estímulo Negativo', 'Fecha'])

    for registro in RegistroEnsayo.objects.all():
        escritor.writerow([
            registro.numero_ensayo,
            'Sí' if registro.presiono_a else 'No',
            registro.tiempo_reaccion if registro.tiempo_reaccion is not None else '',
            'Sí' if registro.hubo_estimulo_negativo else 'No',
            registro.fecha.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return respuesta
