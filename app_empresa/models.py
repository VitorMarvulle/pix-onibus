from django.db import models
from app.models import Usuario
import string , random 

def gerarCodigoPassagem(tamanho=6, prefixo='PX'):
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choices(caracteres, k=tamanho))
    return prefixo + codigo

# Create your models here.
class Funcionario(models.Model):
  idFuncionario = models.AutoField(primary_key=True)
  codigo = models.CharField(max_length=10, unique=True, blank= True,editable=False)
  senha = models.CharField(max_length=128)
  nome = models.CharField(max_length=100)
  funcao = models.CharField(max_length=50)
  email = models.EmailField()
  cpf = models.BigIntegerField(unique=True)

  def save(self, *args, **kwargs):
   if not self.codigo:
      self.codigo = self.gerarCodigoUnico()
      
   if not self.senha:
      self.senha = self.gerarSenhaAleatoria()

   super().save(*args, **kwargs)

  def gerarCodigoUnico(self):
     abreviacao = self.funcao[:2].upper()
     nomes = self.nome.strip().split()
     prefixoNome = nomes[0][:2].upper() if nomes else "xx"

     ultimosCpf = str(self.cpf)[-3:]
     baseCodigo = f"{abreviacao}{prefixoNome}{ultimosCpf}"
     codigo = baseCodigo
     contador = 1

     while Funcionario.objects.filter(codigo=codigo).exists():
        codigo = f"{baseCodigo}{contador}"
        contador += 1

     return codigo
  
  def gerarSenhaAleatoria(tamanho=6):
   caracteres = string.ascii_letters + string.digits  # Letras e números
   senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
   return senha
     

  def __str__(self):
        return f'{self.nome} - {self.funcao}'
  
  
class Linha(models.Model):
  idLinha = models.IntegerField(primary_key=True)
  nomeLinha = models.CharField(max_length=100)

  def __str__(self):
     return f'{self.idLinha} - {self.nomeLinha}'
  
  
class Passagem(models.Model):
  idPassagem = models.CharField(max_length=20)
  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='passagens')
  valor = models.DecimalField(max_digits=8, decimal_places=2)
  dataCriacao = models.DateTimeField(auto_now_add=True)
  usosDisponiveis = models.PositiveIntegerField(default=1)


  def save(self, *args, **kwargs):
     if not self.idPassagem:
        novoId = gerarCodigoPassagem()
        while Passagem.objects.filter(idPassagem=novoId).exists():
           novoId = gerarCodigoPassagem()
        self.idPassagem = novoId

     super().save(*args, **kwargs)

  def __str__(self):
        return f"{self.idPassagem} - R$ {self.valor}"


class Historico(models.Model):
   id = models.AutoField(primary_key=True)
   usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
   funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
   passagem = models.ForeignKey(Passagem, on_delete=models.CASCADE)
   linha = models.ForeignKey(Linha, on_delete=models.CASCADE)
   datahora= models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self.usuario.idTelUsuario} - {self.linha.nomeLinha} em {self.datahora}"


