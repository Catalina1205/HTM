from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import Template, Context
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.core.cache import cache
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from htmdjango1.models import Perfil, Eps, Trasladoeps, Tipodeincapacidad, Incapacidades, Permisos
import json
from django.conf import settings

# Cargas estácticas


def permisosUF(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        return render(request, 'Permisos/permisosUF.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    else:
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        return redirect('/inicioSesion')
 

def incapacidadesUF (request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        return render(request, 'Incapacidades/incapacidadesUF.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    else: 
            return redirect('/inicioSesion')

def trasladoEPSUF (request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        return render(request, 'TrasladosEPS/trasladoEPSUF.html',  {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario,  'es_rrhh': es_rrhh})
    else: 
        return redirect('/inicioSesion')
    

# Traslado de EPS UF

def insertartrasladoEPS(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
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
                trasladoEPS.certificadoEPSactual = certificadoEPSactual
                fecha_hora_utc = timezone.now()
                trasladoEPS.Datetime_create = fecha_hora_utc.astimezone(timezone.get_current_timezone())
                trasladoEPS.usuarios_id = usuario_id
                trasladoEPS.epsactual_id = epsactual_id  # Asignar el ID seleccionado
                trasladoEPS.epsnueva_id = epsnueva_id  # Asignar el ID seleccionado
                trasladoEPS.save()
                print (trasladoEPS.Datetime_create)
                nuevo_registro_id = trasladoEPS.id
                with connection.cursor() as cursor:
                    cursor.execute("CALL actualizar_respuesta(%s)", [nuevo_registro_id])
            
                
                # Lógica para enviar el correo electrónico
                asunto = 'Solicitud de Traslado de EPS enviada'

                # Cargar las instancias de las EPS usando los IDs del formulario
                eps_actual = get_object_or_404(Eps, id=request.POST.get('epsactual_id'))
                eps_nueva = get_object_or_404(Eps, id=request.POST.get('epsnueva_id'))

                mensaje_html = render_to_string('TrasladosEPS/correoSolicitudEPS.html', {
                    'eps_actual': eps_actual.nombre,
                    'eps_nueva': eps_nueva.nombre,
                    'motivo': request.POST.get('motivo'),
                })
                mensaje_texto = strip_tags(mensaje_html)
                
                # Cambia 'correo_origen@example.com' por tu dirección de correo
                correo_origen = 'humantalentmanagement8@gmail.com'
                destinatarios = [request.user.email]

                send_mail(asunto, mensaje_texto, correo_origen, destinatarios, html_message=mensaje_html)

                mensaje_exito = "Solicitud enviada correctamente. Revise su correo para más detalles."
                return render(request, 'TrasladosEPS/pagina_exito.html', {'mensaje_exito': mensaje_exito})


            else:
                epss = Eps.objects.all()
                return render(request, 'TrasladosEPS/solicitudTrasladoEPS.html', {'epss': epss, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    else: 
        return redirect('/inicioSesion')


def listadotraslados (request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        usuarioid = request.session.get('usuario_id')
        consultar = connection.cursor()
        consultar.execute("call listartraslados  ('"+str(usuarioid)+"')")
        return render(request, 'TrasladosEPS/historialTrasladoEPS.html', {'traslados': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    else: 
        return redirect('/inicioSesion')


def borrartraslado (request, idtraslado):  
    if request.user.is_authenticated:
        borrar = connection.cursor()
        borrar.execute("call borrartraslado ('"+str(idtraslado)+"')")
        return redirect('/historialtrasladosEPSUF')
    else: 
        return redirect('/inicioSesion')

# Incapacidades UF

def insertarincapacidad(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
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
                incapacidades.certificadoIncapacidad = certificadoIncapacidad
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
                return render(request, 'Incapacidades/solicitudIncapacidades.html', {'tipos': tipos, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    
    else: 
        return redirect('/inicioSesion')


def listadoincapacidades (request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        usuarioid = request.session.get('usuario_id')
        consultar = connection.cursor()
        consultar.execute("call listarincapacidades ('"+str(usuarioid)+"')")
        return render(request, 'Incapacidades/historialIncapacidades.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh })
    else: 
        return redirect('/inicioSesion')


def borrarincapacidad (request, idincapacidad):   
    if request.user.is_authenticated: 
        borrar = connection.cursor()
        borrar.execute("call borrarincapacidad ('"+str(idincapacidad)+"')")
        return redirect('/historialincapacidadesUF')
    else: 
        return redirect('/inicioSesion')


# Permisos UF
"""
def insertarpermiso(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        usuario_id = request.session.get('usuario_id')
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')

        if usuario_id is not None:
            if request.method == "POST":
                tipo = request.POST.get('motivoprefix')
                motivoMedico = request.POST.get('selecMotivoMedico')
                motivoPersonal = request.POST.get('selecMotivoPersonal')
                motivoPublico = request.POST.get('selecMotivoPublico')
                otro = request.POST.get('otrotext')
                fechas = request.POST.get('fechasOcultas')
                certificadoPermiso = request.FILES.get('certificadoPermiso')   
                observaciones = request.POST.get('observaciones')      
                

                if otro and otro.strip(): 
                    motivo = otro
                elif tipo == 'medico':
                    motivo = motivoMedico
                elif tipo == 'obligacionespersonales':
                    motivo = motivoPersonal
                elif tipo == 'obligacionespublicas':
                    motivo = motivoPublico
                    
                permisos = Permisos()
                permisos.tipo = tipo
                permisos.motivo = motivo
                permisos.fechaHora = fechas
                permisos.adjunto = certificadoPermiso
                permisos.observaciones = observaciones
                permisos.Datetime_create = timezone.now() 
                permisos.usuarios_id = usuario_id
                permisos.save()
                
                
                nuevo_registro_id = permisos.id
                with connection.cursor() as cursor:
                    cursor.execute("CALL actualizar_respuesta_permiso(%s)", [nuevo_registro_id])
                                
                return redirect('/historialPermisosUF')

            else:
            
                return render(request, 'Permisos/solicitudPermisos.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
    
    else: 
        return redirect('/inicioSesionIN')

"""
#Permisos correo
@login_required
def insertarpermiso(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        usuario_id = request.session.get('usuario_id')
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')

        if usuario_id is not None:
            if request.method == "POST":
                tipo = request.POST.get('motivoprefix')
                motivoMedico = request.POST.get('selecMotivoMedico')
                motivoPersonal = request.POST.get('selecMotivoPersonal')
                motivoPublico = request.POST.get('selecMotivoPublico')
                otro = request.POST.get('otrotext')
                fechas = request.POST.get('fechasOcultas')
                certificadoPermiso = request.FILES.get('certificadoPermiso')   
                observaciones = request.POST.get('observaciones')      
                
                if otro and otro.strip(): 
                    motivo = otro
                elif tipo == 'medico':
                    motivo = motivoMedico
                elif tipo == 'obligacionespersonales':
                    motivo = motivoPersonal
                elif tipo == 'obligacionespublicas':
                    motivo = motivoPublico
                    
                permisos = Permisos()
                permisos.tipo = tipo
                permisos.motivo = motivo
                permisos.fechaHora = fechas
                permisos.adjunto = certificadoPermiso
                permisos.observaciones = observaciones
                permisos.Datetime_create = timezone.now() 
                permisos.usuarios_id = usuario_id
                permisos.save()
                
                nuevo_registro_id = permisos.id
                with connection.cursor() as cursor:
                    cursor.execute("CALL actualizar_respuesta_permiso(%s)", [nuevo_registro_id])
                
                # Enviar correo electrónico
                enviar_correo_solicitud_permiso(permisos)

                # Renderizar la página de éxito con el mensaje personalizado
                mensaje_exito = "Tu solicitud de permiso ha sido enviada. Pronto recibirás una respuesta."
                return render(request, 'Permisos/pagina_exito.html', {'mensaje_exito': mensaje_exito})
            else:
                return render(request, 'Permisos/solicitudPermisos.html', {'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
        else: 
            return redirect('/inicioSesion')
    else: 
        return redirect('/inicioSesion')


    
# Modifica la función enviar_correo_solicitud_permiso en views.py
def enviar_correo_solicitud_permiso(permisos):
    asunto = 'Nueva Solicitud de Permiso'
    mensaje_html = render_to_string('Permisos/correoSolicitudPermiso.html', {
        'tipo_permiso': permisos.tipo,
        'fecha_inicio': permisos.fechaHora,  # Utiliza el campo existente fechaHora
        'fecha_fin': permisos.fechaHora,  # Utiliza el campo existente fechaHora para fecha_fin también
    })
    
    # Lista de destinatarios, puedes obtenerla de tu modelo de usuario o configurarla manualmente
    lista_destinatarios = [permisos.usuarios_id]  # Utiliza el campo existente usuarios_id

    send_mail(
        asunto,
        '',  # Deja el cuerpo del mensaje vacío, ya que estás utilizando el HTML proporcionado
        settings.EMAIL_HOST_USER,  # O utiliza otra dirección de correo configurada en tu aplicación
        lista_destinatarios,
        html_message=mensaje_html,
        fail_silently=True,
    )






def listadopermisos(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        usuarioid = request.session.get('usuario_id')
        
        permisos = Permisos.objects.filter(usuarios_id=usuarioid)
        
        for permiso in permisos:
            permiso.fechaHora = json.loads(permiso.fechaHora)
        
        return render(request, 'Permisos/historialPermisos.html', {'permisos': permisos, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})
        
    else:
        return redirect('/inicioSesion')



    
# Abrir formulario el historial traslado eps

def verdetallestrasladoEPS(request, traslado_id):
    if request.method == "POST":
        # Procesar la respuesta si es necesario
        return redirect('/historialtrasladosEPSUF')
    else:
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        consultar = connection.cursor()
        consultar.execute("call verdetallestraslado ('"+str(traslado_id)+"')")
        traslados = consultar.fetchall()  # Obtener los resultados de la consulta
        return render(request, 'TrasladosEPS/verTrasladoEPSUF.html', {'traslados': traslados, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})
    
# Abrir formulario el historial incapacidad

def verdetallesincapacidades(request, incapacidad_id):
    if request.method == "POST":
        return redirect('/historialincapacidadesUF')
    else:
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')
        consultar = connection.cursor()
        consultar.execute("call verdetallesincapacidades ('"+str(incapacidad_id)+"')")
        return render(request, 'Incapacidades/verincapacidadUF.html', {'incapacidades': consultar, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})
    
# views Abrir formulario el historial Permisos
def verdetallespermisos (request, permiso_id):
    permisos_orm = get_object_or_404(Permisos, id=permiso_id)
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
        
        return render(request, 'Permisos/verpermisosUF.html', {'permisosF': permisosF, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario})


   
# CORREOS ELECTRONICOS

# traslado eps: cuando usuario envia solicitud
@login_required
def CorreoSolicitudEnviadaEPS(request):
    if request.method == 'POST':
        # Procesar el formulario

        # Lógica para enviar el correo electrónico
        asunto = 'Solicitud de Traslado de EPS enviada'

        # Cargar las instancias de las EPS usando los IDs del formulario
        eps_actual = get_object_or_404(Eps, id=request.POST.get('epsactual_id'))
        eps_nueva = get_object_or_404(Eps, id=request.POST.get('epsnueva_id'))

        mensaje_html = render_to_string('TrasladosEPS/correoSolicitudEPS.html', {
            'eps_actual': eps_actual.nombre,
            'eps_nueva': eps_nueva.nombre,
            'motivo': request.POST.get('motivo'),
        })
        mensaje_texto = strip_tags(mensaje_html)
        
        # Cambia 'correo_origen@example.com' por tu dirección de correo
        correo_origen = 'humantalentmanagement8@gmail.com'
        destinatarios = [request.user.email]

        send_mail(asunto, mensaje_texto, correo_origen, destinatarios, html_message=mensaje_html)

        mensaje_exito = "Solicitud enviada correctamente. Revise su correo para más detalles."
        return render(request, 'TrasladosEPS/pagina_exito.html', {'mensaje_exito': mensaje_exito})

    # Asegúrate de pasar cualquier contexto necesario para el formulario
    epss = Eps.objects.all()  # Añade otros datos necesarios para el formulario
    context = {'epss': epss}  # Actualiza esto con el contexto necesario para tu formulario
    return render(request, 'TrasladosEPS/solicitudTrasladoEPS.html', context)


# Incapacidad: cuando usuario envia solicitud
@login_required
def insertarincapacidad(request):
    if request.user.is_authenticated:
        es_rrhh = request.user.groups.filter(name='RRHH').exists()
        usuario_id = request.session.get('usuario_id')
        nombre_usuario = request.session.get('name')
        apellido_usuario = request.session.get('lastname')

        if usuario_id is not None:
            if request.method == "POST":
                numeroIncapacidad = request.POST.get('numeroIncapacidad')
                fechaInicio = request.POST.get('fechaInicio')
                fechaFin = request.POST.get('fechaFin')
                certificadoIncapacidad = request.FILES.get('certificadoIncapacidad')
                tipodeincapacidad_id  = request.POST.get('tipodeincapacidad_id')

                incapacidades = Incapacidades()
                incapacidades.numeroIncapacidad = numeroIncapacidad
                incapacidades.fechaInicio = fechaInicio
                incapacidades.fechaFin = fechaFin
                incapacidades.certificadoIncapacidad = certificadoIncapacidad
                incapacidades.Datetime_create = timezone.now() 
                incapacidades.usuarios_id = usuario_id
                incapacidades.tipodeincapacidad_id = tipodeincapacidad_id
                incapacidades.save()
                nuevo_registro_id = incapacidades.id
                with connection.cursor() as cursor:
                    cursor.execute("CALL actualizar_respuesta_incapacidad(%s)", [nuevo_registro_id])

                # Enviar correo electrónico
                asunto = 'Solicitud de Incapacidad enviada'
                mensaje_html = render_to_string('Incapacidades/correoSolicitudIncapacidad.html', {
                    'tipo_incapacidad': Tipodeincapacidad.objects.get(id=tipodeincapacidad_id).nombre,
                    'numero_incapacidad': numeroIncapacidad,
                    'fecha_inicio': fechaInicio,
                    'fecha_fin': fechaFin,
                })
                mensaje_texto = strip_tags(mensaje_html)
                correo_origen = 'humantalentmanagement8@gmail.com'
                destinatarios = [request.user.email]
                send_mail(asunto, mensaje_texto, correo_origen, destinatarios, html_message=mensaje_html)

                mensaje_exito = "Solicitud de incapacidad enviada correctamente. Revise su correo para más detalles."
                return render(request, 'Incapacidades/pagina_exito.html', {'mensaje_exito': mensaje_exito})

            else:
                tipos = Tipodeincapacidad.objects.all()
                return render(request, 'Incapacidades/solicitudIncapacidades.html', {'tipos': tipos, 'nombre_usuario': nombre_usuario, 'apellido_usuario': apellido_usuario, 'es_rrhh': es_rrhh})

    else: 
        return redirect('/inicioSesion')
    
    
    






