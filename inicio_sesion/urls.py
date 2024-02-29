from django.urls import path
from . import views

urlpatterns = [
    path('inicioSesion', views.inicioSesionIN ),
    path('user/configuracion',views.config_usuario)

       
]