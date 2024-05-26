from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('ingredientes/', IngredienteListView.as_view(), name='ingredient-list'),
    path('ingredientes/<int:pk>/', IngredienteDetailView.as_view(), name='ingredient-detail'),
    path('receitas/', ReceitaListView.as_view(), name='receita-list'),
    path('receitas/<int:pk>/', ReceitaDetailView.as_view(), name='receita-detail'),
    path('custos-indiretos/', CustoIndiretoListView.as_view(), name='custoindireto-list'),
    path('custos-indiretos/<int:pk>/', CustoIndiretoDetailView.as_view(), name='custoindireto-detail'),
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionario-list'),
    path('funcionarios/<int:pk>/', FuncionarioDetailView.as_view(), name='funcionario-detail'),
    path('lojas/', LojasListView.as_view(), name='lojas-list'),
    path('lojas/<int:pk>/', LojasDetailView.as_view(), name='lojas-detail'),
]