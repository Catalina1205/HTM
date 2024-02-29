from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.core.cache import cache
from django.db import connection

from htmdjango1.models import Perfil, Empleado


def registropaso1(request):    
    if request.method == 'POST':
        correo = request.POST.get('correo2')
        request.session['correoUsuario'] = correo  # Guarda el correo en la sesión
        print (request.session['correoUsuario'])
        return redirect('/registropaso2')
    else:
        return render(request, 'registropaso1.html')


def registropaso2(request):
    if request.method == 'POST':
        if request.POST.get('codigo'):
            return redirect ('/registropaso3')
        else:
            messages.error(request, 'Debes ingresar un código')
    return render(request, 'registropaso2.html')



from django.contrib.auth.models import User, Group

def pagina(request):
    correo = request.session.get('correoUsuario')

    if request.method == "POST":
        if (
            request.POST.get('nombre') and request.POST.get('apellido') and
            request.POST.get('lista') and request.POST.get('numero') and
            request.POST.get('numeroCelular') and request.POST.get('numeroTelefono') and
            request.POST.get('password2') and request.POST.get('fecha') and
            request.POST.get('edad') and request.POST.get('genero') and
            request.POST.get('cargo') and request.POST.get('area') and
            request.POST.get('eps')
         ):
            # Creación del usuario
            user = User.objects.create_user(
                username=request.POST.get('nombre'),
                password=request.POST.get('password2'),
                email=correo,
                first_name=request.POST.get('nombre'),
                last_name=request.POST.get('apellido'),
            )
            
            # Perfil asociado al usuario
            perfil = Perfil.objects.create(
                user=user,
                tipo_documento=request.POST.get('lista'),
                documento=request.POST.get('numero'),
                numero_cel=request.POST.get('numeroCelular'),
                numero_tel=request.POST.get('numeroTelefono'),
                fecha_nacimiento=request.POST.get('fecha'),
                edad=request.POST.get('edad'),
                genero=request.POST.get('genero'),
                cargo=request.POST.get('cargo'),
                area=request.POST.get('area'),
                eps=request.POST.get('eps')
            )

            # Asigna al grupo RRHH si el área es RRHH o a Empleados si el area es diferente a ésta
            area = request.POST.get('area')
            if area == "RRHH":
                rrhh_group, created = Group.objects.get_or_create(name='RRHH')
                user.groups.add(rrhh_group)
            else:
                empleados_group, created = Group.objects.get_or_create(name='Empleados')
                user.groups.add(empleados_group)
                

            return redirect('/inicioSesion')

    else:
        unempleado = Empleado.objects.using('empresa_db').filter(correo=correo)
        return render(request, 'registropaso3.html', {'correo': correo, 'unempleado': unempleado})
    







"""
from htmdjango1.models import Usuarios, Eps


# Cargas estáticas ↓

def inicioIN(request):
    return render(request, 'INICIO/inicioIN.html')

# Usuario administrador ↓
def inicioUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UA/inicioUA.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})
    
# InicioPosIniciosesionUF   
def inicio (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/inicio.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

""" 


