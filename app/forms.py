# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Produto, Pedido, PedidoProduto, Venda

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['referencia', 'nome', 'preco_custo', 'preco_venda', 'estoque']
        widgets = {
            'referencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Referência'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Custo'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Venda'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estoque'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['identificador']
        widgets = {
            'identificador': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Identificador da Sacola'}),
        }

class PedidoProdutoForm(forms.ModelForm):
    class Meta:
        model = PedidoProduto
        fields = ['pedido', 'produto', 'quantidade']
        widgets = {
            'pedido': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
        }

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['sacola', 'qtd_sacola', 'data_de_entrega', 'data_de_vencimento']
        widgets = {
            'sacola': forms.Select(attrs={'class': 'form-control'}),
            'qtd_sacola': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade Sacola'}),
            'data_de_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_de_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
