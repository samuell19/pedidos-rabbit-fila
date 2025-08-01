# Sistema de Pedidos com RabbitMQ e Django

Este é um sistema de gerenciamento de pedidos que utiliza Django REST Framework para a API e RabbitMQ para processamento assíncrono de mensagens.

## Funcionalidades

- API REST para criação de pedidos
- Processamento assíncrono usando RabbitMQ
- Producer interativo para testes
- Consumer para processamento dos pedidos
- Interface administrativa Django

## Tecnologias Utilizadas

- Django 4.2
- Django REST Framework 3.14
- RabbitMQ (via pika 1.3.2)
- SQLite3

## Estrutura do Projeto

```
api/
├── api/                # Configurações principais do Django
├── pedidos/           # App de pedidos
└── worker/            # Scripts do RabbitMQ
    ├── producer_interativo.py
    └── consumer_local.py
```

## Configuração e Instalação

1. Clone o repositório:
```bash
git clone <https://github.com/samuell19/pedidos-rabbit-fia>
cd pedidos-rabbit-fia
```

2. Instale as dependências:
```bash
cd api
pip install -r requirements.txt
```

3. Execute as migrações do Django:
```bash
python manage.py migrate
```

4. Configure o RabbitMQ (usando Docker):
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

## Como Executar

1. Inicie o servidor Django:
```bash
python manage.py runserver
```

2. Inicie o consumer:
```bash
python api/worker/consumer_local.py
```

3. Para testar o producer:
```bash
python api/worker/producer_interativo.py
```

## Endpoints da API

- `POST /api/pedidos/` - Criar novo pedido
- `GET /api/pedidos/` - Listar pedidos
- `GET /api/pedidos/<id>/` - Detalhes do pedido


