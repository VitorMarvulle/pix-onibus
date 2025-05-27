from django.db import models

# Create your models here.
class Usuario(models.Model):
  idTelUsuario = models.BigIntegerField(primary_key=True)