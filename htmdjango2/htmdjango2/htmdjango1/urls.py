"""
URL configuration for htmdjango1 project.

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
from htmdjango1.views import inicio, permisosUF, solicitudPermisos, historialPermisos, incapacidadesUF,  trasladoEPSUF, inicioUA, permisosUA, inicioIN, inicioSesionIN,registropaso1, registropaso2, pagina, insertartrasladoEPS, insertarincapacidad, listadotraslados, borrartraslado, listadoincapacidades, borrarincapacidad, listadotrasladosUA, listadoincapacidadesUA, verdetallestrasladoEPS, verdetallesincapacidades

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio ),
    path('permisosUF/', permisosUF), 
    path('solicitudPermisos/', solicitudPermisos),
    path('historialPermisos/', historialPermisos),
    path('incapacidadesUF/',incapacidadesUF),
    path('trasladoEPSUF/', trasladoEPSUF),
    path('inicioUA/', inicioUA ), 
    path('permisosUA/', permisosUA ), 
    path('', inicioIN ),
    path('inicioSesionIN', inicioSesionIN ),
    path('registropaso1', registropaso1 ),
    path('registropaso2', registropaso2 ),
    path('registropaso3', pagina ),
    path('insertartrasladoEPS/', insertartrasladoEPS),
    path('insertarincapacidades/', insertarincapacidad),
    path('historialtrasladosEPSUF/', listadotraslados),
    path('borrartraslado/<int:idtraslado>', borrartraslado),
    path('historialincapacidadesUF/', listadoincapacidades),
    path('borrarincapacidad/<int:idincapacidad>', borrarincapacidad),
    path('historialtrasladosEPSUA/', listadotrasladosUA),
    path('historialincapacidadesUA/', listadoincapacidadesUA),
    path('verdetallestraslado/<int:traslado_id>', verdetallestrasladoEPS),
    path('verdetallesincapacidad/<int:incapacidad_id>', verdetallesincapacidades)
    
]
