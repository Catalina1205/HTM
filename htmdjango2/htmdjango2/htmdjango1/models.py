from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Usuarios (models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    tipo_documento = models.CharField(max_length=40)
    documento = models.CharField(max_length=40)
    numero_cel = models.CharField(max_length=40)
    numero_tel = models.CharField(max_length=40)
    correo = models.CharField(max_length=40)
    contraseña = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    genero = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'usuarios'


class CustomUser (AbstractUser):
    tipo_documento = models.CharField(max_length=40)
    documento = models.CharField(max_length=40)
    numero_cel = models.CharField(max_length=40)
    numero_tel = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    genero = models.CharField(max_length=40)
    

       
class Eps (models.Model):
    nombre = models.CharField(max_length=100)       
    
    class Meta:
        db_table = 'eps'
  
        
class Trasladoeps (models.Model):
    motivo = models.CharField(max_length=100)
    certificadoEPSactual = models.BinaryField(max_length=1048576)
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
    certificadoIncapacidad = models.BinaryField(max_length=1048576)
    Datetime_create = models.DateTimeField(auto_now_add=True)
    usuarios_id = models.IntegerField()
    tipodeincapacidad_id = models.IntegerField()
    
    class Meta:
        db_table = 'incapacidades'
        


