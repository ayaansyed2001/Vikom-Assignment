📦 Vikmo – Sales Order & Inventory Lite
📌 Project Overview

This project is a simplified Sales Order & Inventory Management System built using Django REST Framework.
It simulates Vikmo’s core B2B SaaS functionality for auto parts distribution where:
Admin manages products and inventory
Dealers place orders
Stock is automatically validated and deducted
Orders follow a controlled lifecycle
The system ensures transactional consistency, proper stock validation, and structured API design.

🚀 Features Implemented
🧾 Product Management
Create, update, delete products
Unique SKU constraint
Pricing & description fields
Stock displayed in product listing

📊 Inventory Management

One inventory record per product
Manual stock adjustments allowed
Inventory audit trail logging
Stock deducted only on order confirmation

🏢 Dealer Management

Create and manage dealers
Dealers can have multiple orders
Dealer deletion restricted if orders exist

📦 Order Management

Draft → Confirmed → Delivered lifecycle
Auto-generated order numbers (ORD-YYYYMMDD-XXXX)
Multiple order items supported
Automatic line total & order total calculation
Price snapshot preserved at order time
Confirmed/Delivered orders locked from editing
🧠 Business Rules Implemented

✅ Stock Validation

Stock checked before confirmation
Entire order rejected if any item insufficient
Clear error message returned

✅ Stock Deduction

Stock deducted only when order moves from Draft → Confirmed
Implemented using atomic transactions

✅ Status Flow Enforcement

Draft → Confirmed → Delivered
Invalid transitions rejected

✅ Order Editing Rules

Only Draft orders editable
Confirmed/Delivered orders locked
Deleting confirmed order restores stock

🔎 Filtering Support

Orders can be filtered by:
Status
Dealer
Created date range

🛠️ Tech Stack Used

Python 3.10+
Django 4.2+
Django REST Framework
Django Filter
SQLite (default)

🗄️ Database Design
Models Implemented (sales app)

Product
Inventory
Dealer
Order
OrderItem
InventoryAdjustment
Relationships
Product → OneToOne → Inventory
Dealer → OneToMany → Orders
Order → OneToMany → OrderItems
Inventory → OneToMany → InventoryAdjustments

⚙️ Setup Instructions

Follow these steps to run locally:
git clone <your-repository-link>
cd vikmo
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/
🔌 API Documentation

Base URL:

http://127.0.0.1:8000/api/
🧾 Products

GET /api/products/

POST /api/products/

GET /api/products/{id}/

PUT /api/products/{id}/

DELETE /api/products/{id}/

🏢 Dealers

GET /api/dealers/

POST /api/dealers/

GET /api/dealers/{id}/

PUT /api/dealers/{id}/

📦 Orders

GET /api/orders/

POST /api/orders/

GET /api/orders/{id}/

PUT /api/orders/{id}/

DELETE /api/orders/{id}/

POST /api/orders/{id}/confirm/

POST /api/orders/{id}/deliver/

📊 Inventory (Admin)

GET /api/inventory/

POST /api/inventory/

GET /api/inventory/{product_id}/

PUT /api/inventory/{product_id}/

🧪 Demo Scenarios Covered
1️⃣ Successful Order Flow

Create Product

Add Inventory

Create Dealer

Create Draft Order

Confirm Order → Stock deducted

Deliver Order

2️⃣ Insufficient Stock

Create order requesting more than available

Confirmation rejected

Error shows available vs requested quantity

3️⃣ Invalid Status Transition

Deliver draft order → Blocked

Edit confirmed order → Blocked

Reverse transitions → Blocked

📌 Assumptions Made

Each product has exactly one inventory record.

Inventory represents current stock state (not historical stock logs).

Draft orders do not reserve stock.

Price at order time is snapshotted and stored in OrderItem.

Confirmed order deletion restores stock.

Dealers with existing orders cannot be deleted (PROTECT constraint).

Manual inventory updates are performed by admin users.

🧪 Demo / Step-by-Step Testing Flow

Base URL:

http://127.0.0.1:8000/api/

Use Postman → Body → raw → JSON.

🔹 SCENARIO 1 — Successful Order Flow
1️⃣ Create Product

POST

/api/products/

Body:

{
  "name": "Brake Pad",
  "sku": "BP001",
  "price": 500,
  "description": "Front brake pad"
}

Expected:

Product created

ID = 1

2️⃣ Add Inventory

POST

/api/inventory/

Body:

{
  "product": 1,
  "quantity": 100
}

Expected:

Stock = 100 units

3️⃣ Create Dealer

POST

/api/dealers/

Body:

{
  "name": "ABC Motors",
  "email": "abc@test.com",
  "phone": "9999999999",
  "address": "Pune"
}

⚠️ All fields required:
name
email
phone
address
Expected:
Dealer ID = 1

4️⃣ Create Draft Order

POST

/api/orders/

Body:

{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 10
    }
  ]
}

Expected:

Status = DRAFT

total_amount = 5000

5️⃣ Confirm Order

POST

/api/orders/1/confirm/

Expected:

Status → CONFIRMED

Stock deducted

6️⃣ Verify Stock Deduction

GET

/api/products/

Expected:

stock = 90
7️⃣ Deliver Order

POST

/api/orders/1/deliver/

Expected:

Status → DELIVERED

🔹 SCENARIO 2 — Insufficient Stock
1️⃣ Reduce Stock to 5

PUT

/api/inventory/1/

Body:

{
  "quantity": 5
}
2️⃣ Create Large Order

POST

/api/orders/

Body:

{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 10
    }
  ]
}
3️⃣ Confirm Order

POST

/api/orders/2/confirm/

Expected error:

{
  "error": "Insufficient stock",
  "details": [
    {
      "product": "Brake Pad",
      "available": 5,
      "requested": 10
    }
  ]
}
🔹 SCENARIO 3 — Invalid Status Transition
Case 1 — Deliver Draft Order

POST

/api/orders/{draft_id}/deliver/

Expected:

Only confirmed orders can be delivered.
Case 2 — Edit Confirmed Order

PUT

/api/orders/1/

Body:

{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 5
    }
  ]
}

Expected:

Only draft orders can be edited.
Case 3 — Reverse Transition

Try confirming delivered order → blocked.

🧾 Important Testing Notes

Inventory created once per product
Stock deducted only on confirm
Draft orders editable
Confirmed orders locked
Price snapshot preserved


📦 Postman Collection

Postman collection included in repository as:

vikmo_api_test.postman_collection.json
🏁 Conclusion

This project fulfills all functional and technical requirements defined in the Vikmo assignment, including relational database design, transactional stock management, order lifecycle enforcement, and RESTful API implementation.
