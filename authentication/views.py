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
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('panel_admin')
        return super().get(request, *args, **kwargs)

class ExperimentoView(LoginRequiredMixin, TemplateView):
    template_name = 'experimento/iniciar.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('panel_admin')
        return super().get(request, *args, **kwargs)

class FinExperimentoView(LoginRequiredMixin, TemplateView):
    template_name = 'experimento/fin.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('panel_admin')
        return super().get(request, *args, **kwargs)

@login_required
@user_passes_test(is_staff_user, login_url='/usuario/')
def panel_admin(request):
    return render(request, 'admin/experimento/panel_admin.html')

class CompleteProfileView(View):
    def get(self, request):
        # Verificar si el perfil ya está completo
        if request.user.is_authenticated and request.user.perfil_completo:
            return redirect('home')  # Redirige a la página principal si el perfil está completo

        # Mostrar el formulario para completar el perfil
        form = CompleteProfileForm()
        return render(request, 'authentication/complete_profile.html', {'form': form})

    def post(self, request):
        form = CompleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.perfil_completo = True  # Marcar el perfil como completo
            usuario.save()
            return redirect('home')  # Redirige a la página principal después de completar el perfil
        return render(request, 'authentication/complete_profile.html', {'form': form})

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



