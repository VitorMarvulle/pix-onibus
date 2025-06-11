from django.shortcuts import render, redirect
from .forms import FuncionarioForm,LinhaForm,LoginForm,SelecionarLinhaForm
from .models import Linha,Funcionario,Historico, Passagem
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['login_opcao']
            identificador = form.cleaned_data['identificador']
            senha = form.cleaned_data['senha']


            try:
                if tipo =='codigo':
                    funcionario = Funcionario.objects.get(codigo=identificador,senha = senha)
                    request.session['funcionario_id'] = funcionario.idFuncionario
                    messages.success(request,'Login de Motorista realizado com Sucesso!')
                    return redirect('linha_motorista')
                else:
                    funcionario = Funcionario.objects.get(email=identificador,senha=senha)
                    request.session['funcionario_id'] = funcionario.idFuncionario
                    messages.success(request, 'Login de Administrador realizado com sucesso!')
                    return redirect('dashboard')
            except Funcionario.DoesNotExist:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    context = {
            'form':form,
            'previous_url': '/',
            'next_url': '/empresa/dashboard/'
        }
    return render(request, 'login.html', context)

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
    if 'funcionario_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = SelecionarLinhaForm(request.POST)
        if form.is_valid():
            linha = form.cleaned_data['linha']
            request.session['linha_id']= linha.idLinha
            return redirect('home_motorista')
        
    else:
        form = SelecionarLinhaForm()

    context = {
        'form':form,
        'previous_url': '/',
        'next_url': '/empresa/home_motorista/',
    }

    return render(request, 'linha_motorista.html', context)
    
def home_motorista(request):
    funcionario_id = request.session.get('funcionario_id')
    linha_id = request.session.get('linha_id')

    if not funcionario_id or not linha_id:
        return redirect('login')
    
    funcionario = Funcionario.objects.get(idFuncionario=funcionario_id)
    linha = Linha.objects.get(idLinha=linha_id)

    context = {
        'funcionario':funcionario,
        'linha': linha,
        'previous_url': '/empresa/home_motorista/',
        'next_url': '/login/'

    }
    return render(request, 'home_motorista.html', context)
    
def confirmacao(request):
    return render(request, 'confirmacao.html', {
        'previous_url': '/empresa/home_motorista/',
    })

@csrf_exempt # Use com cuidado, idealmente configure CSRF no frontend
@require_POST # Garante que esta view só aceite requisições POST
def validar_bilhete(request):
    try:
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        print(f"--- Buscando no banco pelo ID recebido: '{ticket_id}' ---")

        if not ticket_id:
            return JsonResponse({'status': 'error', 'message': 'ID do bilhete não fornecido.'}, status=400)

        # Busca o bilhete no banco de dados
        passagem = Passagem.objects.get(idPassagem=ticket_id)
        usuario_id = passagem.usuario_id
        idPassagem = passagem.id
        # Verifica se ainda há usos disponíveis
        if passagem.usosDisponiveis > 0:
            passagem.usosDisponiveis -= 1  # Decrementa o número de usos
            passagem.save()

            #  INSERÇÃO NO HISTÓRICO AQUI 
            funcionario_id = request.session.get('funcionario_id')
            linha_id = request.session.get('linha_id')

            if funcionario_id and linha_id:
                funcionario = Funcionario.objects.get(idFuncionario=funcionario_id)
                linha = Linha.objects.get(idLinha=linha_id)

                Historico.objects.create(
                    usuario_id=usuario_id,
                    passagem_id=idPassagem,
                    funcionario_id=funcionario.idFuncionario,
                    linha_id=linha.idLinha 
                )
            else:
                print("Erro: ID do funcionário ou da linha não encontrado na sessão.")
            
            # Retorna sucesso com a URL para redirecionamento
            return JsonResponse({
                'status': 'success',
                'message': 'Bilhete validado com sucesso!',
                'redirect_url': f'/empresa/confirmacao/?ticket={ticket_id}&usos={passagem.usosDisponiveis}'
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
        