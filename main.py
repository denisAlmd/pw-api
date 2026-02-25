from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="PW API de Pedidos",
    description="API para pedidos com cliente, endereço, itens e pagamento.",
    version="1.0.0"
)

app.include_router(router)