from django.db import models
from django.urls import reverse
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

class Ingrediente(models.Model):
    UNIDADES_CHOICES = (
        ('g', 'gramas'),
        ('kg', 'quilogramas'),
        ('ml', 'mililitros'),
        ('l', 'litros'),
    )
    nome = models.CharField(max_length=100)
    preco = models.DecimalField('Preço por peso', max_digits=10, decimal_places=2)
    unidade_medida = models.CharField('Preço por unidade', max_length=2, choices=UNIDADES_CHOICES)

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nome']

class Receita(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.ManyToManyField(Ingrediente, through='QuantidadeIngrediente')
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    margem_lucro = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

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
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.ingrediente} - {self.quantidade} na receita {self.receita}'
    
    class Meta:
        verbose_name = 'Quantidade de Ingrediente'
        verbose_name_plural = 'Quantidades de Ingredientes'
        ordering = ['ingrediente']

@receiver(m2m_changed, sender=Receita.ingredientes.through)
@receiver(post_save, sender=QuantidadeIngrediente)
def update_receita_cost(sender, instance, **kwargs):
    if isinstance(instance, Receita):
        receita = instance
    else:
        receita = instance.receita
    receita.custo = receita.custo_ingredientes()
    receita.valor_venda = receita.calcular_valor_venda()
    receita.save()

class CustoIndireto(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nome 
    
    class Meta:
        verbose_name = 'Custo Indireto'
        verbose_name_plural = 'Custos Indiretos'
        ordering = ['nome']

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']

class Lojas(models.Model):
    endereco = models.CharField(max_length=150)
    aluguel = models.DecimalField(max_digits=10, decimal_places=2)
    agua = models.DecimalField(max_digits=10, decimal_places=2)
    luz = models.DecimalField(max_digits=10, decimal_places=2)
    funcionario = models.ManyToManyField(Funcionario)
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    numero_por_dia = models.IntegerField('Pratos vendidos por dia', default=1)

    @property
    def numero_funcionarios(self):
        return self.funcionario.count()
    
    def calcular_custo_total(self):
        total = self.aluguel + self.agua + self.luz
        for funcionario in self.funcionario.all():
            total += funcionario.salario
        return total

    @property
    def custo_por_prato(self):
        custo_indiretos = sum(c.valor for c in CustoIndireto.objects.all())
        if self.numero_por_dia > 0:
            return (self.calcular_custo_total() + custo_indiretos) / self.numero_por_dia
        return 0

    def __str__(self):
        return self.endereco

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['endereco']

@receiver(m2m_changed, sender=Lojas.funcionario.through)
def atualizando_custo_loja_m2m(sender, instance, **kwargs):
    if kwargs.get('action') in ['post_add', 'post_remove', 'post_clear']:
        instance.custo = instance.calcular_custo_total()
        instance.save()

@receiver(post_save, sender=Funcionario)
def update_store_cost_post_save(sender, instance, **kwargs):
    lojas = instance.lojas_set.all()
    for loja in lojas:
        loja.custo = loja.calcular_custo_total()
        loja.save()
