from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from .forms import UserProfileForm, CustomRegisterForm, CompleteProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
from experimento.models import RegistroEnsayo, RegistroExperimentoCompleto
import csv
from django.http import HttpResponse
from datetime import datetime

def is_staff_user(user):
    return user.is_staff

class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'index.html')
        
        # Verificar si el usuario tiene un perfil completo
        if not hasattr(request.user, 'profile'):
            return redirect('complete_profile')
            
        if request.user.is_staff:
            return redirect('panel_admin')
        return redirect('usuario')

class UsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/inicio.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ExperimentoView(LoginRequiredMixin, TemplateView):
    template_name = 'experimento/iniciar.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class FinExperimentoView(LoginRequiredMixin, TemplateView):
    template_name = 'experimento/fin.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
@user_passes_test(is_staff_user, login_url='/usuario/')
def panel_admin(request):
    # Consultar el modelo que guarda los resultados completos del experimento
    todos_los_resultados = RegistroExperimentoCompleto.objects.all().order_by('-fecha', 'user__username') # Corregido: usar 'user' en lugar de 'usuario'
    
    context = {
        'resultados': todos_los_resultados
    }
    return render(request, 'authentication/results_panel.html', context)

@login_required
def descargar_resultados_csv(request):
    # Opcional: restringir a superusuarios
    # if not request.user.is_superuser:
    #     return HttpResponse("No tienes permiso para descargar estos datos.", status=403)

    # Crear la respuesta HTTP con la cabecera para CSV
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="resultados_experimentos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'},
    )
    response.write(u'\ufeff'.encode('utf8')) # BOM para compatibilidad con Excel en algunos casos

    # Crear un escritor CSV
    writer = csv.writer(response, delimiter=';') # Usar punto y coma como delimitador por si Excel lo prefiere

    # Escribir la fila de cabecera
    writer.writerow([
        'ID Registro',
        'ID Usuario',
        'Username',
        'Fecha',
        'Total Ensayos',
        'Respuestas Correctas',
        'Omisiones',
        'Respuestas Incorrectas',
        'Tiempo Reacción Promedio (ms)'
    ])

    # Obtener los datos de la base de datos
    resultados = RegistroExperimentoCompleto.objects.all().select_related('user').order_by('-fecha')

    # Escribir las filas de datos
    for r in resultados:
        writer.writerow([
            r.id,
            r.user.id,
            r.user.username,
            r.fecha.strftime("%Y-%m-%d %H:%M:%S"), # Formatear fecha
            r.total_ensayos,
            r.respuestas_correctas,
            r.omisiones,
            r.respuestas_incorrectas,
            f"{r.tiempo_reaccion_promedio:.2f}".replace('.', ',') if r.tiempo_reaccion_promedio is not None else 'N/A' # Formato numérico con coma
        ])

    return response

class CompleteProfileView(LoginRequiredMixin, View):
    template_name = 'authentication/complete_profile.html'

    def get(self, request):
        # Check if the profile already exists
        if hasattr(request.user, 'profile'):
            # Profile exists, maybe redirect home or show a message?
            # For now, let's redirect home as the original logic intended
            # You might want to allow users to *edit* their profile here later
            return redirect('home')

        # Profile doesn't exist, show the form to create it
        form = CompleteProfileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Try to get the existing profile, or create a new one if it doesn't exist
        # This handles both initial creation and potential future edits
        profile_instance = None
        if hasattr(request.user, 'profile'):
            profile_instance = request.user.profile
            
        form = CompleteProfileForm(request.POST, instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user # Ensure the profile is linked to the correct user
            profile.save()
            messages.success(request, 'Perfil completado/actualizado con éxito.')
            return redirect('home') # Redirect after successful completion/update
        
        # If form is not valid, re-render the page with the form and errors
        return render(request, self.template_name, {'form': form})

def registro(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            expediente = form.cleaned_data['expediente']
            password = form.cleaned_data['password1']

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo ya está registrado.')
            elif UserProfile.objects.filter(expediente=expediente).exists():
                form.add_error('expediente', 'Este número de expediente ya está registrado.')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre)
                UserProfile.objects.create(user=user, sex=sex, age=age, expediente=expediente)
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('iniciosesion')
    else:
        form = CustomRegisterForm()  
        return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al usuario a la página principal
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')
    return render(request, 'iniciosesion.html')  # Maneja solicitudes GET y muestra el formulario
