from django.shortcuts import render, redirect
from .forms import FuncionarioForm,LinhaForm
from django.contrib import messages


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
    if request.method == 'POST':
        form = LinhaForm(request.POST or None,request.FILES)
        if form.is_valid():
            linha = form.save(commit=False)
            linha.nomeLinha = linha.nomeLinha.upper()
            linha.save()
            messages.success(request, "Linha Cadastrada com Sucesso!")
            return redirect('add_linha')
    else:
        form = LinhaForm()

    context = {
        'form':form
    }

    return render(request, 'add_linha.html',context)

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