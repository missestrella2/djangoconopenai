"""
URL configuration for catering_V2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin
from calculos import views  # Importa las vistas de la aplicación "calculos"
from .views import politica_privacidad  # Si la vista está en 'catering/views.py'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculos/', include('calculos.urls')),
    #path('', RedirectView.as_view(url='/calculos/', permanent=False)),  # Redirige la raíz a /calculos/
    path('', views.home),  # La vista home renderizará la plantilla home.html
    #path('calculos/calcular/', views.calcular_catering, name='calcular_catering'),
    path('calculos/', views.home_calculos, name='home_calculos'),  # Nueva ruta para /calculos/
    path('api/', include('api.urls')),
    path('politica-de-privacidad/', politica_privacidad, name='politica_privacidad'),
]




