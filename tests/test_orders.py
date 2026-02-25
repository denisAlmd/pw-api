from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order_pix():
    payload = {
        "cliente": {"nome": "João", "email": "joao@email.com"},
        "endereco": {
            "rua": "Rua A",
            "numero": "123",
            "cidade": "Cidade",
            "estado": "UF",
            "cep": "12345-678"
        },
        "itens": [
            {"produto_id": 1, "quantidade": 2, "preco_unitario": 10.0},
            {"nome": "Produto X", "quantidade": 1, "preco_unitario": 5.5}
        ],
        "pagamento": {
            "tipo": "pix",
            "pix_key": "chavepix123"
        }
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "received"
    assert data["total"] == 25.5
    assert "order_id" in data
    assert data["pagamento"]["tipo"] == "pix"
    assert "pix_key" in data["pagamento"]

def test_create_order_card():
    payload = {
        "cliente": {"nome": "Maria", "email": "maria@email.com"},
        "endereco": {
            "rua": "Rua B",
            "numero": "456",
            "cidade": "Cidade",
            "estado": "UF",
            "cep": "98765-432"
        },
        "itens": [
            {"produto_id": 2, "quantidade": 1, "preco_unitario": 20.0}
        ],
        "pagamento": {
            "tipo": "card",
            "card_number": "1234567890123456",
            "card_holder": "Maria",
            "exp_month": 12,
            "exp_year": 2099,
            "cvv": "123"
        }
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "received"
    assert data["total"] == 20.0
    assert "order_id" in data
    assert data["pagamento"]["tipo"] == "card"
    assert "card_number" not in data["pagamento"]

def test_create_order_invalid_item():
    payload = {
        "cliente": {"nome": "João", "email": "joao@email.com"},
        "endereco": {
            "rua": "Rua A",
            "numero": "123",
            "cidade": "Cidade",
            "estado": "UF",
            "cep": "12345-678"
        },
        "itens": [],
        "pagamento": {
            "tipo": "pix",
            "pix_key": "chavepix123"
        }
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 422
    assert "itens deve ser lista não vazia" in response.text

def test_create_order_missing_payment():
    payload = {
        "cliente": {"nome": "João", "email": "joao@email.com"},
        "endereco": {
            "rua": "Rua A",
            "numero": "123",
            "cidade": "Cidade",
            "estado": "UF",
            "cep": "12345-678"
        },
        "itens": [
            {"produto_id": 1, "quantidade": 2, "preco_unitario": 10.0}
        ]
        # pagamento faltando
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 422
    assert "pagamento" in response.text