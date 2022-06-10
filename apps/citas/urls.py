from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.citas.views import *
urlpatterns =[
    path('listar_tipo_mascota/',login_required(TipoMascotaListView.as_view()), name='listar_tipo_mascota'),
    path('tipo_mascota/',login_required(TipoMascotaView.as_view()), name='tipo_mascota'),
    path('modificar_tipo_mascota/',login_required(TipoMascotaUpdateView.as_view()), name='modificar_tipo_mascota'),
    path('eliminar_tipo_mascota/<int:id>/',login_required(eliminarTipoMascota), name='eliminar_tipo_mascota'),

    path('listar_raza/',login_required(RazaListView.as_view()), name='listar_raza'),
    path('raza/',login_required(RazaView.as_view()), name='raza'),
    path('modificar_raza/',login_required(RazaUpdateView.as_view()), name='modificar_raza'),
    path('eliminar_raza/<int:id>/',login_required(eliminarRaza), name='eliminar_raza'),

    path('listar_mascota/',login_required(MascotaListView.as_view()), name='listar_mascota'),
    path('mascota/',login_required(MascotaView.as_view()), name='mascota'),
    path('modificar_mascota/',login_required(MascotaUpdateView.as_view()), name='modificar_mascota'),
    path('eliminar_mascota/<int:id>/',login_required(eliminarMascota), name='eliminar_mascota'),
    path('buscar_cliente/<str:dni>/',login_required(buscarCliente), name='buscar_cliente'),
    path('listar_tipo_servicio/',login_required(TipoServicioListView.as_view()), name='listar_tipo_servicio'),
    path('tipo_servicio/',login_required(TipoServicioView.as_view()), name='tipo_servicio'),
    path('modificar_tipo_servicio/',login_required(TipoServicioUpdateView.as_view()), name='modificar_tipo_servicio'),
    path('eliminar_tipo_servicio/<int:id>/',login_required(eliminarTipoServicio), name='eliminar_tipo_servicio'),

    path('listar_servicio/',login_required(ServicioListView.as_view()), name='listar_servicio'),
    path('servicio/',login_required(ServicioView.as_view()), name='servicio'),
    path('modificar_servicio/',login_required(ServicioUpdateView.as_view()), name='modificar_servicio'),
    path('eliminar_servicio/<int:id>/',login_required(eliminarServicio), name='eliminar_servicio'),

    #Cita
    #path('listar_cita/',login_required(CitaListView.as_view()), name='listar_cita'),
    #path('cita/', login_required(CitaView.as_view()), name='cita'),
    #path('modificar_cita/',login_required(MascotaUpdateView.as_view()), name='modificar_cita'),
    #path('eliminar_cita/<int:id>/',login_required(eliminarCita), name='eliminar_cita'),
    
    
]