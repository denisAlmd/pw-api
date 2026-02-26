from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.routes import router

app = FastAPI(
    title="PW API de Pedidos",
    description="API para pedidos com cliente, endereço, itens e pagamento.",
    version="1.0.0"
)

app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "campo": ".".join(str(loc) for loc in err["loc"] if isinstance(loc, str)),
            "mensagem": err["msg"]
        })
    return JSONResponse(
        status_code=422,
        content={"erro_validacao": errors}
    )