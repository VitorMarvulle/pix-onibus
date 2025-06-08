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

    

