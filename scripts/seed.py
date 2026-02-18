from decimal import Decimal

from app.db.session import SessionLocal
from app.models import (
    Customer,
    Product,
    Sku,
    Inventory,
)


def run():
    db = SessionLocal()

    try:
        print("Seeding database...")

        # ----------------------------
        # 1) Create Customers
        # ----------------------------
        customer1 = Customer(
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            status="ACTIVE",
        )

        customer2 = Customer(
            email="alice@example.com",
            first_name="Alice",
            last_name="Smith",
            status="ACTIVE",
        )

        db.add_all([customer1, customer2])
        db.flush()  # Flush to get IDs without committing

        print("Inserted customers")

        # ----------------------------
        # 2) Create Products
        # ----------------------------
        product1 = Product(
            name="MacBook Pro",
            description="Apple laptop",
            status="ACTIVE",
        )

        product2 = Product(
            name="Gaming Mouse",
            description="RGB mouse",
            status="ACTIVE",
        )

        db.add_all([product1, product2])
        db.flush()

        print("Inserted products")

        # ----------------------------
        # 3) Create SKUs
        # ----------------------------
        sku1 = Sku(
            product_id=product1.id,
            sku_code="MBP-16-512",
            title="MacBook Pro 16 512GB",
            price_amount=Decimal("2499.00"),
            price_currency="USD",
            status="ACTIVE",
        )

        sku2 = Sku(
            product_id=product2.id,
            sku_code="MOUSE-RGB-01",
            title="RGB Gaming Mouse",
            price_amount=Decimal("79.99"),
            price_currency="USD",
            status="ACTIVE",
        )

        db.add_all([sku1, sku2])
        db.flush()

        print("Inserted skus")

        # ----------------------------
        # 4) Create Inventory
        # ----------------------------
        inventory1 = Inventory(
            sku_id=sku1.id,
            on_hand=10,
            reserved=0,
        )

        inventory2 = Inventory(
            sku_id=sku2.id,
            on_hand=100,
            reserved=0,
        )

        db.add_all([inventory1, inventory2])

        db.commit()

        print("Inventory inserted")
        print("Seeding completed successfully")

    except Exception as e:
        db.rollback()
        print("Error occurred:", e)
    finally:
        db.close()


if __name__ == "__main__":
    run()
