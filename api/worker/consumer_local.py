import pika
import json
import time

def callback(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"[x] Processando pedido: {pedido['produto']} x {pedido['quantidade']}")
    time.sleep(3)
    print("[✓] Pedido concluído")

# Usando localhost para teste local
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='fila_pedidos')

print('[*] Aguardando pedidos...')
channel.basic_consume(queue='fila_pedidos', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
