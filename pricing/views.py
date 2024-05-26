from django.shortcuts import render
from django.views.generic import *
from .models import *

class IndexView(TemplateView):
    template_name = "index.html"

class IngredienteListView(ListView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_list.html'
    context_object_name = 'ingredientes'

class IngredienteDetailView(DetailView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_detail.html'
    context_object_name = 'ingrediente'

class ReceitaListView(ListView):
    model = Receita
    template_name = 'receita_list.html'
    context_object_name = 'receitas'

class ReceitaDetailView(DetailView):
    model = Receita
    template_name = 'receita_detail.html'
    context_object_name = 'receita'

class CustoIndiretoListView(ListView):
    model = CustoIndireto
    template_name = 'custoindireto_list.html'
    context_object_name = 'custos_indiretos'

class CustoIndiretoDetailView(DetailView):
    model = CustoIndireto
    template_name = 'custoindireto_detail.html'
    context_object_name = 'custo_indireto'

class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'funcionario_list.html'
    context_object_name = 'funcionarios'

class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'funcionario_detail.html'
    context_object_name = 'funcionario'

class LojasListView(ListView):
    model = Lojas
    template_name = 'lojas_list.html'
    context_object_name = 'lojas'

class LojasDetailView(DetailView):
    model = Lojas
    template_name = 'lojas_detail.html'
    context_object_name = 'loja'