import sqlite3

DATABASE = "inventory.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            reorder_level INTEGER NOT NULL DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def get_all_products():
    connection = get_db_connection()
    products = connection.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return products


def add_product(name, category, price, quantity, reorder_level):
    connection = get_db_connection()

    connection.execute("""
        INSERT INTO products
        (name, category, price, quantity, reorder_level)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, price, quantity, reorder_level))

    connection.commit()
    connection.close()
def get_product(product_id):
    connection = get_db_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()
    return product


def update_product(product_id, name, category, price, quantity, reorder_level):
    connection = get_db_connection()

    connection.execute("""
        UPDATE products
        SET name = ?,
            category = ?,
            price = ?,
            quantity = ?,
            reorder_level = ?
        WHERE id = ?
    """, (
        name,
        category,
        price,
        quantity,
        reorder_level,
        product_id
    ))

    connection.commit()
    connection.close()


def delete_product(product_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()


def update_stock(product_id, amount):
    connection = get_db_connection()

    connection.execute("""
        UPDATE products
        SET quantity = quantity + ?
        WHERE id = ?
    """, (amount, product_id))

    connection.commit()
    connection.close()