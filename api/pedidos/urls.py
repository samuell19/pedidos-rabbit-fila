from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.PedidoCreateView.as_view(), name='criar_pedido'),
]
