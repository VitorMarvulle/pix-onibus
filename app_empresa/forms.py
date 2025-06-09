from django import forms
from .models import Funcionario,Linha,Passagem


class FuncionarioForm(forms.ModelForm):
  class Meta:
    model = Funcionario
    fields = ['nome','funcao','cpf']
    widgets = {
          'nome': forms.TextInput(attrs={'class': 'login-input', 'placeholder': 'Nome completo'}),
          'funcao': forms.TextInput(attrs={'class': 'login-input', 'placeholder': 'Função'}),
          'cpf': forms.NumberInput(attrs={'class': 'login-input', 'placeholder': '00000000000','maxlength': '11',
    'title': 'Digite apenas números'}),
    }
    
  def clean_cpf(self):
      cpf = self.cleaned_data.get('cpf')

      if self.instance.pk:
        if Funcionario.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Um fucionário com esse CPF já esta cadastrado!")
        
      else:
        if Funcionario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Um fucionário com esse CPF já esta cadastrado!")
        
      return cpf

class LinhaForm(forms.ModelForm):
  class Meta:
    model = Linha
    fields = ['idLinha','nomeLinha']
    widgets = {
            'idLinha': forms.NumberInput(attrs={'class': 'login-input'}),
            'nomeLinha': forms.TextInput(attrs={'class': 'login-input'}),
        }
  
  def clean_idLinha(self):
        idLinha = self.cleaned_data.get('idLinha')

        if self.instance.pk:
          if Linha.objects.filter(idLinha=idLinha).exclude(pk=self.instance.pk).exists():
              raise forms.ValidationError("Esta linha ja está cadastrada")
          
        else:
          if Linha.objects.filter(idLinha=idLinha).exists():
             raise forms.ValidationError("Esta linha ja está cadastrada")
          
        return idLinha

    

