from django.urls import path
from . import views

urlpatterns = [
    path('historialpermisosUA/', views.listadopermisosUA ),
    path('historialtrasladosEPSUA/', views.listadotrasladosUA),
    path('historialincapacidadesUA/', views.listadoincapacidadesUA),
    path('verdetallestraslado/<int:traslado_id>', views.verdetallestrasladoEPS),
    path('verdetallesincapacidad/<int:incapacidad_id>', views.verdetallesincapacidades),
    path('verdetallestraslado/<int:traslado_id>', views.verdetallestrasladoEPS),
    path('verdetallespermiso/<int:permiso_id>', views.verdetallespermisos),

]