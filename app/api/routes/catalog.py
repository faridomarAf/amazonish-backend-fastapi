from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Product, Sku, Inventory
from app.schemas.catalog import (
    ProductCreate,
    ProductResponse,
    SkuCreate,
    SkuResponse,
    InventoryCreate,
)

router = APIRouter(prefix="/catalog", tags=["catalog"])

# Create Product


@router.post("/products", response_model=ProductResponse)
def create_product(request: ProductCreate):
    with SessionLocal() as db:
        product = Product(
            name=request.name,
            description=request.description,
            status="ACTIVE",
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
        )

# List Products (Public)


@router.get("/products")
def list_products():
    with SessionLocal() as db:
        products = db.scalars(
            select(Product).where(Product.status == "ACTIVE")
        ).all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
            }
            for p in products
        ]

# Create SKU


@router.post("/skus", response_model=SkuResponse)
def create_sku(request: SkuCreate):
    with SessionLocal() as db:

        product = db.scalar(
            select(Product).where(Product.id == request.product_id)
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        sku = Sku(
            product_id=request.product_id,
            sku_code=request.sku_code,
            title=request.title,
            price_amount=request.price_amount,
            price_currency=request.price_currency,
            status="ACTIVE",
        )

        db.add(sku)
        db.commit()
        db.refresh(sku)

        return SkuResponse(
            id=sku.id,
            product_id=sku.product_id,
            sku_code=sku.sku_code,
            title=sku.title,
            price_amount=sku.price_amount,
            price_currency=sku.price_currency,
        )


# Initialize Inventory
@router.post("/inventory")
def create_inventory(request: InventoryCreate):
    with SessionLocal() as db:

        sku = db.scalar(
            select(Sku).where(Sku.id == request.sku_id)
        )

        if not sku:
            raise HTTPException(status_code=404, detail="SKU not found")

        inventory = Inventory(
            sku_id=request.sku_id,
            on_hand=request.on_hand,
            reserved=0,
        )

        db.add(inventory)
        db.commit()

        return {"message": "Inventory created"}
