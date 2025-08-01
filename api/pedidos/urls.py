from django.urls import path
from . import views

urlpatterns = [
    path('', views.PedidoListView.as_view(), name='listar_pedidos'),
    path('criar/', views.PedidoCreateView.as_view(), name='criar_pedido'),
]
