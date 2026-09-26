"""
URL configuration for STAP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path
from Atencion.views import crear_o_editar_paciente,consultar_paciente
from Atencion.views import ingresos_pacientes,generar_html,reportes,descargar_archivo_seguro,generar_token_seguro,rips
from Atencion.views import (ingreso_pacientes,consultar_paciente_ingreso,ingresos_pacientes_tabla,obtener_ingreso,historias_clinicas,historias_clinicas_tabla,adjuntar_archivo,login_view, register_view,home_view,logout_view,custom_404_view,consulta_usuario,crear_o_editar_facturas)
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('historias/', historias_clinicas, name='historias_clinicas'),
    path('historias_tabla/', historias_clinicas_tabla, name='historias_clinicas_tabla'),





