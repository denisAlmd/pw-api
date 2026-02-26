import json

class OrdersStore:
    def __init__(self):
        self.filename = "orders.json"

    def save_order(self, order_id: str, order_data: dict) -> None:
        orders = self._get_orders()
        orders[order_id] = order_data
        with open(self.filename, "w") as f:
            json.dump(orders, f, indent=4)

    def _get_orders(self) -> dict:
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
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
                with open(self.filename, "w") as f:
                    json.dump(orders, f, indent=4)
            else:
                raise Exception("Pedido não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao atualizar o pedido: {str(e)}")