from fastapi import APIRouter, HTTPException, status
from typing import Any
import uuid

from models import Order
from orders_store import OrdersStore

orders_store = OrdersStore()

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order) -> Any:
    print(f"Recebido pedido: {order}")
    try:
        total = sum(item.quantidade * item.preco_unitario for item in order.itens)
        order_id = str(uuid.uuid4())

        saved_order = orders_store.save_order(order_id, order.model_dump())

        # Remove o número do cartão da resposta, se necessário
        pagamento_out:dict = saved_order.get("pagamento", {})
        if pagamento_out.get("tipo") == "card":
            pagamento_out.pop("card_number", None)

        return {
            "order_id": order_id,
            "cliente": saved_order.get("cliente"),
            "endereco": saved_order.get("endereco"),
            "itens": saved_order.get("itens"),
            "pagamento": pagamento_out,
            "total": total
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar o pedido: {str(e)}"
        )

@router.put("/orders/{order_id}", status_code=status.HTTP_200_OK)
def update_order(order_id: str, order: Order) -> Any:
    try:
        # Atualiza o pedido no armazenamento
        orders_store.update_order(order_id, order.model_dump())

        return {
            "order_id": order_id,
            "status": "updated",
            "cliente": order.cliente.model_dump(),
            "endereco": order.endereco.model_dump(),
            "itens": [item.model_dump() for item in order.itens],
            "pagamento": order.pagamento.model_dump(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar o pedido: {str(e)}"
        )