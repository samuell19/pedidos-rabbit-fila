from django.db import models

class Pedido(models.Model):
    produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)