import os
import requests as req
import json

def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def nova_ordem():
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
            "quantidade": 2
            },
            {
            "produto_id": 2,
            "nome": "Outro Produto",
            "quantidade": 1
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
    try:
        response = req.post(url, json=order_data)
        response_data = response.json()
    except req.RequestException as e:
        print(f"Erro de conexão com a API: {str(e)}\n Sua API está rodando? Verifique se o servidor está ativo e tente novamente.")
        return
    except Exception as e:
        print(f"Erro ao enviar o pedido: {str(e)}")
        response_data = {"error": f"Erro ao enviar o pedido: {str(e)}"}

    if not response_data:
        print("Resposta vazia recebida do servidor.")
        response_data = {"error": "Resposta vazia recebida do servidor."}

    try:
        folder_path = "respostas/"
        os.makedirs(folder_path, exist_ok=True)
        count = len(os.listdir(folder_path)) + 1
        file_name = f"ordem_criada_{count}.json"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)
            print(f"Resposta salva em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar a resposta: {str(e)}")
        response_data["error"] = f"Erro ao salvar a resposta: {str(e)}"

def get_ordem(order_id: str):
    url = f"http://localhost:8000/orders/{order_id}"
    try:
        response = req.get(url)
        response_data = response.json()
    except req.RequestException as e:
        print(f"Erro de conexão com a API: {str(e)}\n Sua API está rodando? Verifique se o servidor está ativo e tente novamente.")
        return
    except Exception as e:
        print(f"Erro ao obter o pedido: {str(e)}")
        response_data = {"error": f"Erro ao obter o pedido: {str(e)}"}

    if not response_data:
        print("Resposta vazia recebida do servidor.")
        response_data = {"error": "Resposta vazia recebida do servidor."}

    try:
        folder_path = "respostas/get/"
        os.makedirs(folder_path, exist_ok=True)
        count = len(os.listdir(folder_path)) + 1
        file_name = f"ordem_obtida_{count}.json"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)
            print(f"Resposta salva em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar a resposta: {str(e)}")
        response_data["error"] = f"Erro ao salvar a resposta: {str(e)}"

def update_ordem(order_id: str):
    url = f"http://localhost:8000/orders/{order_id}"
    order_data = {
        "cliente": {
            "nome": "Maria Oliveira",
            "email": "maria@email.com"
        },
        'itens': [
            {
                "produto_id": 1,
                "nome": "Produto Exemplo",
                "quantidade": 3
            },
            {
                "produto_id": 3,
                "nome": "Novo Produto",
                "quantidade": 2
            }
        ]
    }

    try:
        response = req.put(url, json=order_data)
        response_data = response.json()
    except req.RequestException as e:
        print(f"Erro de conexão com a API: {str(e)}\n Sua API está rodando? Verifique se o servidor está ativo e tente novamente.")
        return
    except Exception as e:
        print(f"Erro ao atualizar o pedido: {str(e)}")
        response_data = {"error": f"Erro ao atualizar o pedido: {str(e)}"}

    if not response_data:
        print("Resposta vazia recebida do servidor.")
        response_data = {"error": "Resposta vazia recebida do servidor."}

    try:
        folder_path = "respostas/update/"
        os.makedirs(folder_path, exist_ok=True)
        count = len(os.listdir(folder_path)) + 1
        file_name = f"ordem_atualizada_{count}.json"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)
            print(f"Resposta salva em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar a resposta: {str(e)}")
        response_data["error"] = f"Erro ao salvar a resposta: {str(e)}"

def main():
    clear_console()
    #nova_ordem()
    #get_ordem("f261d7f0-59dd-483a-b47b-d9087d3851e5")
    update_ordem("c3caebc3-4e1b-433e-83a3-770f675d59f1")

if __name__ == "__main__":
    main()