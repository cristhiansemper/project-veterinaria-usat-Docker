from django.shortcuts import redirect, render

# Create your views here.
def Inicio(request):
    if request.user.is_authenticated:
        return redirect(to='dashboard')
    else:
        return render(request, 'login.html')

def dashboard(request):
    return render(request,'dashboard.html')