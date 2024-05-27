# pricing/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Funcionario)
@receiver(post_delete, sender=Funcionario)
def update_store_and_recipe_cost(sender, instance, **kwargs):
    loja = instance.loja_associada
    if loja:
        loja.custo = loja.calcular_custo_total()
        loja.save()
        for receita in Receita.objects.all():
            receita.custo = receita.custo_ingredientes()
            receita.valor_venda = receita.calcular_valor_venda()
            receita.save()

@receiver(post_save, sender=QuantidadeIngrediente)
@receiver(post_delete, sender=QuantidadeIngrediente)
def update_recipe_cost(sender, instance, **kwargs):
    receita = instance.receita
    receita.custo = receita.custo_ingredientes()
    receita.valor_venda = receita.calcular_valor_venda()
    receita.save()

@receiver(post_save, sender=Lojas)
@receiver(post_delete, sender=Lojas)
def update_recipes_on_store_change(sender, instance, **kwargs):
    for receita in Receita.objects.all():
        receita.custo = receita.custo_ingredientes()
        receita.valor_venda = receita.calcular_valor_venda()
        receita.save()
