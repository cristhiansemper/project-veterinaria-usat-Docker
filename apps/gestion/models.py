from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class TipoEmpleado(models.Model):
    id_tipo_empleado=models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=50, null=True, blank=False)
    estado= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de Empleado'
        verbose_name_plural = 'Tipo de Empleados'

    def __str__(self):
        return self.descripcion

class TipoDocumento(models.Model):
    id_tipo_documento=models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=20, unique=True, null=True, blank=False)
    estado= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipo de Documentos'

    def __str__(self):
        return self.descripcion

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,apellidos,password=None):
        if not email:
            raise ValueError('El usuario debe de tener correo electrónico')
        
        usuario=self.model(
            username=username, 
            email=self.normalize_email(email), 
            nombres=nombres, 
            apellidos=apellidos,
            )
    
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self,email,username,nombres,apellidos,password):
        usuario=self.create_user(
            email,
            username=username,  
            nombres=nombres, 
            apellidos=apellidos,
            password=password
        )
        usuario.usuario_administrador= True
        usuario.save()
        return usuario

usuario_sexo = [
    (0,"Femenino"),
    (1,"Masculino")
]
class Usuario(AbstractBaseUser):
    id_tipo_documento=models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING, null=True, blank=False)
    numero_documento=models.CharField(max_length=15,unique=True ,null=True, blank=False)
    username=models.CharField(unique=True, max_length=100)
    email=models.EmailField(max_length=100,null=True)
    nombres=models.CharField(max_length=50,null=False)
    apellidos=models.CharField(max_length=50,null=False)
    sexo=models.IntegerField(blank=False,null=True, choices=usuario_sexo)
    telefono=models.CharField(max_length=10, blank=True,null=False)
    fecha_nacimiento=models.DateField(blank=False,null=True)
    id_tipo_empleado=models.ForeignKey(TipoEmpleado, on_delete=models.DO_NOTHING, null=True, blank=False)
    fecha_registro=models.DateField(blank=False,null=True)
    is_active=models.BooleanField(default=True)
    usuario_staff=models.BooleanField(default=True)
    usuario_administrador=models.BooleanField(default=False)
    objects=UsuarioManager()

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['nombres','apellidos','email']

    def __str__(self):
        return f'Usuario {self.nombres}, {self.apellidos}'
      
    def has_perm(self,perm,ob = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_staff
    @property
    def is_superuser(self):
        return self.usuario_administrador

cliente_sexo = [
    (0,"Femenino"),
    (1,"Masculino")
]

class Cliente(models.Model):
    id_cliente=models.AutoField(primary_key=True)
    id_tipo_documento=models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING, null=True, blank=False)
    numero_documento=models.CharField(max_length=15,unique=True ,null=False, blank=False)
    nombre=models.CharField(max_length=70 ,null=False, blank=False)
    apellido=models.CharField(max_length=70 ,null=False, blank=False)
    sexo=models.IntegerField(blank=False,null=False, choices=cliente_sexo)
    telefono=models.CharField(max_length=10, blank=False,null=False)
    fecha_nacimiento=models.DateField(blank=False,null=False)
    direccion=models.CharField(max_length=50, blank=False,null=False)
    correo=models.EmailField(max_length=100, blank=False,null=False)
    fecha_registro=models.DateField(blank=False,null=False)
    estado=models.BooleanField(null=False,default=True)
    id_usuario=models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre


