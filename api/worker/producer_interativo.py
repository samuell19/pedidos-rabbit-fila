import pika
import json
import sys
from datetime import datetime

class PedidoProducer:
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = None
        self.channel = None
        
    def conectar(self):
        """Conecta ao RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='fila_pedidos')
            print(f"✅ Conectado ao RabbitMQ em {self.host}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar ao RabbitMQ: {e}")
            return False
    
    def enviar_pedido(self, produto, quantidade):
        """Envia um pedido para a fila"""
        if not self.channel:
            print("❌ Não conectado ao RabbitMQ")
            return False
            
        try:
            pedido = {
                'produto': produto,
                'quantidade': quantidade,
                'timestamp': datetime.now().isoformat(),
                'id': f"pedido_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            message = json.dumps(pedido, indent=2)
            self.channel.basic_publish(
                exchange='', 
                routing_key='fila_pedidos', 
                body=message
            )
            
            print(f"📦 Pedido enviado:")
            print(f"   • Produto: {produto}")
            print(f"   • Quantidade: {quantidade}")
            print(f"   • ID: {pedido['id']}")
            print(f"   • Timestamp: {pedido['timestamp']}")
            print()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar pedido: {e}")
            return False
    
    def fechar_conexao(self):
        """Fecha a conexão com RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("🔌 Conexão fechada")

def menu_interativo():
    """Menu interativo para enviar pedidos"""
    producer = PedidoProducer()
    
    if not producer.conectar():
        return
    
    print("\n" + "="*50)
    print("🛒 SISTEMA DE PEDIDOS - PRODUCER")
    print("="*50)
    
    try:
        while True:
            print("\nOpções:")
            print("1. 📦 Enviar pedido personalizado")
            print("2. 🚀 Enviar pedido rápido (pré-definido)")
            print("3. 📊 Enviar múltiplos pedidos de teste")
            print("4. ❌ Sair")
            
            opcao = input("\nEscolha uma opção (1-4): ").strip()
            
            if opcao == "1":
                produto = input("Digite o produto: ").strip()
                try:
                    quantidade = int(input("Digite a quantidade: ").strip())
                    producer.enviar_pedido(produto, quantidade)
                except ValueError:
                    print("❌ Quantidade deve ser um número!")
                    
            elif opcao == "2":
                pedidos_rapidos = [
                    ("Notebook Dell", 1),
                    ("Mouse Gamer", 3),
                    ("Teclado Mecânico", 2),
                    ("Monitor 24\"", 1),
                    ("Headset", 2)
                ]
                
                print("\nPedidos disponíveis:")
                for i, (prod, qtd) in enumerate(pedidos_rapidos, 1):
                    print(f"{i}. {prod} (x{qtd})")
                
                try:
                    escolha = int(input("Escolha um pedido (1-5): ")) - 1
                    if 0 <= escolha < len(pedidos_rapidos):
                        produto, quantidade = pedidos_rapidos[escolha]
                        producer.enviar_pedido(produto, quantidade)
                    else:
                        print("❌ Opção inválida!")
                except ValueError:
                    print("❌ Digite um número válido!")
                    
            elif opcao == "3":
                try:
                    num_pedidos = int(input("Quantos pedidos enviar? "))
                    produtos_teste = [
                        "Smartphone", "Tablet", "Notebook", "Smartwatch", 
                        "Fone Bluetooth", "Carregador", "Cabo USB", "SSD"
                    ]
                    
                    print(f"\n🚀 Enviando {num_pedidos} pedidos de teste...")
                    for i in range(num_pedidos):
                        import random
                        produto = random.choice(produtos_teste)
                        quantidade = random.randint(1, 5)
                        producer.enviar_pedido(f"{produto} #{i+1}", quantidade)
                        
                    print(f"✅ {num_pedidos} pedidos enviados!")
                except ValueError:
                    print("❌ Digite um número válido!")
                    
            elif opcao == "4":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida!")
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    finally:
        producer.fechar_conexao()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--simples":
        # Modo simples (como o original)
        producer = PedidoProducer()
        if producer.conectar():
            producer.enviar_pedido("Notebook Dell", 2)
            producer.fechar_conexao()
    else:
        # Modo interativo
        menu_interativo()
