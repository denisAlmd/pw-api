from fastapi import APIRouter, HTTPException, status
from typing import Any
import uuid

from models import Order

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order) -> Any:
    try:
        # Calcula o valor total do pedido
        total = sum(item.quantidade * item.preco_unitario for item in order.itens)
        order_id = str(uuid.uuid4())

        # Remove o número do cartão da resposta, se for pagamento com cartão
        pagamento_out = order.pagamento.model_dump()
        if getattr(order.pagamento, "tipo", None) == "card":
            pagamento_out.pop("card_number", None)

        return {
            "order_id": order_id,
            "total": total,
            "status": "received",
            "cliente": order.cliente.model_dump(),
            "endereco": order.endereco.model_dump(),
            "itens": [item.model_dump() for item in order.itens],
            "pagamento": pagamento_out,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar o pedido: {str(e)}"
        )