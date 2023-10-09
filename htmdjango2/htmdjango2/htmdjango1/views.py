from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.core.cache import cache
from django.db import connection
from htmdjango1.models import Usuarios, Trasladoeps, Eps, Tipodeincapacidad, Incapacidades


# Cargas estáticas ↓

def inicioIN(request):
    return render(request, 'INICIO/inicioIN.html')

def permisosUF (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/permisosUF.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario} )

def solicitudPermisos (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/solicitudPermisos.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def historialPermisos (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/historialPermisos.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def incapacidadesUF (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/incapacidadesUF.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def trasladoEPSUF (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/trasladoEPSUF.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


# Usuario administrador ↓
def inicioUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UA/inicioUA.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def permisosUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UA/permisosUA.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def listadotrasladosUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    consultar = connection.cursor()
    consultar.execute("call listartrasladosUA")
    return render(request, 'UA/trasladoEPSUA.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def listadoincapacidadesUA (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    consultar = connection.cursor()
    consultar.execute("call listarincapacidadesUA")
    return render(request, 'UA/incapacidadesUA.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

    
# InicioPosIniciosesionUF   
def inicio (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    return render(request, 'UF/inicio.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

 
# Inicio de sesion ↓
def inicioSesionIN(request):    
    if request.method == 'POST':
        documento = request.POST.get('documento_id')
        password = request.POST.get('contrasena')
        
        usuario = Usuarios.objects.filter(documento=documento, contraseña=password).first()
        if usuario:
            request.session['usuario_id'] = usuario.id 
            request.session['name'] = usuario.nombre
            request.session['lastname'] = usuario.apellido
            print(request.session)    
            return redirect('inicio/')
        else:
            messages.error(request, 'Credenciales inválidas')
        
    return render(request, 'INICIO/inicioSesionIN.html')



# Registro de usuario ↓

def registropaso1(request):    
    if request.method == 'POST':
        correo = request.POST.get('correo2')
        request.session['correoUsuario'] = correo  # Guarda el correo en la sesión
        print (request.session['correoUsuario'])
        return redirect('/registropaso2')
    else:
        return render(request, 'INICIO/registropaso1.html')


def registropaso2(request):
    if request.method == 'POST':
        if request.POST.get('codigo'):
            return redirect ('/registropaso3')
        else:
            messages.error(request, 'Debes ingresar un código')
    return render(request, 'INICIO/registropaso2.html')


def pagina(request):   
    
    correo = request.session.get('correoUsuario')  
    
    if request.method == "POST":
            
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('lista') and request.POST.get('numero') and request.POST.get('numeroCelular') and request.POST.get('numeroTelefono') and request.POST.get('password2') and request.POST.get('fecha') and request.POST.get('edad') and request.POST.get('genero'):
            
            usuarios = Usuarios()
            usuarios.nombre = request.POST.get('nombre')
            usuarios.apellido = request.POST.get('apellido')
            usuarios.tipo_documento = request.POST.get('lista')
            usuarios.documento = request.POST.get('numero')
            usuarios.numero_cel = request.POST.get('numeroCelular')
            usuarios.numero_tel = request.POST.get('numeroTelefono')
            usuarios.correo = correo
            usuarios.contraseña = request.POST.get('password2')
            usuarios.fecha_nacimiento = request.POST.get('fecha')
            usuarios.edad = request.POST.get('edad')
            usuarios.genero = request.POST.get('genero')
            usuarios.save()
            return redirect('/inicioSesionIN')
    
    else:
        return render(request, 'INICIO/registropaso3.html', {'correo': correo})
    
    

# Traslado de EPS UF
def insertartrasladoEPS(request):
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')

    if usuario_id is not None:
        if request.method == "POST":
            motivo = request.POST.get('motivo')
            certificadoEPSactual = request.FILES.get('certificadoEPSactual')  # Acceder al archivo enviado
            epsactual_id = request.POST.get('epsactual_id')  # Obtener el ID seleccionado del formulario
            epsnueva_id = request.POST.get('epsnueva_id')  # Obtener el ID seleccionado del formulario

            trasladoEPS = Trasladoeps()
            trasladoEPS.motivo = motivo
            trasladoEPS.certificadoEPSactual = certificadoEPSactual.read()
            trasladoEPS.Datetime_create = timezone.now() 
            trasladoEPS.usuarios_id = usuario_id
            trasladoEPS.epsactual_id = epsactual_id  # Asignar el ID seleccionado
            trasladoEPS.epsnueva_id = epsnueva_id  # Asignar el ID seleccionado
            trasladoEPS.save()
            nuevo_registro_id = trasladoEPS.id
            with connection.cursor() as cursor:
                cursor.execute("CALL actualizar_respuesta(%s)", [nuevo_registro_id])
            return redirect('/historialtrasladosEPSUF')

        else:
            epss = Eps.objects.all()
            return render(request, 'UF/solicitudTrasladoEPS.html', {'epss': epss, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})

def listadotraslados (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    usuarioid = request.session.get('usuario_id')
    consultar = connection.cursor()
    consultar.execute("call listartraslados  ('"+str(usuarioid)+"')")
    return render(request, 'UF/historialTrasladoEPS.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


def borrartraslado (request, idtraslado):       
    borrar = connection.cursor()
    borrar.execute("call borrartraslado ('"+str(idtraslado)+"')")
    return redirect('/historialtrasladosEPSUF')


# Incapacidades UF
def insertarincapacidad(request):
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')

    if usuario_id is not None:
        if request.method == "POST":
            numeroIncapacidad = request.POST.get('numeroIncapacidad')
            fechaInicio = request.POST.get('fechaInicio')
            fechaFin = request.POST.get('fechaFin')
            certificadoIncapacidad = request.FILES.get('certificadoIncapacidad')  # Acceder al archivo enviado
            tipodeincapacidad_id  = request.POST.get('tipodeincapacidad_id')  # Obtener el ID seleccionado del formulario


            incapacidades = Incapacidades()
            incapacidades.numeroIncapacidad = numeroIncapacidad
            incapacidades.fechaInicio = fechaInicio
            incapacidades.fechaFin = fechaFin
            incapacidades.certificadoIncapacidad = certificadoIncapacidad.read()
            incapacidades.Datetime_create = timezone.now() 
            incapacidades.usuarios_id = usuario_id
            incapacidades.tipodeincapacidad_id = tipodeincapacidad_id  # Asignar el ID seleccionado
            incapacidades.save()
            nuevo_registro_id = incapacidades.id
            with connection.cursor() as cursor:
                cursor.execute("CALL actualizar_respuesta_incapacidad(%s)", [nuevo_registro_id])
            return redirect('/historialincapacidadesUF')

        else:
            tipos = Tipodeincapacidad.objects.all()
            return render(request, 'UF/solicitudIncapacidades.html', {'tipos': tipos, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


def listadoincapacidades (request):
    nombre_usuario = request.session.get('name')
    apellido_usuario = request.session.get('lastname')
    usuarioid = request.session.get('usuario_id')
    consultar = connection.cursor()
    consultar.execute("call listarincapacidades ('"+str(usuarioid)+"')")
    return render(request, 'UF/historialIncapacidades.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


def borrarincapacidad (request, idincapacidad):       
    borrar = connection.cursor()
    borrar.execute("call borrarincapacidad ('"+str(idincapacidad)+"')")
    return redirect('/historialincapacidadesUF')


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
        return render(request, 'UA/vertrasladoEPS.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


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
        return render(request, 'UA/verincapacidad.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})