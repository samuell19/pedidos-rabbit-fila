import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PedidoSerializer
from .models import Pedido

class PedidoListView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all().order_by('-criado_em')
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

class PedidoCreateView(APIView):
    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()

            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='fila_pedidos')

            message = json.dumps(serializer.data)
            channel.basic_publish(exchange='', routing_key='fila_pedidos', body=message)
            connection.close()

            return Response({'status': 'Pedido enviado com sucesso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
