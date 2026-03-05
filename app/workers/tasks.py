# from sqlalchemy import select
# from datetime import datetime
# import random

# from app.db.session import SessionLocal
# from app.models import OutboxEvent, Order, Inventory, Shipment
# from app.workers.celery_app import celery_app


# @celery_app.task(bind=True, name="app.workers.tasks.process_outbox")
# def process_outbox(self):
#     with SessionLocal() as db:

#         # Fetch all unprocessed events
#         events = db.execute(
#             select(OutboxEvent).where(OutboxEvent.published_at.is_(None))
#         ).scalars().all()

#         for event in events:
#             try:
#                 if event.event_type == "OrderCreated":
#                     handle_order_created(db, event)

#                 # mark event as published
#                 event.published_at = datetime.utcnow()
#                 db.commit()
#             except Exception as e:
#                 db.rollback()
#                 print(f"Error processing event {event.id}: {e}")

#     def handle_order_created(db, event):
#         payload = event.payload
#         order_id = payload["order_id"]

#         order = db.get(Order, order_id)
#         if not order:
#             return

#         # simulate payment success/failure
#         payment_success = random.random() > 0.2  # 80% chance

#         if payment_success:
#             order.status = "PAID"

#             # capture inventory
#             for item in order.order_items:
#                 inventory = db.get(Inventory, item.sku_id)
#                 inventory.on_hand -= item.qty
#                 inventory.reserved -= item.qty

#             # create shipment
#             shipment = Shipment(
#                 order_id=order.id,
#                 carrier="DHL",
#                 tracking_number=f"TRK-{order.id}-{random.randint(1000,9999)}"
#             )
#             db.add(shipment)
#         else:
#             order.status = "CANCELLED"

#             # release inventory
#             for item in order.order_items:
#                 inventory = db.get(Inventory, item.sku_id)
#                 inventory.reserved -= item.qty

#         print(f"[DEBUG] Processing event {event.id} for order {order_id}")


from sqlalchemy import select
from datetime import datetime
import random

from app.db.session import SessionLocal
from app.models import OutboxEvent, Order, Inventory, Shipment
from app.workers.celery_app import celery_app


# ---- Helper function must be top-level ----
def handle_order_created(db, event):
    payload = event.payload
    order_id = payload["order_id"]

    order = db.get(Order, order_id)
    if not order:
        print(f"[WARNING] Order {order_id} not found")
        return

    # simulate payment success/failure
    payment_success = random.random() > 0.2  # 80% chance

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
            tracking_number=f"TRK-{order.id}-{random.randint(1000,9999)}"
        )
        db.add(shipment)
        print(f"[DEBUG] Order {order_id} PAID and shipment created")
    else:
        order.status = "CANCELLED"

        # release inventory
        for item in order.order_items:
            inventory = db.get(Inventory, item.sku_id)
            inventory.reserved -= item.qty
        print(f"[DEBUG] Order {order_id} CANCELLED and inventory released")

    # Final debug
    print(f"[DEBUG] Processing event {event.id} for order {order_id}")


# ---- Celery task ----
@celery_app.task(bind=True, name="app.workers.tasks.process_outbox")
def process_outbox(self):
    with SessionLocal() as db:

        # Fetch all unprocessed events
        events = db.execute(
            select(OutboxEvent).where(OutboxEvent.published_at.is_(None))
        ).scalars().all()

        for event in events:
            try:
                if event.event_type == "OrderCreated":
                    handle_order_created(db, event)

                # mark event as published
                event.published_at = datetime.utcnow()
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"[ERROR] Error processing event {event.id}: {e}")
