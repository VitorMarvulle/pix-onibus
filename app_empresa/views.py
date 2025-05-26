from django.shortcuts import render

def login(request):
    return render(request, 'login.html', {
        'previous_url': '/',
        'next_url': '/empresa/dashboard/',
    })

def dashboard(request):
    return render(request, 'dashboard.html', {
        'previous_url': '/',
        'add_motorista': '/empresa/add_motorista/',
        'add_linha': '/empresa/add_linha/',
        'lista_motorista': '/empresa/lista_motorista/',
    })

def add_linha(request):
    return render(request, 'add_linha.html', {
        'previous_url': '/empresa/dashboard/',
        'next_url': '/add_motorista/',
    })

def add_motorista(request):
    return render(request, 'add_motorista.html', {
        'previous_url': '/empresa/dashboard/',
        'next_url': '/lista_motorista/',
    })

def lista_motorista(request):
    return render(request, 'lista_motorista.html', {
        'previous_url': '/',
        'add_motorista': '/empresa/add_motorista/',
        'add_linha': '/empresa/add_linha/',
        'dashboard': '/empresa/dashboard/',
    })

def linha_motorista(request):
    return render(request, 'linha_motorista.html', {
        'previous_url': '/',
        'next_url': '/empresa/home_motorista/',
    })
    
def home_motorista(request):
    return render(request, 'home_motorista.html', {
        'previous_url': '/empresa/linha_motorista/',
        'next_url': '/login/',
    })
    
def confirmacao(request):
    return render(request, 'confirmacao.html', {
        'previous_url': '/empresa/home_motorista/',
    })