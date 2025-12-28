from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, StockMovement, User

from config import Config
from flask import session
from functools import wraps


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "inventory-secret"

db.init_app(app)

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

#  ADD PRODUCT 
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        cas = request.form["cas"]
        unit = request.form["unit"]

        # CAS must be unique
        if Product.query.filter_by(cas_number=cas).first():
            flash("CAS Number already exists!", "danger")
            return redirect(url_for("add_product"))

        product = Product(name=name, cas_number=cas, unit=unit)
        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("inventory"))

    return render_template("add_product.html")


#  UPDATE STOCK + MOVEMENT HISTORY 
@app.route("/update-stock/<int:product_id>", methods=["GET", "POST"])
@login_required
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        action = request.form["action"]
        quantity = float(request.form["quantity"])

        # Validations
        if quantity <= 0:
            flash("Quantity must be positive!", "danger")
            return redirect(request.url)

        if action == "OUT" and product.stock < quantity:
            flash("Stock cannot go below zero!", "danger")
            return redirect(request.url)

        # Update stock
        if action == "IN":
            product.stock += quantity
        else:
            product.stock -= quantity

        # Log stock movement
        movement = StockMovement(
            product_id=product.id,
            action=action,
            quantity=quantity
        )

        db.session.add(movement)
        db.session.commit()

        flash("Stock updated successfully!", "success")
        return redirect(url_for("update_stock", product_id=product.id))

    # Fetch movement history (latest first)
    movements = (
        StockMovement.query
        .filter_by(product_id=product.id)
        .order_by(StockMovement.timestamp.desc())
        .all()
    )

    return render_template(
        "update_stock.html",
        product=product,
        movements=movements
    )


#  EDIT PRODUCT 
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.unit = request.form["unit"]

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("inventory"))

    return render_template("edit_product.html", product=product)


#  DELETE PRODUCT 
@app.route("/delete/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("inventory"))

@app.route("/")
@login_required
def inventory():
    search = request.args.get("search")
    sort = request.args.get("sort")

    query = Product.query

    # Search by name or CAS
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.cas_number.ilike(f"%{search}%"))
        )

    # Sorting logic
    if sort == "stock_desc":
        query = query.order_by(Product.stock.desc())
    elif sort == "stock_asc":
        query = query.order_by(Product.stock.asc())
    elif sort == "name_asc":
        query = query.order_by(Product.name.asc())
    elif sort == "name_desc":
        query = query.order_by(Product.name.desc())

    products = query.all()
    return render_template("products.html", products=products)


#  LOGIN / LOGOUT
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session["user_id"] = user.id
            return redirect(url_for("inventory"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/seed-user")
def seed_user():
    if User.query.filter_by(username="admin").first():
        return "Admin user already exists"

    admin = User(
        username="admin",
        password="admin123"
    )
    db.session.add(admin)
    db.session.commit()

    return "Admin user created"

@app.route("/seed")
def seed():
    if Product.query.first():
        return "Data already exists"

    products = [
        Product(name="Ethanol", cas_number="64-17-5", unit="Litre", stock=50),
        Product(name="Acetone", cas_number="67-64-1", unit="Litre", stock=30),
        Product(name="Methanol", cas_number="67-56-1", unit="Litre", stock=40),
        Product(name="Sodium Hydroxide", cas_number="1310-73-2", unit="KG", stock=3),
        Product(name="Hydrochloric Acid", cas_number="7647-01-0", unit="Litre", stock=25),
        Product(name="Sulfuric Acid", cas_number="7664-93-9", unit="Litre", stock=15),
        Product(name="Ammonia", cas_number="7664-41-7", unit="KG", stock=2),
    ]

    db.session.bulk_save_objects(products)
    db.session.commit()

    return "Sample data added"


#  RUN APP 
if __name__ == "__main__":
    app.run(debug=True)
