# views.py

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from .models import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.views import View
from .forms import *


def generate_invoice(request, sacola_id):
    # Retrieve the sacola and its products
    sacola = PedidoProduto.objects.get(id=sacola_id)
    sacola_produtos = PedidoProduto.objects.filter(sacola=sacola)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sacola_{sacola.id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2 * cm, height - 2 * cm, f"Sacola {sacola.id}")

    # Draw the table header
    p.setFont("Helvetica-Bold", 12)
    headers = ["Ref", "Descrição", "Quant", "Preço"]
    x_offsets = [2 * cm, 4 * cm, 12 * cm, 16 * cm]
    for i, header in enumerate(headers):
        p.drawString(x_offsets[i], height - 4 * cm, header)

    # Draw lines for the table header
    p.line(2 * cm, height - 4.2 * cm, width - 2 * cm, height - 4.2 * cm)

    # Draw the table rows
    p.setFont("Helvetica", 12)
    y = height - 5 * cm
    for produto in sacola_produtos:
        p.drawString(x_offsets[0], y, str(produto.produto.referencia))
        p.drawString(x_offsets[1], y, produto.produto.nome)
        p.drawString(x_offsets[2], y, str(produto.quantidade))
        p.drawString(x_offsets[3], y, f'R$ {produto.produto.preco_venda:.2f}')
        y -= 1 * cm

    # Draw lines for the table rows
    p.line(2 * cm, y + 1 * cm + 0.2 * cm, width - 2 * cm, y + 1 * cm + 0.2 * cm)
    for i in range(len(sacola_produtos)):
        p.line(2 * cm, y + (i + 1) * cm + 0.2 * cm, width - 2 * cm, y + (i + 1) * cm + 0.2 * cm)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response


class IndexView(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)
    
class ProdutoView(View):
    template_name = 'produto.html'

    def get(self, request):
        produtos = Produto.objects.all()
        form = ProdutoForm()  # Instancia o formulário vazio para ser usado no template
        return render(request, self.template_name, {'produtos': produtos, 'form': form})

    def post(self, request):
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva os dados do formulário no banco de dados
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto')
        else:
            # Se o formulário não for válido, você pode fazer algo, como renderizar novamente o template com erros
            messages.error(request, 'Erro ao cadastrar o produto. Verifique os dados inseridos.')
            return render(request, self.template_name, {'form': form})

    def delete(self, request):
        referencia = request.POST.get('referencia')
        Produto.objects.filter(referencia=referencia).delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('produto')

    def update(self, request):
        referencia = request.POST.get('referencia')
        produto = Produto.objects.get(referencia=referencia)
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produto')
        else:
            messages.error(request, 'Erro ao atualizar o produto. Verifique os dados inseridos.')
            return render(request, self.template_name, {'form': form})
    