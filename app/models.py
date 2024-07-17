from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now

class Produto(models.Model):
    referencia = models.IntegerField(verbose_name='Referência', unique=True)
    nome = models.CharField(max_length=255, verbose_name='Nome')
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de custo', validators=[MinValueValidator(0)])
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de venda', validators=[MinValueValidator(0)])
    estoque = models.IntegerField(verbose_name='Estoque', validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.nome} (Ref: {self.referencia})'

class Pedido(models.Model):
    identificador = models.IntegerField(verbose_name='Identificador da Sacola', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido {self.identificador}'

class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='produtos', related_query_name='produto')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='pedidos', related_query_name='pedido')
    quantidade = models.IntegerField(verbose_name='Quantidade', validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto na sacola'
        verbose_name_plural = 'Produtos na sacola'

    def __str__(self):
        return f'{self.produto.nome} x {self.quantidade}'

class Venda(models.Model):
    sacola = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='vendas', related_query_name='venda')
    qtd_sacola = models.IntegerField(verbose_name='Quantidade Sacola', validators=[MinValueValidator(1)])
    data_de_entrega = models.DateField(verbose_name='Data de Entrega')
    data_de_vencimento = models.DateField(verbose_name='Data de Vencimento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f'Venda para sacola {self.sacola.identificador}'


    def get_valor_total(self):
        total_pedido = sum(item.produto.preco_venda * item.quantidade for item in self.sacola.produtos.all())
        return total_pedido * self.qtd_sacola