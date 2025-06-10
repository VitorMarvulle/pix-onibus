from django.shortcuts import render, redirect
from .forms import FuncionarioForm,LinhaForm
from .models import Linha,Funcionario,Historico, Passagem
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def login(request):
    return render(request, 'login.html', {
        'previous_url': '/',
        'next_url': '/empresa/dashboard/',
    })

def dashboard(request):
    
    historicos = Historico.objects.select_related('usuario','funcionario','passagem','linha').all().order_by('-datahora')

    context = {
        'historicos':historicos,
        'previous_url': '/',
        'add_motorista': '/empresa/add_motorista/',
        'add_linha': '/empresa/add_linha/',
        'lista_motorista': '/empresa/lista_motorista/'
    }

    return render(request, 'dashboard.html',context)

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

    linhas = Linha.objects.all().order_by('idLinha')

    context = {
        'form':form,
        'linhas':linhas,
        'previous_url': '/empresa/dashboard/',
        'next_url': '/add_motorista/'
    }

    return render(request, 'add_linha.html',context)

def editar_linha(request, id):
    linha = get_object_or_404(Linha, idLinha=id)
    if request.method == 'POST':
        form = LinhaForm(request.POST, instance=linha)
        if form.is_valid():
            linha = form.save(commit=False)
            linha.nomeLinha = linha.nomeLinha.upper()
            linha.save()
            messages.success(request, "Linha Atualizada com sucesso!")
            return redirect('add_linha')
    
    else:
        form = LinhaForm(instance=linha)
    
    linhas = Linha.objects.all().order_by('idLinha')

    context = {
        'form':form,
        'linhas':linhas
    }

    return render(request, 'add_linha.html',context)

def excluir_linha(request,id):
    linha = get_object_or_404(Linha, idLinha=id)
    linha.delete()
    messages.success(request, "Linha exluida com sucesso!")
    return redirect('add_linha')

def add_motorista(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST or None,request.FILES)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.funcao = funcionario.funcao.upper()
            funcionario.save()
        

            context = {
                'form': FuncionarioForm(),  # form limpo
                'senha_gerada': funcionario.senha,
                'funcionario': funcionario.nome,
                'codigo': funcionario.codigo,
                'mostrar_modal': True
            }
            
            return render(request, 'add_motorista.html',context)
    else:
        form = FuncionarioForm()

    context = {
        'form':form
    }

    return render(request, 'add_motorista.html',context)
    
def lista_motorista(request):

    funcionarios = Funcionario.objects.all().values()

    context = {
        'funcionarios': funcionarios,
        'previous_url': '/',
        'add_motorista': '/empresa/add_motorista/',
        'add_linha': '/empresa/add_linha/',
        'dashboard': '/empresa/dashboard/'
    }

    return render(request, 'lista_motorista.html',context)

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

@csrf_exempt # Use com cuidado, idealmente configure CSRF no frontend
@require_POST # Garante que esta view só aceite requisições POST
def validar_bilhete(request):
    try:
        # Extrai o dado JSON do corpo da requisição
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')

        if not ticket_id:
            return JsonResponse({'status': 'error', 'message': 'ID do bilhete não fornecido.'}, status=400)

        # Busca o bilhete no banco de dados
        passagem = Passagem.objects.get(idPassagem=ticket_id)

        # Verifica se ainda há usos disponíveis
        if passagem.usosDisponiveis > 0:
            passagem.usosDisponiveis -= 1  # Decrementa o número de usos
            passagem.save()
            
            # Retorna sucesso com a URL para redirecionamento
            return JsonResponse({
                'status': 'success',
                'message': 'Bilhete validado com sucesso!',
                'redirect_url': '/empresa/confirmacao/'
            })
        else:
            # Retorna erro se não houver usos
            return JsonResponse({
                'status': 'error',
                'message': 'Este bilhete não possui mais usos disponíveis.',
                'redirect_url': '/empresa/confirmacao/?status=error'
            }, status=400)

    except Passagem.DoesNotExist:
        # Retorna erro se o bilhete não for encontrado
        return JsonResponse({
            'status': 'error',
            'message': 'Bilhete inválido ou não encontrado.',
            'redirect_url': '/empresa/confirmacao/?status=error'
        }, status=404)
        
    except Exception as e:
        # Captura outros erros inesperados
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
