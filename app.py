from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'inventory_secret_key'

LOW_STOCK_THRESHOLD = 5
DB_PATH = "/app/data/inventory.db"

# -----------------------
# Database Setup
# -----------------------
def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Input Validation
# -----------------------
def validate_product(name, category, price, quantity):
    errors = []
    if not name or len(name.strip()) == 0:
        errors.append("Product name is required.")
    if not category or len(category.strip()) == 0:
        errors.append("Category is required.")
    try:
        price = float(price)
        if price < 0:
            errors.append("Price cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Price must be a valid number.")
    try:
        quantity = int(quantity)
        if quantity < 0:
            errors.append("Quantity cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Quantity must be a valid whole number.")
    return errors, price, quantity

# -----------------------
# Home Page - View Products
# -----------------------
@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products, threshold=LOW_STOCK_THRESHOLD)

# -----------------------
# Add Product
# -----------------------
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']

        errors, price, quantity = validate_product(name, category, price, quantity)

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template("add_product.html",
                                   name=name, category=category,
                                   price=price, quantity=quantity)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            (name, category, price, quantity)
        )
        conn.commit()
        conn.close()
        flash("Product added successfully!", 'success')
        return redirect(url_for('home'))
    return render_template("add_product.html")

# -----------------------
# Edit Product
# -----------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']

        errors, price, quantity = validate_product(name, category, price, quantity)

        if errors:
            for error in errors:
                flash(error, 'danger')
            cursor.execute("SELECT * FROM products WHERE id=?", (id,))
            product = cursor.fetchone()
            conn.close()
            return render_template("edit_product.html", product=product)

        cursor.execute(
            "UPDATE products SET name=?, category=?, price=?, quantity=? WHERE id=?",
            (name, category, price, quantity, id)
        )
        conn.commit()
        conn.close()
        flash("Product updated successfully!", 'success')
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template("edit_product.html", product=product)

# -----------------------
# Delete Product
# -----------------------
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Product deleted successfully!", 'success')
    return redirect(url_for('home'))

# -----------------------
# Run App
# -----------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)