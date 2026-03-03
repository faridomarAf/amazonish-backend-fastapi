from sqlalchemy import select
from datetime import datetime

from app.db.session import SessionLocal
from app.models import OutboxEvent, Order, Inventory
from app.workers.celery_app import celery_app


@celery_app.task
def process_outbox():
    with SessionLocal() as db:

        events = db.scalars(
            select(OutboxEvent)
            .where(OutboxEvent.published_at.is_(None))
        ).all()

        for event in events:

            if event.event_type == "OrderCreated":
                handle_order_created(db, event)

            event.published_at = datetime.utcnow()

        db.commit()


def handle_order_created(db, event):
    payload = event.payload
    order_id = payload["order_id"]

    order = db.get(Order, order_id)

    if not order:
        return

    # Simulate payment success
    order.status = "PAID"

    # Capture inventory (reduce on_hand, reduce reserved)
    items = order.order_items

    for item in items:
        inventory = db.get(Inventory, item.sku_id)

        inventory.on_hand -= item.qty
        inventory.reserved -= item.qty
