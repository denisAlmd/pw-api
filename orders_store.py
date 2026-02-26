import json
import os

from models import OrderUpdate

class OrdersStore:
    def __init__(self):
        self.folder_path = "ordens/"

    def save_order(self, order_id: str, order_data: dict) -> dict:
        try:
            order_data['status'] = 'created'
            folder_path = self.folder_path
            os.makedirs(folder_path, exist_ok=True)
            file_name = f"{order_id}.json"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(order_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Não foi possível salvar o pedido! Entre em contato com o suporte. {str(e)}")
        
        return order_data

    def get_order(self, order_id: str) -> dict:
        try:
            file_path = os.path.join(self.folder_path, f"{order_id}.json")
            if not os.path.exists(file_path):
                raise Exception("Pedido não encontrado.")
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Erro ao obter o pedido: {str(e)}")
        
    def update_order(self, order_id: str, order_data: dict) -> dict:
        try:            
            file_path = os.path.join(self.folder_path, f"{order_id}.json")
            
            if not os.path.exists(file_path):
                raise Exception("Pedido não encontrado para atualização.")
            
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data: dict = json.load(f)
            
            existing_data.update(order_data)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)

            if len(order_data.keys()) > 1:
                existing_data['Campos atualizados'] = list(order_data.keys())
            else:
                existing_data['Campo atualizado'] = list(order_data.keys())
            return existing_data
        except Exception as e:
            raise Exception(f"Erro ao atualizar o pedido: {str(e)}")