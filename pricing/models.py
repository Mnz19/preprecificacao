from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Ingrediente(models.Model):
    UNIDADES_CHOICES = (
        ('g', 'gramas (G)'),
        ('kg', 'quilogramas (Kg)'),
        ('ml', 'mililitros (Ml)'),
        ('l', 'litros (L)'),
        ('un', 'unidades'),
    )
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço por peso', max_digits=10, decimal_places=2)
    unidade_medida = models.CharField('Unidade de Medida', max_length=2, choices=UNIDADES_CHOICES)
    
    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nome']

class Receita(models.Model):
    nome = models.CharField('Nome', max_length=100)
    ingredientes = models.ManyToManyField(Ingrediente, through='QuantidadeIngrediente', verbose_name='Ingredientes')
    custo = models.DecimalField('Custo', max_digits=10, decimal_places=2, default=0.00, editable=False)
    valor_venda = models.DecimalField('Valor de Venda', max_digits=10, decimal_places=2, default=0.00, editable=False)
    margem_lucro = models.DecimalField('Margem de Lucro (%)', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})
    
    def custo_ingredientes(self):
        total = 0
        for quantidade in self.quantidadeingrediente_set.all():
            total += quantidade.ingrediente.preco * quantidade.quantidade
        return total    
    
    @property
    def custo_lojas(self):
        custo_lojas = 0
        for loja in Lojas.objects.all():
            if loja.numero_por_dia > 0:
                custo_lojas += loja.custo_por_prato
        return custo_lojas
    
    def calcular_valor_venda(self):
        custo_total = self.custo_ingredientes() + self.custo_lojas
        return custo_total * (1 + self.margem_lucro / 100)
    
    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        ordering = ['nome']

class QuantidadeIngrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.ingrediente} - {self.quantidade} na receita {self.receita}'
    
    class Meta:
        verbose_name = 'Quantidade de Ingrediente'
        verbose_name_plural = 'Quantidades de Ingredientes'
        ordering = ['ingrediente']

class CustoIndireto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nome 
    
    class Meta:
        verbose_name = 'Custo Indireto'
        verbose_name_plural = 'Custos Indiretos'
        ordering = ['nome']

class Funcionario(models.Model):
    nome = models.CharField('Nome', max_length=100)
    salario = models.DecimalField('Salário', max_digits=10, decimal_places=2)
    loja_associada = models.ForeignKey('Lojas', verbose_name='Lojas', blank=True, null=True, on_delete=models.SET_NULL, related_name='funcionario')
    ativo = models.BooleanField('Ativo?', default=True)
    
    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']

class Lojas(models.Model):
    endereco = models.CharField('Endereço', max_length=150)
    aluguel = models.DecimalField('Aluguel', max_digits=10, decimal_places=2)
    agua = models.DecimalField('Água', max_digits=10, decimal_places=2)
    luz = models.DecimalField('Luz', max_digits=10, decimal_places=2)
    custo = models.DecimalField('Custo', max_digits=10, decimal_places=2, default=0.00, editable=False)
    numero_por_dia = models.IntegerField('Pratos vendidos por dia', default=1)

    @property
    def numero_funcionarios(self):
        numero_funcionarios = Funcionario.objects.filter(loja_associada=self).count()
        return numero_funcionarios
    
    def calcular_custo_total(self):
        total = self.aluguel + self.agua + self.luz
        funcionarios = Funcionario.objects.filter(loja_associada=self, ativo=True)
        for funcionario in funcionarios:
            total += funcionario.salario
        return total

    @property
    def custo_por_prato(self):
        custo_indiretos = sum(c.valor for c in CustoIndireto.objects.all())
        if self.numero_por_dia > 0:
            return (self.calcular_custo_total() + custo_indiretos) / self.numero_por_dia
        return 0

    def save(self, *args, **kwargs):
        self.endereco = self.endereco.lower()
        self.custo = self.calcular_custo_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.endereco

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['endereco']
