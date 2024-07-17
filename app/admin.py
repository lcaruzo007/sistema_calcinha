from django.contrib import admin
from .models import Produto, Pedido, PedidoProduto, Venda

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'nome', 'preco_custo', 'preco_venda', 'estoque')
    search_fields = ('nome', 'referencia')
    list_filter = ('preco_venda', 'estoque')

class PedidoProdutoInline(admin.TabularInline):
    model = PedidoProduto
    extra = 1
    autocomplete_fields = ['produto']

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'get_total')
    inlines = [PedidoProdutoInline]

    def get_total(self, obj):
        total = sum(item.produto.preco_venda * item.quantidade for item in obj.produtos.all())
        return f'R$ {total:.2f}'
    get_total.short_description = 'Total da Sacola'

class VendaAdmin(admin.ModelAdmin):
    list_display = ('sacola', 'qtd_sacola', 'data_de_entrega', 'data_de_vencimento', 'get_valor_total', 'created_at', 'updated_at')
    search_fields = ('sacola__identificador',)
    list_filter = ('data_de_entrega', 'data_de_vencimento')

    def get_valor_total(self, obj):
        valor_total = obj.get_valor_total()
        return f'R$ {valor_total:.2f}'
    get_valor_total.short_description = 'Valor Total da Venda'

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Venda, VendaAdmin)
