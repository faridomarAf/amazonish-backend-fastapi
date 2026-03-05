from sqlalchemy import select
from datetime import datetime

from app.db.session import SessionLocal
from app.models import OutboxEvent, Order, Inventory
from app.workers.celery_app import celery_app

import random
from app.models import Shipment


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

    # simulate payment success/failure
    payment_success = random.random() > 0.2   # 80% success

    if payment_success:

        order.status = "PAID"

        # capture inventory
        for item in order.order_items:
            inventory = db.get(Inventory, item.sku_id)

            inventory.on_hand -= item.qty
            inventory.reserved -= item.qty

        # create shipment
        shipment = Shipment(
            order_id=order.id,
            carrier="DHL",
            tracking_number=f"TRK-{order.id}"
        )

        db.add(shipment)

    else:

        order.status = "CANCELLED"

        # release inventory
        for item in order.order_items:
            inventory = db.get(Inventory, item.sku_id)

            inventory.reserved -= item.qty
