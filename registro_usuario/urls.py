from django.urls import path
from . import views

urlpatterns = [
    path('registropaso1', views.registropaso1 ),
    path('registropaso2', views.registropaso2 ),
    path('registropaso3', views.pagina )
]