from django import forms
from .models import *

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nome', 'preco', 'unidade_medida']
        labels = {
            'nome': 'Nome',
            'preco': 'Preço',
            'unidade_medida': 'Unidade de Medida',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        preco = cleaned_data.get('preco')
        nome = cleaned_data.get('nome')
        nome = nome.lower()
        
        if preco and preco <= 0:
            self.add_error('preco', 'O preço deve ser maior que zero.')
        
        if nome and Ingrediente.objects.filter(nome=nome).exists():
            self.add_error('nome', 'Ingrediente já cadastrado.')
        
        return cleaned_data

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'margem_lucro']
        labels = {
            'nome': 'Nome da receita',
            'margem_lucro': 'Margem de Lucro (%)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'margem_lucro': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 20'}),
        }
class QuantidadeIngredienteForm(forms.ModelForm):
    class Meta:
        model = QuantidadeIngrediente
        fields = ['ingrediente', 'quantidade']
        labels = {
            'ingrediente': 'Ingrediente',
            'quantidade': 'Quantidade',
        }
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'salario', 'loja_associada']
        labels = {
            'nome': 'Nome',
            'salario': 'Salário',
            'loja_associada': 'Loja associada',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'loja_associada': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salario = cleaned_data.get('salario')
        nome = cleaned_data.get('nome')
        nome = nome.lower()
        
        if salario and salario <= 0:
            self.add_error('salario', 'O salário deve ser maior que zero.')
        
        if nome and Funcionario.objects.filter(nome=nome).exists():
            self.add_error('nome', 'Funcionário já cadastrado.')
        
        return cleaned_data

class FuncionarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'salario', 'loja_associada']
        labels = {
            'nome': 'Nome',
            'salario': 'Salário',
            'loja_associada': 'Loja associada',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'loja_associada': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salario = cleaned_data.get('salario')
        
        if salario and salario <= 0:
            self.add_error('salario', 'O salário deve ser maior que zero.')
        
        return cleaned_data

class LojaForm(forms.ModelForm):
    class Meta:
        model = Lojas
        fields = ['endereco', 'aluguel', 'agua', 'luz', 'numero_por_dia']
        labels = {
            'endereco': 'Endereço',
            'aluguel': 'Aluguel',
            'agua': 'Água',
            'luz': 'Luz',
            'numero_por_dia': 'Pratos vendidos por dia',
        }
        widgets = {
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'aluguel': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Aluguel'}),
            'agua': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Água'}),
            'luz': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Luz'}),
            'numero_por_dia': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        numero_por_dia = cleaned_data.get('numero_por_dia')
        custo_por_prato = cleaned_data.get('custo_por_prato')
        
        if numero_por_dia and numero_por_dia <= 0:
            self.add_error('numero_por_dia', 'O número de pratos por dia deve ser maior que zero.')
        
        if custo_por_prato and custo_por_prato <= 0:
            self.add_error('custo_por_prato', 'O custo por prato deve ser maior que zero.')
        
        return cleaned_data
        
class CustoIndiretoForm(forms.ModelForm):
    class Meta:
        model = CustoIndireto
        fields = ['nome', 'valor']
        labels = {
            'nome': 'Nome',
            'valor': 'Valor',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        valor = cleaned_data.get('valor')
        nome = cleaned_data.get('nome')
        nome = nome.lower()
        
        if valor and valor <= 0:
            self.add_error('valor', 'O valor deve ser maior que zero.')
            
        if nome and not CustoIndireto.objects.filter(nome=nome).exists():
            if nome and CustoIndireto.objects.filter(nome=nome).exists():
                self.add_error('nome', 'Custo indireto já cadastrado.')
        
        return cleaned_data