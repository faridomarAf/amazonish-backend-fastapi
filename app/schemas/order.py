from decimal import Decimal
from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):
    sku_id: int
    qty: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: Decimal
    total_currency: str
