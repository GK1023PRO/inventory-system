# 📦 Inventory Management System

A simple web-based inventory management system built with Python, Flask, and SQLite.

## Features

- ✅ View all products
- ➕ Add new products
- ✏️ Edit existing products
- ❌ Delete products
- ⚠️ Low stock alerts (below 5 units)
- 🎨 Clean Bootstrap UI
- ✅ Input validation with error messages
- 🐳 Docker support with persistent data

## Tech Stack

- Python 3.12
- Flask
- SQLite
- Bootstrap 5
- Docker

## Run Locally

1. Install dependencies:
pip install -r requirements.txt

2. Start the app:
python app.py

3. Visit: http://127.0.0.1:5000

## Run with Docker

1. Build the image:
docker build -t inventory-system .

2. Run the container with persistent data:
docker run -p 5003:5000 -v inventory-data:/app/data inventory-system

3. Visit: http://127.0.0.1:5003

## Project Structure
app/

├── app.py

├── requirements.txt

├── Dockerfile

├── .dockerignore

├── README.md

├── .gitignore

└── templates/

├── index.html

├── add_product.html

└── edit_product.html

## Notes

- Data persists between Docker restarts using a Docker volume
- Low stock alert triggers when quantity is below 5 units
- Negative values are blocked on both frontend and backend