import requests as req
import json

def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_console()
    url = "http://localhost:8000/orders"
    order_data = {
        "cliente": {
            "nome": "João da Silva",
            "email": "joao@email.com"
        },
        "endereco": {
            "rua": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01234-567",
            "complemento": "Apto 45"
        },
        "itens": [
            {
            "produto_id": 1,
            "nome": "Produto Exemplo",
            "quantidade": 2,
            "preco_unitario": 19.99
            },
            {
            "produto_id": 2,
            "nome": "Outro Produto",
            "quantidade": 1,
            "preco_unitario": 29.99
            }
        ],
        "pagamento": {
            "tipo": "card",
            "card_number": "1234567890123456",
            "card_holder": "João da Silva",
            "exp_month": 12,
            "exp_year": 2026,
            "cvv": "123"
        }
        }
    
    response = req.post(url, json=order_data)
    response_data = response.json()
    response_data["status_code"] = response.status_code
    print(json.dumps(response_data, indent=4))

if __name__ == "__main__":
    clear_console()
    main()