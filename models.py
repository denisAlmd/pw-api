from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator
import datetime

class Cliente(BaseModel):
    nome: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)

    @field_validator("nome", "email")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Campo obrigatório não pode ser vazio")
        return v

class Endereco(BaseModel):
    rua: str = Field(..., min_length=1)
    numero: str = Field(..., min_length=1)
    cidade: str = Field(..., min_length=1)
    estado: str = Field(..., min_length=1)
    cep: str = Field(..., min_length=4)
    complemento: Optional[str] = None

    @field_validator("rua", "numero", "cidade", "estado", "cep")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Campo obrigatório não pode ser vazio")
        return v

class Item(BaseModel):
    produto_id: Optional[int] = None
    nome: Optional[str] = None
    quantidade: int = Field(..., gt=0)

    @field_validator("nome", mode="before")
    def produto_id_ou_nome(cls, v, info):
        values = info.data
        if not v and not values.get("produto_id"):
            raise ValueError("é necessário 'produto_id' ou 'nome'")
        return v

    @field_validator("nome")
    def nome_not_empty(cls, v, info):
        if v is not None and not v.strip():
            raise ValueError("Nome do item não pode ser vazio")
        return v

class PixPagamento(BaseModel):
    tipo: Literal["pix"] = "pix"
    pix_key: str = Field(..., min_length=1)

    @field_validator("pix_key")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("pix_key não pode ser vazio")
        return v

class CardPagamento(BaseModel):
    tipo: Literal["card"] = "card"
    card_number: str = Field(..., min_length=13, max_length=19)
    card_holder: str = Field(..., min_length=1)
    exp_month: int = Field(..., ge=1, le=12)
    exp_year: int
    cvv: str = Field(..., min_length=3, max_length=4)

    @field_validator("card_number", "card_holder", "cvv")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Campo obrigatório não pode ser vazio")
        return v

    @field_validator("exp_year")
    def year_not_past(cls, v):
        current = datetime.datetime.utcnow().year
        if v < current:
            raise ValueError("cartão vencido")
        return v

Pagamento = Union[PixPagamento, CardPagamento]

class Order(BaseModel):
    cliente: Cliente
    endereco: Endereco
    itens: List[Item]
    pagamento: Pagamento

    @field_validator("itens")
    def itens_nao_vazios(cls, v):
        if not v or len(v) == 0:
            raise ValueError("itens deve ser lista não vazia")
        return v