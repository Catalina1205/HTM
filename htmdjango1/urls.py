
from django.contrib import admin
from django.urls import path, include
from htmdjango1.views import inicio, inicioUA, inicioIN, logoutusuario, errorpagina

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('solicitudes_empleado.urls')),
    path('', include('revision_solicitudes.urls')),
    path('', include('inicio_sesion.urls')),
    path('', include('registro_usuario.urls')),
    path('inicio/', inicio ),
    path('inicioUA/', inicioUA ), 
    path('logout/', logoutusuario ), 
    path('errorpagina/', errorpagina),
    path('', inicioIN )    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
