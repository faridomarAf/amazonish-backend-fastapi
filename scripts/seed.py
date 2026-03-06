from decimal import Decimal
from contextlib import contextmanager

from app.db.session import SessionLocal
from app.models import Customer, Product, Sku, Inventory, Order, OrderItem


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run():
    with get_db() as db:
        try:
            print("Seeding database...")

            # ----------------------------
            # 1) Create Customers (idempotent)
            # ----------------------------
            customers_data = [
                {"email": "john@example.com",
                    "first_name": "John", "last_name": "Doe"},
                {"email": "alice@example.com",
                    "first_name": "Alice", "last_name": "Smith"}
            ]

            customers = []
            for data in customers_data:
                customer = db.query(Customer).filter_by(
                    email=data["email"]).first()
                if not customer:
                    customer = Customer(
                        email=data["email"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        status="ACTIVE"
                    )
                    db.add(customer)
                    db.flush()
                customers.append(customer)

            print(
                f"Inserted/verified customers: {[c.email for c in customers]}")

            # ----------------------------
            # 2) Create Products (idempotent)
            # ----------------------------
            products_data = [
                {"name": "MacBook Pro", "description": "Apple laptop"},
                {"name": "Gaming Mouse", "description": "RGB mouse"},
                {"name": "USB-C Hub", "description": "Multiport hub"}
            ]

            products = []
            for data in products_data:
                product = db.query(Product).filter_by(
                    name=data["name"]).first()
                if not product:
                    product = Product(
                        name=data["name"],
                        description=data["description"],
                        status="ACTIVE"
                    )
                    db.add(product)
                    db.flush()
                products.append(product)

            print(f"Inserted/verified products: {[p.name for p in products]}")

            # ----------------------------
            # 3) Create SKUs (idempotent)
            # ----------------------------
            skus_data = [
                {"product": products[0], "sku_code": "MBP-16-512",
                    "title": "MacBook Pro 16 512GB", "price_amount": Decimal("2499.00")},
                {"product": products[1], "sku_code": "MOUSE-RGB-01",
                    "title": "RGB Gaming Mouse", "price_amount": Decimal("79.99")},
                {"product": products[2], "sku_code": "HUB-USB-C-01",
                    "title": "USB-C Hub", "price_amount": Decimal("49.99")}
            ]

            skus = []
            for data in skus_data:
                sku = db.query(Sku).filter_by(
                    sku_code=data["sku_code"]).first()
                if not sku:
                    sku = Sku(
                        product_id=data["product"].id,
                        sku_code=data["sku_code"],
                        title=data["title"],
                        price_amount=data["price_amount"],
                        price_currency="USD",
                        status="ACTIVE"
                    )
                    db.add(sku)
                    db.flush()
                skus.append(sku)

            print(f"Inserted/verified SKUs: {[s.sku_code for s in skus]}")

            # ----------------------------
            # 4) Create Inventory (idempotent)
            # ----------------------------
            inventory_data = [
                {"sku": skus[0], "on_hand": 10},
                {"sku": skus[1], "on_hand": 100},
                {"sku": skus[2], "on_hand": 5}
            ]

            for data in inventory_data:
                inv = db.query(Inventory).filter_by(
                    sku_id=data["sku"].id).first()
                if not inv:
                    inv = Inventory(
                        sku_id=data["sku"].id, on_hand=data["on_hand"], reserved=0)
                    db.add(inv)

            db.commit()
            print("Inventory inserted/verified")

            # ----------------------------
            # 5) Optional: Create Sample Order (idempotent)
            # ----------------------------
            existing_order = db.query(Order).filter_by(
                customer_id=customers[0].id).first()
            if not existing_order:
                order = Order(customer_id=customers[0].id, status="PAID")
                db.add(order)
                db.flush()

                order_item = OrderItem(
                    order_id=order.id,
                    sku_id=skus[0].id,
                    qty=1,
                    price_amount=skus[0].price_amount,
                    price_currency=skus[0].price_currency
                )
                db.add(order_item)
                db.commit()
                print(f"Inserted sample order with ID: {order.id}")

            print("Seeding completed successfully")

        except Exception as e:
            db.rollback()
            print("Error occurred during seeding:", e)


if __name__ == "__main__":
    run()
