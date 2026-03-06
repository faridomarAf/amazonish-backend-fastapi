# Amazonish Backend

A production-ready **Amazon-like e-commerce backend** built with **FastAPI**, **MySQL**, **Redis**, and **Celery**, implementing safe inventory reservation, order lifecycle, and event-driven architecture.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [Event Flow](#event-flow)
7. [Getting Started](#getting-started)
8. [API Endpoints](#api-endpoints)
9. [Testing](#testing)
10. [Future Improvements](#future-improvements)

---

## Project Overview

This project is a backend for an e-commerce platform with features similar to Amazon:

* User registration & JWT authentication
* Product catalog with SKUs
* Inventory management with safe reservation
* Order creation with transactional integrity (no overselling)
* Event-driven architecture using Outbox pattern & Celery
* Payment simulation & shipment creation

---

## Architecture

```text
                +-------------+
                |   Client    |
                +------+------+
                       |
                       v
               +-------+-------+
               |    FastAPI    |
               |  (API Layer)  |
               +-------+-------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
   +----+----+                 +------+------+
   |  MySQL  |                 |   Redis     |
   |Database |                 | Message Bus |
   +----+----+                 +------+------+
        |                             |
        |                             v
        |                    +--------+--------+
        |                    |  Celery Worker  |
        |                    +--------+--------+
        |                             |
        v                             v
  +-----+-----+               +-------+------+
  |  Orders   |               | Event Handler|
  | Inventory |               | Payments     |
  +-----------+               +--------------+
```

This architecture demonstrates separation of concerns, event-driven workflows, and safe transactional operations.

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** MySQL 8.0 + SQLAlchemy + Alembic
* **Cache / Message Broker:** Redis + Celery
* **Authentication:** JWT using python-jose
* **Password Security:** bcrypt via passlib
* **Testing:** Pytest + HTTPX
* **Containerization:** Docker & Docker Compose
* **Python Version:** 3.12

---

## Project Structure

```text
app/
├── api/                  # Routes and dependencies
│   ├── dependencies/     # Auth, common dependencies
│   └── routes/           # API endpoints: auth, catalog, orders
├── core/                 # Config, security, logging
├── db/                   # SQLAlchemy session and base
├── models/               # Database models
├── schemas/              # Pydantic request/response schemas
├── workers/              # Celery app and tasks
└── main.py               # FastAPI entry point

alembic/                  # DB migrations
scripts/                  # Seed and helper scripts
tests/                     # Unit and integration tests
Dockerfile
docker-compose.yml
.env.example
pyproject.toml
README.md
```

---

## Database Schema

**Tables and relationships:**

* `customers` → registered users
* `products` → product catalog
* `skus` → individual sellable units of a product
* `inventory` → stock levels for SKUs
* `orders` → customer orders
* `order_items` → items within orders
* `shipments` → shipment information
* `outbox_events` → event-driven workflow tracking

Example relational view:

```text
customers
   |
orders
   |
order_items
   |
skus
   |
inventory
shipments
outbox_events
```

---

## Event Flow

```text
OrderCreated (outbox)
      ↓
Celery Worker picks up event
      ↓
Simulate Payment
      ↓
PaymentSucceeded or PaymentFailed
      ↓
If SUCCESS: Order → PAID, Inventory captured, Shipment created
If FAILED: Order → CANCELLED, Inventory released
      ↓
Email notification (future enhancement)
```

---

## Getting Started

### 1. Clone repository

```bash
git clone <your_repo_url>
cd amazonish-backend
```

### 2. Copy environment file

```bash
cp .env.example .env
# Edit .env with your DB, Redis, JWT secrets
```

### 3. Run services with Docker

```bash
docker-compose up --build
```

### 4. Run migrations

```bash
make migrate
```

### 5. Seed sample data

```bash
make seed
```

### 6. Run FastAPI server

```bash
make run
```

### 7. Run Celery worker

```bash
make worker
```

### 8. Access API docs

Open browser: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Authentication

* `POST /auth/register` – Register a new user
* `POST /auth/login` – Login and receive JWT token

### Users

* `GET /users/me` – Get current user info (protected)

### Catalog

* `POST /catalog/products` – Create product
* `GET /catalog/products` – List products
* `POST /catalog/skus` – Create SKU
* `POST /catalog/inventory` – Initialize inventory

### Orders

* `POST /orders` – Create order (safe inventory reservation)

> Use `Authorize` in Swagger to pass JWT token for protected endpoints.

---

## Testing

### Run all tests

```bash
make test
```

### Run specific test files

```bash
pytest tests/test_auth.py
pytest tests/test_catalog.py
pytest tests/test_orders.py
pytest tests/test_health.py
```

### What is tested

* User registration, login, and JWT validation
* Product, SKU creation, and inventory initialization
* Order creation with safe inventory reservation (no overselling)
* Worker and outbox event processing
* Health endpoints

### Notes

* Ensure services are running (`docker-compose up`) before running tests
* Tests use `httpx.AsyncClient` for async endpoints
* Sample data can be seeded using `make seed`

---

## Future Improvements

* Integrate real payment gateway
* Implement email notifications on shipment
* Add idempotency checks for events
* Expand test coverage with edge cases
* Implement logging & observability with structured logs
* Improve Celery with retry and error handling
* Add frontend integration
