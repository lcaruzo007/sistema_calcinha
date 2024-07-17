from django.urls import path
from app.views import *


urlpatterns = [
    path('generate_invoice/<int:sacola_id>/', generate_invoice, name='generate_invoice'),
    path('', IndexView.as_view(), name='index'),
    path('produto/', ProdutoView.as_view(), name='produto'),

    # Add more paths here
]