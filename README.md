# MyCart - Inventory Management System

MyCart is a web-based inventory management system developed using Python, Flask, and SQLite. It helps users manage products, monitor stock levels, track inventory value, and identify low-stock items through a simple and responsive dashboard.

## Features

- Add new products
- Edit existing products
- Delete products
- Increase or decrease stock quantity
- Prevent stock quantity from going below zero
- Search products
- Filter products by category
- Automatic low-stock detection
- Inventory value calculation
- Dashboard statistics
- Inventory distribution by category
- Responsive web interface
- SQLite database for persistent data storage

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js
- Jinja2

## Dashboard

The dashboard provides an overview of:

- Total Products
- Total Stock
- Inventory Value
- Low Stock Products
- Recent Products
- Inventory by Category

## Project Structure

```text
Inventory Managment system
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── static
│   ├── logo.png
│   └── style.css
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── add_product.html
│   └── edit_product.html
│
└── venv