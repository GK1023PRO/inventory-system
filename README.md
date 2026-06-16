# 📦 Inventory Management System

A simple web-based inventory management system built with Python, Flask, and SQLite.

## Features

- ✅ View all products
- ➕ Add new products
- ✏️ Edit existing products
- ❌ Delete products
- ⚠️ Low stock alerts (below 5 units)
- 🎨 Clean Bootstrap UI

## Tech Stack

- Python 3.12
- Flask
- SQLite
- Bootstrap 5

## Run Locally

1. Install dependencies:
pip install -r requirements.txt

2. Start the app:
python app.py

3. Visit: http://127.0.0.1:5000

## Run with Docker

1. Build the image:
docker build -t inventory-system .

2. Run the container:
docker run -p 5003:5000 inventory-system

3. Visit: http://127.0.0.1:5000

## Project Structure
app/

├── app.py

├── requirements.txt

├── Dockerfile

├── .dockerignore

├── README.md

└── templates/

├── index.html

├── add_product.html