from django import forms
from .models import Funcionario,Linha,Passagem

class FuncionarioForm(forms.ModelForm):
  class Meta:
    model = Funcionario
    fields = ['nome','funcao','email','cpf']

class LinhaForm(forms.ModelForm):
  class Meta:
    model = Linha
    fields = ['idLinha','nomeLinha']

    

