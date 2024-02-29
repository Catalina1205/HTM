from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.core.cache import cache
from django.db import connection

from django.contrib.auth.models import User
from htmdjango1.models import Perfil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                print(f"Usuario autenticado: {request.user.username}")
                print(f"Grupos del usuario: {request.user.groups.all()}")
                
                if request.user.groups.filter(name=group_name).exists():
                    print(f"El usuario pertenece al grupo {group_name}")
                    return view_func(request, *args, **kwargs)
                else:
                    print(f"El usuario NO pertenece al grupo {group_name}")
            else:
                print("Usuario no autenticado")
                
            return redirect('/errorpagina')  # Cambia 'ruta_de_redireccion' según tu configuración
        return wrapper
    return decorator



def errorpagina(request):
    return render(request, 'Inc/errorpagina.html')

# Cargas estáticas ↓

def inicioIN(request):
    return render(request, 'INICIO/inicioIN.html')

# Usuario administrador ↓
@group_required('RRHH')
@login_required
def inicioUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UA/inicioUA.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})
    
# InicioPosIniciosesionUF   
def inicio (request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        return render(request, 'UF/inicio.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    else: 
        return redirect('/inicioSesion')

def logoutusuario (request):
    logout(request)
    return redirect('/inicioSesion')

