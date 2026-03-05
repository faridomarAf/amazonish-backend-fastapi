import uuid
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models import Order, OrderItem, Inventory, Sku, OutboxEvent, Customer
from app.schemas.order import OrderCreate, OrderResponse
from app.api.dependencies.auth import get_current_user
from app.workers.tasks import process_outbox as celery_process_outbox

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse)
def create_order(
    request: OrderCreate,
    current_user: Customer = Depends(get_current_user),
):
    with SessionLocal() as db:
        try:
            total_amount = Decimal("0.00")
            currency = "USD"

            order = Order(
                customer_id=current_user.id,
                status="CREATED",
                total_amount=Decimal("0.00"),
                total_currency=currency,
            )
            db.add(order)
            db.flush()  # assign order.id

            for item in request.items:
                inventory = db.scalar(
                    select(Inventory)
                    .where(Inventory.sku_id == item.sku_id)
                    .with_for_update()
                )
                if not inventory:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Inventory not found for SKU {item.sku_id}"
                    )

                available = inventory.on_hand - inventory.reserved
                if available < item.qty:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for SKU {item.sku_id}"
                    )

                inventory.reserved += item.qty

                sku = db.scalar(select(Sku).where(Sku.id == item.sku_id))
                if not sku:
                    raise HTTPException(
                        status_code=404, detail="SKU not found")

                line_total = sku.price_amount * item.qty
                total_amount += line_total

                order_item = OrderItem(
                    order_id=order.id,
                    sku_id=item.sku_id,
                    qty=item.qty,
                    unit_amount=sku.price_amount,
                    unit_currency=sku.price_currency,
                )
                db.add(order_item)

            order.total_amount = total_amount

            outbox = OutboxEvent(
                event_id=str(uuid.uuid4()),
                aggregate_type="ORDER",
                aggregate_id=order.id,
                event_type="OrderCreated",
                payload={
                    "order_id": order.id,
                    "customer_id": current_user.id,
                    "total_amount": str(total_amount),
                },
            )
            db.add(outbox)

            db.commit()

            celery_process_outbox.delay()

            return OrderResponse(
                id=order.id,
                status=order.status,
                total_amount=order.total_amount,
                total_currency=order.total_currency,
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
