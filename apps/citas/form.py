from django import forms
from apps.citas.models import *

class TipoMascotaForm(forms.ModelForm):
    """Form definition for TipoMascota."""

    class Meta:
        """Meta definition for TipoMascotaform."""

        model = TipoMascota
        fields = '__all__'
        widgets={
            'descripcion':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-control'}),
            #'usuario_activo':forms.TextInput(attrs={'class':'form-control'}),
            #'usuario_administrador':forms.TextInput(attrs={'class':'form-control'}),
        }

class RazaForm(forms.ModelForm):
    """Form definition for TipoMascota."""

    class Meta:
        """Meta definition for TipoMascotaform."""

        model = Raza
        fields = '__all__'
        widgets={
            'id_tipo_mascota':forms.Select(attrs={'class':'form-select'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-control'}),
            #'usuario_activo':forms.TextInput(attrs={'class':'form-control'}),
            #'usuario_administrador':forms.TextInput(attrs={'class':'form-control'}),
        }

class MascotaForm(forms.ModelForm):
    """Form definition for Mascota."""

    class Meta:
        """Meta definition for Mascotaform."""

        model = Mascota
        fields = '__all__'
        widgets={
            #'id_cliente':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloNumeros(event);'}),
            'id_raza':forms.Select(attrs={'class':'form-select'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'fecha_nacimiento':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'fecha_registro':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'estado':forms.CheckboxInput(),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets={
            'id_mascota':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloNumeros(event);'}),
            'id_usuario':forms.Select(attrs={'class':'form-select'}),
            'fecha_cita':forms.DateInput(attrs={'class':'form-control'}),
            'costo':forms.NumberInput(attrs={'class':'form-control','onkeypress':'return soloNumeros(event);'}),
            'estado':forms.CheckboxInput(),

        }

class TipoServicioForm(forms.ModelForm):
    """Form definition for TipoServicio."""

    class Meta:
        """Meta definition for TipoServicioform."""

        model = TipoServicio
        fields = '__all__'
        widgets={
            'descripcion':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class ServicioForm(forms.ModelForm):
    """Form definition for Servicio."""

    class Meta:
        """Meta definition for Servicioform."""

        model = Servicio
        fields = '__all__'
        widgets={
            'id_tipo_servicio':forms.Select(attrs={'class':'form-select'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'precio':forms.NumberInput(attrs={'class':'form-control','onkeypress':'return soloNumeros(event);'}),
            'estado':forms.CheckboxInput(),

        }

class DetalleCitaServicioForm(forms.ModelForm):
    """Form definition for DetalleCitaServicio."""

    class Meta:
        """Meta definition for DetalleCitaServicioform."""

        model = DetalleCitaServicio
        fields = '__all__'
        widgets={
            'id_servicio':forms.Select(attrs={'class':'form-select'}),
            'detalle':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'monto':forms.CheckboxInput(attrs={'class':'form-control'}),
        }


