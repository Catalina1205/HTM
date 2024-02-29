from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.core.cache import cache
from django.db import connection
from htmdjango1.models import Perfil
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ConfigurarPerfil




def inicioSesionIN(request):    
    if request.method == 'POST':
        documento = request.POST.get('documento_id')
        password = request.POST.get('contrasena')
        
        # Obtener el perfil del usuario basado en el documento
        perfil = Perfil.objects.filter(documento=documento).first()
        if perfil is None:
            messages.error(request,'El usuario no existe')

        if perfil != None:
            # Obtener el usuario de auth_user relacionado con el perfil
            usuario = perfil.user

            # Verificar la contraseña utilizando check_password
            if usuario and check_password(password, usuario.password):
                # Autenticar al usuario y redirigir
                user = authenticate(request, username=usuario.username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['usuario_id'] = usuario.id 
                    request.session['name'] = usuario.first_name
                    request.session['lastname'] = usuario.last_name
                    print(request.session)    
                    return redirect('inicio/')
            else:
                messages.success(request, 'Credenciales inválidas')
    
    return render(request, 'inicioSesionIN.html')


def config_usuario(request):
        
    if request.user.is_authenticated:
            es_rrhh = request.user.groups.filter(name='RRHH').exists()
            usuario_id = request.session.get('usuario_id')
            nombre_usuario = request.session.get('name')
            apellido_usuario = request.session.get('lastname')
            user = request.user
            perfil = Perfil.objects.get(user=user)
            if request.method == 'POST':
                form = ConfigurarPerfil(request.POST)
                if form.is_valid():
                    form = form.cleaned_data
                    perfil.numero_cel = form['phone_number']
                    perfil.numero_tel = form['telphone_number']
                    perfil.edad = form['age']
                    perfil.genero = form['gender']
                    perfil.save()
                    messages.error(request, 'Datos actualizados con exito')

                    if form['password'] and form['password_confirm']:
                        user.set_password(form['password'])
                        user.save()
                   
                    
            return render(request,'config_usuario.html',{'perfil':perfil, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})

    else: 
            return redirect('/inicioSesion')