"""
URL configuration for NeuroDots project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import HomeView, UsuarioView, ExperimentoView, FinExperimentoView, panel_admin, CompleteProfileView, registro
from experimento import views  # Asegúrate de importar views desde la app correspondiente

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# Asegúrate de tener esta importación al principio del archivo
from authentication.views import iniciar_sesion, panel_admin # Agrega iniciar_sesion si no está

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('usuario/', UsuarioView.as_view(), name='usuario'),
    path('experimento/', views.vista_experimento, name='experimento_iniciar'),
    path('experimento/fin/', FinExperimentoView.as_view(), name='experimento_fin'),
    # CORRECTO: Usa la vista 'iniciar_sesion' que maneja GET y POST
    path('iniciosesion/', iniciar_sesion, name='iniciosesion'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('panel-admin/', panel_admin, name='panel_admin'),
    path('registro/', registro, name='registro'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
