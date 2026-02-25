from decimal import Decimal
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class SkuCreate(BaseModel):
    product_id: int
    sku_code: str
    title: str
    price_amount: Decimal
    price_currency: str


class SkuResponse(BaseModel):
    id: int
    product_id: int
    sku_code: str
    title: str
    price_amount: Decimal
    price_currency: str


class InventoryCreate(BaseModel):
    sku_id: int
    on_hand: int
