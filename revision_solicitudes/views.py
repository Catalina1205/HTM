from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone 
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from htmdjango1.models import Perfil, Eps, Trasladoeps, Tipodeincapacidad, Incapacidades, Permisos, Empleado
from . import views

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
                
            return redirect('/errorpagina') 
        return wrapper
    return decorator



# Traslados EPS ↓

@group_required('RRHH')
@login_required
def listadotrasladosUA(request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    consultar = connection.cursor()
    consultar.execute("call listartrasladosUA")
    return render(request, 'TrasladosEPSUA/trasladoEPSUA.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

@group_required('RRHH')
@login_required
def verdetallestrasladoEPS (request, traslado_id):
        
    if request.method == "POST":
        opcionesrespuesta = request.POST.get('opcionesrespuesta')
        if opcionesrespuesta:
            with connection.cursor() as cursor:
                cursor.callproc("actualizarrespuestaTrasladoEPS", [opcionesrespuesta, traslado_id])
            return redirect('/historialtrasladosEPSUA')

    else:
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        consultar = connection.cursor()
        consultar.execute("call verdetallestraslado ('"+str(traslado_id)+"')")
        return render(request, 'TrasladosEPSUA/vertrasladoEPS.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


#  Incapacidades ↓

@group_required('RRHH')
@login_required
def listadoincapacidadesUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    consultar = connection.cursor()
    consultar.execute("call listarincapacidadesUA")
    return render(request, 'IncapacidadesUA/incapacidadesUA.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


@group_required('RRHH')
@login_required
def verdetallesincapacidades (request, incapacidad_id):
    if request.method == "POST":
        opcionesrespuesta = request.POST.get('opcionesrespuesta')
        if opcionesrespuesta:
            with connection.cursor() as cursor:
                cursor.callproc("actualizarrespuestaIncapacidad", [opcionesrespuesta, incapacidad_id])
            return redirect('/historialincapacidadesUA')
    
    else:
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        consultar = connection.cursor()
        consultar.execute("call verdetallesincapacidades ('"+str(incapacidad_id)+"')")
        return render(request, 'IncapacidadesUA/verincapacidad.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})
    

# Permisos ↓

@group_required('RRHH')
@login_required
def listadopermisosUA(request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')

    consultar = connection.cursor()
    consultar.execute("call listarpermisosUA")
    
    # Obtén todos los permisos del procedimiento almacenado
    permisos_procedimiento = consultar.fetchall()
    permisosF = []
    
    for permiso in permisos_procedimiento:
        # Recupera los detalles de cada permiso usando el ORM de Django
        permisos_orm = Permisos.objects.filter(id=permiso[0]).first()
        
        if permisos_orm:
            permisos_orm.fechaHora = json.loads(permisos_orm.fechaHora)
            permisosF.append(permisos_orm)
            
            # Agrega los nombres y apellidos de permisos_procedimiento a permisosF
            permisos_orm.NombreEmpleado = permiso[3]
            permisos_orm.ApellidoEmpleado = permiso[4]
           
            
    return render(request, 'PermisosUA/permisosUA.html', {'permisosF': permisosF, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


@group_required('RRHH')
@login_required
def verdetallespermisos (request, permiso_id):
    if request.method == "POST":
        opcionesrespuesta = request.POST.get('opcionesrespuesta')
        if opcionesrespuesta:
            with connection.cursor() as cursor:
                cursor.callproc("actualizarrespuestaPermiso", [opcionesrespuesta, permiso_id])
            return redirect('/historialpermisosUA')
    
    else:
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        consultar = connection.cursor()
        consultar.execute("call verdetallespermiso ('"+str(permiso_id)+"')")
        
        permisos_procedimiento = consultar.fetchall()
        permisosF = []
        
        for permiso in permisos_procedimiento:
            permisos_orm = Permisos.objects.filter(id=permiso[0]).first()
            
            if permisos_orm:
                permisos_orm.fechaHora = json.loads(permisos_orm.fechaHora)
                permisosF.append(permisos_orm)
                
                permisos_orm.NombreEmpleado = permiso[3]
                permisos_orm.ApellidoEmpleado = permiso[4]
        
        return render(request, 'PermisosUA/verpermisosUA.html', {'permisosF': permisosF, 'consultar':consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})









