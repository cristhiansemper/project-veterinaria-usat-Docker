from django.contrib import admin
from apps.citas.models import *
# Register your models here.
admin.site.register(TipoMascota)
admin.site.register(Raza)
admin.site.register(Mascota)
admin.site.register(Cita)
admin.site.register(TipoServicio)
admin.site.register(Servicio)
admin.site.register(DetalleCitaServicio)