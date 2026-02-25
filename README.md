# API - Guia de Uso

Bem-vindo à sua API! Este guia explica como instalar, rodar e consumir os endpoints principais.

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone <seu-repositorio>
   cd <seu-repositorio>
   ```

2. **Crie e ative o ambiente virtual:**
   ```sh
   python -m venv .pw-api
   .pw-api\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

## Como rodar a API

Execute o servidor com:

```sh
uvicorn main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Estrutura dos Endpoints
- **POST /orders**  
  Recebe uma order(pedido) (json) e processa

> Consulte a documentação automática em `/docs` para ver todos os endpoints disponíveis e exemplos de uso.

## Testes

Execute os testes com:

```sh
pytest
```

## Observações

- Modifique o arquivo `main.py` para adicionar ou alterar endpoints.
- As rotas podem estar organizadas em submódulos, como `api/routes.py`.

---