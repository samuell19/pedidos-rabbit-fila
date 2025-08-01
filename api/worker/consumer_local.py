import pika
import json
import time
import os
import sys
import django

# Configurar Django
sys.path.append('/workspaces/pedidos-rabbit-fila/api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from pedidos.models import Pedido

def callback(ch, method, properties, body):
    pedido_data = json.loads(body)
    print(f"[x] Processando pedido: {pedido_data['produto']} x {pedido_data['quantidade']}")
    
    # Simular processamento
    time.sleep(3)
    
    # Salvar no banco de dados
    try:
        pedido = Pedido.objects.create(
            produto=pedido_data['produto'],
            quantidade=pedido_data['quantidade']
        )
        print(f"[✓] Pedido #{pedido.id} salvo no banco de dados")
        print(f"    • Produto: {pedido.produto}")
        print(f"    • Quantidade: {pedido.quantidade}")
        print(f"    • Criado em: {pedido.criado_em}")
        print("[✓] Processamento concluído\n")
    except Exception as e:
        print(f"[❌] Erro ao salvar no banco: {e}")

# Usando localhost para teste local
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='fila_pedidos')

print('[*] Aguardando pedidos para processar e salvar no banco...')
channel.basic_consume(queue='fila_pedidos', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
