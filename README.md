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

🎥 Demo Video

Video walkthrough link:
(Add Google Drive / YouTube link here)

📦 Postman Collection

Postman collection included in repository as:

vikmo_api_test.postman_collection.json
🏁 Conclusion

This project fulfills all functional and technical requirements defined in the Vikmo assignment, including relational database design, transactional stock management, order lifecycle enforcement, and RESTful API implementation.
