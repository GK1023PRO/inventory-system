from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

LOW_STOCK_THRESHOLD = 5

# -----------------------
# Database Setup
# -----------------------
def init_db():
    conn = sqlite3.connect("inventory.db")
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
# Home Page - View Products
# -----------------------
@app.route('/')
def home():
    conn = sqlite3.connect("inventory.db")
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
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            (name, category, price, quantity)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template("add_product.html")

# -----------------------
# Edit Product
# -----------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        cursor.execute(
            "UPDATE products SET name=?, category=?, price=?, quantity=? WHERE id=?",
            (name, category, price, quantity, id)
        )
        conn.commit()
        conn.close()
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
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# -----------------------
# Run App
# -----------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)