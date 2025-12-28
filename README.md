# Chemical Inventory Management System (chemflotory)
## 🔗 Live Deployment:
https://chemical-inventory-system.onrender.com


## Overview
**chemflotory**, The Chemical Inventory Management System is a web-based application developed using Flask and SQLAlchemy to manage chemical products, track stock movements, and ensure inventory safety.
The system supports authenticated access, real-time stock updates, and maintains a detailed audit trail of inventory changes. It is designed as a functional MVP suitable for academic and internship-level evaluation.


## Key Features
- Secure login and logout functionality
- Add, edit, and delete chemical products
- Update inventory with IN / OUT stock movements
- Prevents stock from going below zero (server-side validation)
- Maintains stock movement history for auditing
- Search products by name or CAS number
- Sort products by stock level or alphabetical order
- Low-stock visual indicators
- Clean, modern SaaS-style UI
- Deployed on a free cloud platform


## Tech Stack
**Backend**: Flask (Python)
**Database:**
  - MySQL (local development)
  - SQLite (cloud deployment)
  - ORM: SQLAlchemy
**Frontend**: HTML, Jinja2, Bootstrap 5
**Deployment**: Render + Gunicorn
**Version Control**: Git & GitHub


## Setup Instructions (Local Development)
### 1️⃣ Clone the Repository
git clone https://github.com/lakshyadas13/chemical-inventory-system.git
cd chemical-inventory-system

### 2️⃣ Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate   # macOS / Linux

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Database Configuration
Ensure MySQL is running locally
Update credentials if required
Tables are created automatically at application startup
with app.app_context():
    db.create_all()

### 5️⃣ Run the Application
python app.py
Access the application at:
http://127.0.0.1:5000


##  Deployment Details
The application is deployed on Render using Gunicorn
SQLite is used as a fallback database for free cloud deployment
The database is selected dynamically using environment variables
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///inventory.db"
)
## Database Models / Tables
### 1️⃣ User
Stores administrator login credentials.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
Purpose:
Handles authentication
Supports future extension for multiple admin users
### 2️⃣ Product
Stores chemical product details.
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cas_number = db.Column(db.String(50), unique=True, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Float, default=0)
Purpose:
Maintains inventory data
Enforces unique CAS numbers
Tracks current stock levels
### 3️⃣ StockMovement
Logs every stock update operation.
class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    action = db.Column(db.String(10))  # IN or OUT
    quantity = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
Purpose:
Records inventory changes
Enables auditability and traceability
Supports historical analysis
🔐 Business Logic Highlights
  - Stock levels are validated server-side to prevent negative values
  - CAS numbers are enforced as unique identifiers
  - All inventory routes are protected using authentication
  - Every stock update generates a corresponding movement record


## Future Enhancements
Role-based access control (Admin / Viewer)
Password hashing and improved security
Persistent managed cloud database
Inventory analytics dashboard
Export reports (CSV / PDF)


# Author
Lakshya Das
