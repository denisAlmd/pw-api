from fastapi import APIRouter, HTTPException, status
from typing import Any
import uuid

from models import Order, OrderUpdate
from orders_store import OrdersStore

orders_store = OrdersStore()
router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order) -> Any:
    print(f"Recebido pedido: {order.model_dump()}")
    try:
        order_id = str(uuid.uuid4())

        saved_order = orders_store.save_order(order_id, order.model_dump())

        pagamento_out: dict = saved_order.get("pagamento", {})
        if pagamento_out.get("tipo") == "card":
            pagamento_out.pop("card_number", None)

        return {
            "order_id": order_id,
            "cliente": saved_order.get("cliente"),
            "endereco": saved_order.get("endereco"),
            "itens": saved_order.get("itens"),
            "pagamento": pagamento_out,
            "status": saved_order.get("status,", "created")
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar o pedido: {str(e)}"
        )
    
@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order(order_id: str) -> Any:
    try:
        order_data = orders_store.get_order(order_id)
        
        if not order_data:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        pagamento_out: dict = order_data.get("pagamento", {})
        if pagamento_out.get("tipo") == "card":
            pagamento_out.pop("card_number", None)

        return {
            "cliente": order_data.get("cliente"),
            "endereco": order_data.get("endereco"),
            "itens": order_data.get("itens"),
            "pagamento": pagamento_out,
            "status": order_data.get("status", "unknown")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao obter o pedido: {str(e)}"
        )

@router.put("/orders/{order_id}", status_code=status.HTTP_200_OK)
def update_order(order_id: str, order: OrderUpdate) -> Any:    
    try:
        order_dict: dict = order.model_dump(exclude_unset=True)
        
        if not order_dict:
            permitted_fields = [field for field in OrderUpdate.model_fields if field != "order_id"]
            raise HTTPException(status_code=400, detail="Nenhum campo válido para atualização foi fornecido. Campos permitidos para atualização: " + ", ".join(permitted_fields))
        
        updated_order = orders_store.update_order(order_id, order_dict)
        return updated_order
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar o pedido: {str(e)}"
        )