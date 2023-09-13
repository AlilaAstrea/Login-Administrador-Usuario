"""
URL configuration for Eva3 project.

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
from django.contrib import admin
from django.urls import path

from biblioteca import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrarIndex),  #check 

##---------------------Api Rest Eva4-----------------------------------##
    path('biblioteca_json/', views.obtenerBibliotecas), #check 
    path("usuario_json/", views.obtenerUsuarios), #check 

    path('biblioteca/', views.biblioteca_list), #check 
    path('biblioteca/<int:id>', views.biblioteca_detail), #check 

    path('usuario/', views.usuario_list), #check 
    path('usuario/<int:id>', views.usuario_detail), #check 

##---------------------------------------------------------------------##
    path('login', views.iniciarSesion), #check
    path('logout', views.cerrarSesion), #check

##---------------------------------------------------------------------##
    path('menu_admin', views.mostrarMenuAdmin), #check

    path('form_registro_idiomas', views.mostrarFormRegistroIdiomas), #check
    path('form_registro_generos', views.mostrarFormRegistroGeneros), #check

    path('registrar_idioma', views.registrarIdioma), #check
    path('registrar_genero', views.registrarGenero), #check

    path('form_modificar_idioma/<int:id>', views.mostrarFormModificarIdioma), #check
    path('form_modificar_genero/<int:id>', views.mostrarFormModificarGenero), #check

    path('modificar_idioma/<int:id>', views.actualizarIdioma), #check
    path('modificar_genero/<int:id>', views.actualizarGenero), #check

    path('eliminar_idioma/<int:id>', views.eliminarIdioma), #check
    path('eliminar_genero/<int:id>', views.eliminarGenero), #check

##---------------------------------------------------------------------##

    path('listar_historial', views.mostrarListarHistorial), #check

##---------------------------------------------------------------------##
##---------------------------------------------------------------------##

    path('menu_usuario', views.mostrarMenuUsuario), #check

    path('form_registrar', views.mostrarFormRegistrar), #check
    path('registrar', views.registrarBiblioteca), #check

    path('listado', views.mostrarListado), #check

    path('editar/<int:id>', views.mostrarFormActualizar), #check
    path('actualizar/<int:id>', views.actualizarBiblioteca), #check

    path('eliminar/<int:id>', views.eliminarBiblioteca), #check
] 
