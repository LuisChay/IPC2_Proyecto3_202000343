from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def resumen1(request):
    return render(request, 'resumen1.html')

def resumen2(request):
    return render(request, 'resumen2.html')

def pdf(request):
    return render(request, 'MANUAL DE USUARIO.pdf')
