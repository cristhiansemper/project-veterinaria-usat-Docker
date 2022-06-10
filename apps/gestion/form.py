from django import forms
from apps.gestion.models import *

class FormularioUsuario(forms.ModelForm):
    password1= forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class":"form-control",
            'id':'password1',
            'required':'required'
        }
    ))
    password2= forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'password2',
            'required':'required'
        }
    ))

    class Meta:
        model=Usuario
        #fields= ['username','nombres','apellidos','email','is_active']
        fields='__all__'
        widgets={
            'id_tipo_empleado':forms.Select(attrs={'class':'form-select'}),
            'id_tipo_documento':forms.Select(attrs={'class':'form-select'}),
            'numero_documento':forms.Select(attrs={'class':'form-select'}),
            'sexo':forms.Select(attrs={'class':'form-select'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'nombres':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'apellidos':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control','onkeypress':'return soloLetras(event);'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control'}),
            'fecha_registro':forms.DateInput(attrs={'class':'form-control'}),
            #'usuario_activo':forms.TextInput(attrs={'class':'form-control'}),
            #'usuario_administrador':forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2
    
    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user