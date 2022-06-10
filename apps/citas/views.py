import json
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, UpdateView, TemplateView
from django.core.serializers import serialize
from apps.citas.models import *
from apps.gestion.models import *
from apps.citas.form import *
# Create your views here.

def buscarCliente(request,dni):
    if request.method=='GET':
        print(dni)
        tm=Cliente.objects.filter(numero_documento=dni)
        print(tm)
        tm_serializer=serialize('json',tm)
        return JsonResponse({'status':True,'cliente':tm_serializer})

class TipoMascotaListView(ListView):
    def get(self,request,*args,**kwargs):
        tm=TipoMascota.objects.all()
        tm_serializer=serialize('json',tm)
        return JsonResponse({'status':True,'tipo_mascota':tm_serializer})

class TipoMascotaView(View):
    model= TipoMascota
    form_class= TipoMascotaForm
    template_name='Citas/tipomascota.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):
        existe=self.model.objects.filter(descripcion__iexact=request.POST['descripcion'])
        if not existe.exists():
            formulario=self.form_class(request.POST)
            if formulario.is_valid():
                formulario.save()
                return JsonResponse({'status':True,'mensaje':'Tipo de mascota agregado correctamente'})
            else:
                return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        else:
            return JsonResponse({'status':False,'mensaje':'La descripción ingresado ya está registrado'})

class TipoMascotaUpdateView(UpdateView):
    def post(self,request,*args,**kwargs):
        tm=get_object_or_404(TipoMascota,id_tipo_mascota=request.POST['id_tipo_mascota'])
        formulario=TipoMascotaForm(request.POST, instance=tm)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Tipo de mascota modificado correctamente'})
        else:
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})

def eliminarTipoMascota(request, id):
    if request.method=='GET':
        tm=TipoMascota.objects.filter(id_tipo_mascota=id)
        print(tm)
        if tm.exists():
            tm.delete()
            return JsonResponse({'status':True,'mensaje':'Tipo de mascota elimado correctamente'})  

class RazaListView(ListView):
    def get(self,request,*args,**kwargs):
        cursor =connection.cursor()
        sql="select raza.id_raza as id,raza.descripcion,raza.estado,tipo_mascota.descripcion from citas_raza as raza "
        sql+="inner join citas_tipomascota as tipo_mascota on raza.id_tipo_mascota_id=tipo_mascota.id_tipo_mascota "
        cursor.execute(sql)
        razas = cursor.fetchall()
        cursor.close()
        return JsonResponse({'status':True,'raza':razas})

class RazaView(View):
    model= Raza
    form_class= RazaForm
    template_name='Citas/raza.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):
        existe=self.model.objects.filter(id_tipo_mascota=request.POST['id_tipo_mascota'],descripcion__iexact=request.POST['descripcion'])
        if not existe.exists():
            formulario=self.form_class(request.POST)
            if formulario.is_valid():
                formulario.save()
                return JsonResponse({'status':True,'mensaje':'Raza agregado correctamente'})
            else:
                return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        else:
            return JsonResponse({'status':False,'mensaje':'La raza y mascota ya está registrado'})
    
class RazaUpdateView(UpdateView):
    def post(self,request,*args,**kwargs):
        raza=get_object_or_404(Raza,id_raza=request.POST['id_raza'])
        formulario=RazaForm(request.POST, instance=raza)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Raza modificado correctamente'})
        else:
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})

def eliminarRaza(request, id):
    if request.method=='GET':
        raza=Raza.objects.filter(id_raza=id)
        if raza.exists():
            raza.delete()
            return JsonResponse({'status':True,'mensaje':'Raza elimado correctamente'})  

class MascotaListView(ListView):
    def get(self,request,*args,**kwargs):
        cursor =connection.cursor()
        sql="select * from fn_lista_mascotas()"
        cursor.execute(sql)
        mascota = cursor.fetchall()
        cursor.close()
        return JsonResponse({'status':True,'mascota':mascota})

class MascotaView(View):
    model= Mascota
    form_class= MascotaForm
    template_name='Citas/mascota.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        context['animal']=TipoMascota.objects.all()
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):      
        formulario=self.form_class(request.POST)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Mascota agregado correctamente'})
        else:
            print(formulario.errors)
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        
class MascotaUpdateView(UpdateView):
    def post(self,request,*args,**kwargs):
        print(request.POST['id_mascota'])
        raza=get_object_or_404(Mascota,id_mascota=request.POST['id_mascota'])
        print('9')
        print(raza)
        formulario=MascotaForm(request.POST, instance=raza)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Mascota modificado correctamente'})
        else:
            print(formulario.errors)
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})

def eliminarMascota(request, id):
    if request.method=='GET':
        mascota=Mascota.objects.filter(id_mascota=id)
        if mascota.exists():
            mascota.delete()
            return JsonResponse({'status':True,'mensaje':'Mascota elimado correctamente'})  

