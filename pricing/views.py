from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = "index.html"

class IngredienteListView(ListView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_list.html'
    context_object_name = 'ingredientes'
    paginate_by = 8

class IngredienteCreateView(CreateView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_form.html'
    form_class = IngredienteForm
    success_url = '/ingredientes/'
    
class IngredienteUpdateView(UpdateView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_form.html'
    form_class = IngredienteForm
    success_url = '/ingredientes/'

class IngredienteDeleteView(DeleteView):
    model = Ingrediente
    template_name = 'ingrediente/ingredient_confirm_delete.html'
    success_url = '/ingredientes/'

class ReceitaListView(ListView):
    model = Receita
    template_name = 'receita/receita_list.html'
    context_object_name = 'receitas'
    paginate_by = 8

class ReceitaCreateView(CreateView):
    model = Receita
    template_name = 'receita/receita_form.html'
    form_class = ReceitaForm
    success_url = reverse_lazy('receita-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente.objects.all()
        return context
    
    def post(self, request):
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save()
            ingredientes_ids = request.POST.getlist('ingredientes')
            quantidades = request.POST.getlist('quantidades')
            for ingrediente_id, quantidade in zip(ingredientes_ids, quantidades):
                ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
                QuantidadeIngrediente.objects.create(receita=receita, ingrediente=ingrediente, quantidade=quantidade)
            return redirect('receita-list')
        return redirect('receita-create')


class ReceitaDetailView(DetailView):
    model = Receita
    template_name = 'receita/receita_detail.html'
    context_object_name = 'receita'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = self.object.quantidadeingrediente_set.filter(receita=self.object)
        return context

class ReceitaUpdateView(UpdateView):
    model = Receita
    template_name = 'receita/receita_update.html'
    form_class = ReceitaForm
    success_url = reverse_lazy('receita-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente.objects.all()
        context['quantidade_ingredientes'] = self.object.quantidadeingrediente_set.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            receita = form.save()
            receita.quantidadeingrediente_set.all().delete()
            ingredientes_ids = request.POST.getlist('ingredientes[]')
            quantidades = request.POST.getlist('quantidades[]')
            for ingrediente_id, quantidade in zip(ingredientes_ids, quantidades):
                if ingrediente_id and quantidade:
                    ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
                    QuantidadeIngrediente.objects.create(receita=receita, ingrediente=ingrediente, quantidade=quantidade)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

        
class ReceitaDeleteView(DeleteView):
    model = Receita
    template_name = 'receita/receita_confirm_delete.html'
    success_url = reverse_lazy('receita-list')

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
    template_name = 'funcionario/funcionario_list.html'
    context_object_name = 'funcionarios'

class FuncionarioCreateView(CreateView):
    model = Funcionario
    template_name = 'funcionario/funcionario_form.html'
    form_class = FuncionarioForm
    success_url = '/funcionarios/'

class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    template_name = 'funcionario/funcionario_form.html'
    form_class = FuncionarioUpdateForm
    success_url = '/funcionarios/'

class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'funcionario/funcionario_confirm_delete.html'
    success_url = '/funcionarios/'

class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'funcionario_detail.html'
    context_object_name = 'funcionario'

class LojasListView(ListView):
    model = Lojas
    template_name = 'loja/loja_list.html'
    context_object_name = 'lojas'

class LojasDetailView(DetailView):
    model = Lojas
    template_name = 'loja/loja_detail.html'
    context_object_name = 'loja'
    
class LojasCreateView(CreateView):
    model = Lojas
    template_name = 'loja/loja_form.html'
    form_class = LojaForm
    success_url = '/lojas/'

class LojasUpdateView(UpdateView):
    model = Lojas
    template_name = 'loja/loja_form.html'
    form_class = LojaForm
    success_url = '/lojas/'

class LojasDeleteView(DeleteView):
    model = Lojas
    template_name = 'loja/loja_confirm_delete.html'
    success_url = '/lojas/'
    