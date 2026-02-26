import json

class OrdersStore:
    def __init__(self):
        self.filename = "orders.json"

    #Lucas, se vc estiver vendo isso, saiba que essa função salva o pedido no arquivo JSON. 
    #Porém, existe um grande risco disso não der certo pq existem muitas operações de leitura e escrita no arquivo, 
    #o que pode causar problemas de concorrência. Para um projeto real, seria melhor usar um banco de dados ou outro tipo de armazenamento mais robusto.
    #Imagina diversos pedidos chegando ao mesmo tempo e tentando acessar o arquivo JSON, isso pode causar corrupção de dados ou perda de informações.
    #Eu poderia melhorar isso usando bloqueios (locks) para garantir que apenas um processo acesse o arquivo de cada vez, 
    #mas isso pode complicar o código e ainda não é a solução ideal para um ambiente de produção.
    def save_order(self, order_id: str, order_data: dict) -> dict:
        try:
            orders = self._get_orders()
            orders[order_id] = order_data
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(orders, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Não foi possível salvar o pedido! Entre em contato com o suporte. {str(e)}")
        
        return orders[order_id]

    def _get_orders(self) -> dict:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return {}

    def get_order(self, order_id: str) -> dict:
        try:
            orders = self._get_orders()
            return orders.get(order_id, {})
        except Exception as e:
            raise Exception(f"Erro ao obter o pedido: {str(e)}")
        
    def update_order(self, order_id: str, order_data: dict) -> None:
        try:
            orders = self._get_orders()
            if order_id in orders:
                orders[order_id] = order_data
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(orders, f, indent=4, ensure_ascii=False)
            else:
                raise Exception("Pedido não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao atualizar o pedido: {str(e)}")