from pyexpat import model
from django.db import models
from apps.gestion.models import Cliente, Usuario
# Create your models here.
class TipoMascota(models.Model):
    id_tipo_mascota=models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=20, null=False, blank=False)
    estado= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de Mascota'
        verbose_name_plural = 'Tipo de Mascotas'

    def __str__(self):
        return self.descripcion

class Raza(models.Model):
    id_raza=models.AutoField(primary_key=True)
    id_tipo_mascota=models.ForeignKey(TipoMascota, on_delete=models.DO_NOTHING, null=False, blank=False)
    descripcion=models.CharField(max_length=50, null=False, blank=False)
    estado= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Raza'
        verbose_name_plural = 'Razas'

    def __str__(self):
        return self.descripcion

mascota_sexo = [
    (0,"Hembra"),
    (1,"Macho")
]
class Mascota(models.Model):
    id_mascota=models.AutoField(primary_key=True)
    id_cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING, blank=False, null=False)
    id_raza=models.ForeignKey(Raza,on_delete=models.DO_NOTHING, blank=False, null=False)
    nombre=models.CharField(max_length=50, blank=False,null=False)
    fecha_nacimiento=models.DateField(blank=False,null=False)
    sexo=models.IntegerField(blank=False,null=False, choices=mascota_sexo)
    fecha_registro=models.DateField(blank=False,null=False)
    estado= models.BooleanField(default=True,null=False)
    id_usuario=models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=False, blank=False)

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    id_numero_cita=models.IntegerField(primary_key=True)
    id_mascota=models.ForeignKey(Mascota,on_delete=models.DO_NOTHING, blank=False, null=False)
    id_usuario_atencion=models.IntegerField(blank=False, null=False)
    detalle=models.CharField(max_length=255, blank=False,null=False)
    fecha_cita=models.DateField(blank=False,null=False)
    hora=models.TimeField(blank=False,null=False)
    costo=models.DecimalField(max_digits=5, blank=False, decimal_places=2,null=False)
    estado= models.BooleanField(default=True,null=False)
    id_usuario=models.ForeignKey(Usuario,on_delete=models.DO_NOTHING, blank=False, null=False)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return self.id_numero_cita

class TipoServicio(models.Model):
    id_tipo_servicio=models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=50, blank=False,null=False)
    estado=models.BooleanField(null=False,default=True)

    class Meta:
        """Meta definition for TipoServicio."""

        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipo de Servicios'

    def __str__(self):
        return self.descripcion


class Servicio(models.Model):
    id_servicio=models.AutoField(primary_key=True)
    id_tipo_servicio=models.ForeignKey(TipoServicio,on_delete=models.DO_NOTHING, null=False, blank=False)
    descripcion=models.CharField(max_length=50, blank=False,null=False)
    precio=models.DecimalField(max_digits=5, blank=False, decimal_places=2,null=False)
    estado=models.BooleanField(null=False,default=True)
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.descripcion

class DetalleCitaServicio(models.Model):
    id_detalle_cita_servicio=models.AutoField(primary_key=True)
    id_cita=models.ForeignKey(Cita,on_delete=models.DO_NOTHING, null=False, blank=False)
    id_servicio=models.ForeignKey(Servicio,on_delete=models.DO_NOTHING, null=False, blank=False)
    detalle=models.CharField(max_length=80, blank=False,null=False)
    monto=models.DecimalField(max_digits=6, blank=False, decimal_places=2,null=False)
    class Meta:
        verbose_name = 'Detalle de Cita-Servicio'
        verbose_name_plural = 'Detalle de Citas-Servicios'

    def __str__(self):
        return f'Detalle: {self.id_cita}-{self.id_servicio.descripcion}'



