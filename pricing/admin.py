from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'unidade_medida']
    search_fields = ['nome']
    list_filter = ['unidade_medida']

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'custo', 'valor_venda', 'margem_lucro']
    search_fields = ['nome']
    list_filter = ['margem_lucro']

@admin.register(CustoIndireto)
class CustoIndiretoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor']
    search_fields = ['nome']
    list_filter = ['valor']

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'salario']
    search_fields = ['nome']
    list_filter = ['salario']

@admin.register(Lojas)
class LojasAdmin(admin.ModelAdmin):
    list_display = ['endereco', 'numero_por_dia', 'custo_por_prato']
    search_fields = ['endereco']
    list_filter = ['numero_por_dia']

@admin.register(QuantidadeIngrediente)
class QuantidadeIngredienteAdmin(admin.ModelAdmin):
    list_display = ['receita', 'ingrediente', 'quantidade']
    search_fields = ['receita']
    list_filter = ['ingrediente']

