from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('ingredientes/', IngredienteListView.as_view(), name='ingredient-list'),
    path("ingrediente/adicionar", IngredienteCreateView.as_view(), name="ingredient-create"),
    path("ingrediente/<int:pk>/editar", IngredienteUpdateView.as_view(), name="ingredient-update"),
    path("ingrediente/<int:pk>/excluir", IngredienteDeleteView.as_view(), name="ingredient-delete"),
    path('receitas/', ReceitaListView.as_view(), name='receita-list'),
    path('receitas/<int:pk>/', ReceitaDetailView.as_view(), name='receita-detail'),
    path('receitas/adicionar', ReceitaCreateView.as_view(), name='receita-create'),
    path('receitas/<int:pk>/editar', ReceitaUpdateView.as_view(), name='receita-update'),
    path('receitas/<int:pk>/excluir', ReceitaDeleteView.as_view(), name='receita-delete'),
    path('custos-indiretos/', CustoIndiretoListView.as_view(), name='custo-list'),
    path('custos-indiretos/adicionar', CustoIndiretoCreateView.as_view(), name='custo-create'),
    path('custos-indiretos/<int:pk>/editar', CustoIndiretoUpdateView.as_view(), name='custo-update'),
    path('custos-indiretos/<int:pk>/excluir', CustoIndiretoDeleteView.as_view(), name='custo-delete'),
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionario-list'),
    path('funcionarios/<int:pk>/', FuncionarioDetailView.as_view(), name='funcionario-detail'),
    path('funcionarios/adicionar', FuncionarioCreateView.as_view(), name='funcionario-create'),
    path('funcionarios/<int:pk>/editar', FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('funcionarios/<int:pk>/excluir', FuncionarioDeleteView.as_view(), name='funcionario-delete'),
    path('lojas/', LojasListView.as_view(), name='loja-list'),
    path('lojas/<int:pk>/', LojasDetailView.as_view(), name='loja-detail'),
    path('lojas/adicionar', LojasCreateView.as_view(), name='loja-create'),
    path('lojas/<int:pk>/editar', LojasUpdateView.as_view(), name='loja-update'),
    path('lojas/<int:pk>/excluir', LojasDeleteView.as_view(), name='loja-delete'),
]