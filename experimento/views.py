from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import RegistroEnsayo, RegistroExperimentoCompleto
import csv
from django.contrib.auth.decorators import login_required

@login_required
def vista_experimento(request):
    return render(request, 'experimento/experimento.html')

@login_required
def guardar_resultado(request):
    if request.method == 'POST':
        datos = request.POST
        RegistroEnsayo.objects.create(
            user=request.user,
            numero_ensayo=datos['numero_ensayo'],
            presiono_a=datos['presiono_a'] == 'true',
            tiempo_reaccion=float(datos['tiempo_reaccion']) if datos['tiempo_reaccion'] else None,
            hubo_estimulo_negativo=datos['hubo_estimulo_negativo'] == 'true',
        )
        return JsonResponse({'estado': 'ok'})
    return JsonResponse({'estado': 'error'}, status=400)

@login_required
def ver_resultados(request):
    resultados = RegistroEnsayo.objects.filter(user=request.user).order_by('fecha')
    return render(request, 'experimento/resultados.html', {'resultados': resultados})

@login_required
def descargar_csv(request):
    respuesta = HttpResponse(content_type='text/csv')
    
    if request.user.is_staff:
        # Admin downloads all results
        resultados = RegistroEnsayo.objects.all().order_by('user__username', 'fecha')
        filename = f'resultados_experimento_TODOS_{request.user.username}.csv'
        headers = ['Usuario', 'Expediente', 'Ensayo', 'Presionó A', 'Tiempo de Reacción', 'Hubo Estímulo Negativo', 'Fecha']
    else:
        # Regular user downloads their own results
        resultados = RegistroEnsayo.objects.filter(user=request.user).order_by('fecha')
        filename = f'resultados_experimento_{request.user.username}.csv'
        headers = ['Ensayo', 'Presionó A', 'Tiempo de Reacción', 'Hubo Estímulo Negativo', 'Fecha']
        
    respuesta['Content-Disposition'] = f'attachment; filename="{filename}"'

    escritor = csv.writer(respuesta)
    escritor.writerow(headers)

    for registro in resultados:
        row_data = [
            registro.numero_ensayo,
            'Sí' if registro.presiono_a else 'No',
            registro.tiempo_reaccion if registro.tiempo_reaccion is not None else '',
            'Sí' if registro.hubo_estimulo_negativo else 'No',
            registro.fecha.strftime('%Y-%m-%d %H:%M:%S')
        ]
        if request.user.is_staff:
            # Add user info for admin download
            expediente = registro.user.profile.expediente if hasattr(registro.user, 'profile') else 'N/A'
            row_data.insert(0, expediente) # Insert expediente at index 1
            row_data.insert(0, registro.user.username) # Insert username at index 0
            
        escritor.writerow(row_data)
        
    return respuesta

@login_required
def guardar_resultado_completo(request):
    if request.method == 'POST':
        datos = request.POST
        try:
            # Convert tiempo_reaccion_ms, handle None if empty or not provided
            tiempo_ms = None
            if datos.get('tiempo_reaccion_ms') and datos['tiempo_reaccion_ms'] != 'null':
                 # Check if it's a valid number before converting
                try:
                    tiempo_ms = float(datos['tiempo_reaccion_ms'])
                except ValueError:
                    print(f"Warning: Invalid float value for tiempo_reaccion_ms: {datos.get('tiempo_reaccion_ms')}")
                    # Decide how to handle invalid float - set to None or raise error? Set to None for now.
                    tiempo_ms = None

            RegistroExperimentoCompleto.objects.create(
                user=request.user,
                fase=datos.get('fase', 'Desconocida'), # Provide default if missing
                numero_ensayo=int(datos.get('numero_ensayo', 0)), # Provide default/handle error
                estimulo=datos.get('estimulo', 'desconocido'),
                respuesta=datos.get('respuesta', 'desconocida'),
                tiempo_reaccion_ms=tiempo_ms,
                consecuencia=datos.get('consecuencia', 'desconocida')
            )
            return JsonResponse({'estado': 'ok', 'message': 'Resultado completo guardado.'})
        except Exception as e:
            # Log the error for debugging
            print(f"Error al guardar resultado completo: {e}")
            print(f"Datos recibidos: {datos}")
            return JsonResponse({'estado': 'error', 'message': str(e)}, status=500)
    # Return error if not POST
    return JsonResponse({'estado': 'error', 'message': 'Método no permitido.'}, status=405)
