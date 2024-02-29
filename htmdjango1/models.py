from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=40)
    documento = models.CharField(max_length=40)
    numero_cel = models.CharField(max_length=40)
    numero_tel = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    genero = models.CharField(max_length=40)
    cargo = models.CharField(max_length=60)
    area = models.CharField(max_length=60)
    eps = models.CharField(max_length=60)

    
    class Meta:
        db_table = 'usuarios_perfil'
        
        
class Empleado(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    tipo_documento = models.CharField(max_length=40)
    documento = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    area = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    eps = models.CharField(max_length=40)
    correo= models.CharField(max_length=60)
    
    class Meta:
        db_table = 'empleados'      
        
       
class Eps (models.Model):
    nombre = models.CharField(max_length=100)       
    
    class Meta:
        db_table = 'eps'
  
        

class Trasladoeps (models.Model):
    motivo = models.CharField(max_length=100)
    certificadoEPSactual = models.FileField(upload_to='traslados/')
    Datetime_create = models.DateTimeField(auto_now_add=True)
    usuarios_id = models.IntegerField()
    epsactual_id = models.IntegerField()
    epsnueva_id = models.IntegerField()
    
    class Meta:
        db_table = 'trasladoEPS'
        

class Tipodeincapacidad (models.Model):
    nombre = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'tipodeincapacidad'
        

class Incapacidades (models.Model):
    numeroIncapacidad = models.CharField(max_length=50) 
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    certificadoIncapacidad = models.FileField(upload_to='incapacidades/')
    Datetime_create = models.DateTimeField(auto_now_add=True)
    usuarios_id = models.IntegerField()
    tipodeincapacidad_id = models.IntegerField()
    
    class Meta:
        db_table = 'incapacidades'

class Permisos (models.Model):
    tipo = models.CharField(max_length=60) 
    motivo = models.CharField(max_length=60) 
    fechaHora = models.JSONField()
    adjunto = models.FileField(upload_to='permisos/')
    observaciones = models.CharField(max_length=250) 
    Datetime_create = models.DateTimeField(auto_now_add=True)
    usuarios_id = models.IntegerField()
    respuesta = models.CharField(max_length=5)

    
    class Meta:
        db_table = 'permisos'











