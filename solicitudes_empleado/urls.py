from django.urls import path
from solicitudes_empleado import views

urlpatterns = [
    path('permisosUF/', views.permisosUF), 
    path('incapacidadesUF/',views.incapacidadesUF),
    path('trasladoEPSUF/', views.trasladoEPSUF),
    path('insertartrasladoEPS/', views.insertartrasladoEPS), 
    path('insertarincapacidades/', views.insertarincapacidad),
    path('historialtrasladosEPSUF/', views.listadotraslados),
    path('borrartraslado/<int:idtraslado>', views.borrartraslado),
    path('historialincapacidadesUF/', views.listadoincapacidades),
    path('borrarincapacidad/<int:idincapacidad>', views.borrarincapacidad),
    path('insertarpermiso/', views.insertarpermiso),
    path('historialPermisosUF/', views.listadopermisos),
    
    path('verTrasladoEPSUF/<int:traslado_id>/', views.verdetallestrasladoEPS, name='ver_traslado_eps_uf'),
    path('ver_incapacidad_uf/<int:incapacidad_id>/', views.verdetallesincapacidades, name='ver_incapacidad_uf'),
    path('verPermisosUF/<int:permiso_id>/', views.verdetallespermisos, name='ver_permisos_uf'), 
    
    #path('insertarpermiso/', views.insertarpermiso, name='insertarpermiso'),
    #path('insertarpermiso/', InsertarPermisoView.as_view(), name='insertarpermiso'),
    

   
]