class TipoServicioListView(ListView):
    def get(self,request,*args,**kwargs):
        ts=TipoServicio.objects.all()
        ts_serialize=serialize('json',ts)
        return JsonResponse({'status':True,'tipo_servicio':ts_serialize})

class TipoServicioView(View):
    model= TipoServicio
    form_class= TipoServicioForm
    template_name='Citas/tiposervicio.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):
        existe=self.model.objects.filter(descripcion__iexact=request.POST['descripcion'])
        if not existe.exists():
            formulario=self.form_class(request.POST)
            if formulario.is_valid():
                formulario.save()
                return JsonResponse({'status':True,'mensaje':'Tipo de servicio agregado correctamente'})
            else:
                return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        else:
            return JsonResponse({'status':False,'mensaje':'Tipo de servicio ya está registrado'})

class TipoServicioUpdateView(UpdateView):
    def post(self,request,*args,**kwargs):
        ts=get_object_or_404(TipoServicio,id_tipo_servicio=request.POST['id_tipo_servicio'])
        formulario=TipoServicioForm(request.POST, instance=ts)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Tipo de Servicio modificado correctamente'})
        else:
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})

def eliminarTipoServicio(request, id):
    if request.method=='GET':
        ts=TipoServicio.objects.filter(id_tipo_servicio=id)
        if ts.exists():
            ts.delete()
            return JsonResponse({'status':True,'mensaje':'Tipo de servicio elimado correctamente'}) 

class ServicioListView(ListView):
    def get(self,request,*args,**kwargs):
        cursor =connection.cursor()
        sql="select * from fn_lista_servicios()"
        cursor.execute(sql)
        servicio = cursor.fetchall()
        cursor.close()
        return JsonResponse({'status':True,'servicio':servicio})

class ServicioView(View):
    model= Servicio
    form_class= ServicioForm
    template_name='Citas/servicio.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):
        existe=self.model.objects.filter(id_tipo_servicio=request.POST['id_tipo_servicio'],descripcion__iexact=request.POST['descripcion'])
        if not existe.exists():
            formulario=self.form_class(request.POST)
            if formulario.is_valid():
                formulario.save()
                return JsonResponse({'status':True,'mensaje':'Servicio agregado correctamente'})
            else:
                return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        else:
            return JsonResponse({'status':False,'mensaje':'El servicio ya está registrado'})

class ServicioUpdateView(UpdateView):
    def post(self,request,*args,**kwargs):
        servicio=get_object_or_404(Servicio,id_servicio=request.POST['id_servicio'])
        formulario=ServicioForm(request.POST, instance=servicio)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'status':True,'mensaje':'Servicio modificado correctamente'})
        else:
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
    
def eliminarServicio(request, id):
    if request.method=='GET':
        servicio=Servicio.objects.filter(id_servicio=id)
        if servicio.exists():
            servicio.delete()
            return JsonResponse({'status':True,'mensaje':'Servicio elimado correctamente'}) 

class CitaListView(ListView):
    def get(self,request,*args,**kwargs):
        cursor =connection.cursor()
        sql=""
        cursor.execute(sql)
        cita = cursor.fetchall()
        cursor.close()
        return JsonResponse({'status':True,'cita':cita})

class CitaView(TemplateView):
    template_name='Compras/cita.html'

class RegistrarCitaView(View):
    model= Cita
    form_class= CitaForm
    template_name='Citas/registrar_cita.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form']=self.form_class
        return context
    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())
    
    def post(self, request, *args,**kwargs):
        new_id=Cita.objects.values('id_cita').last()
        if new_id==None:
            new_id=1
        else:
            new_id=new_id['id_cita']+1
        
        formulario=self.form_class(request.POST)
        if formulario.is_valid():
            formulario.save()
            detalle,mensaje=self.registrarDetalleCitaServicio(new_id,request.POST['detalle_cita'])
            if detalle:   
                return JsonResponse({'status':True,'mensaje':'Cita agregada correctamente'})
            else:
                return JsonResponse({'status':False,'mensaje':mensaje})
        else:
            return JsonResponse({'status':False,'mensaje':'Formulario inválido','errors':formulario.errors})
        
    
    def registrarDetalleCitaServicio(self,id,detalle_cita_servicio):
        obj_detalle_cita_servicio=json.loads(detalle_cita_servicio)
        print(obj_detalle_cita_servicio)
        mensaje=""
        for items in obj_detalle_cita_servicio['productos']:
            formulario=DetalleCitaServicioForm({
                #'id_cita':id,'id_producto':obj_detalle_venta['productos'][items]['id_producto'], 
                #'precio':obj_detalle_venta['productos'][items]['precio'],'cantidad':obj_detalle_venta['productos'][items]['cantidad'],
                #'subtotal':obj_detalle_venta['productos'][items]['subtotal']
            })
            if formulario.is_valid():
                formulario.save()
            else:
                mensaje="Formulario inválido"
                return (False,mensaje)     
        mensaje="Detalle agregado correctamente" 
        return (True,mensaje)
        