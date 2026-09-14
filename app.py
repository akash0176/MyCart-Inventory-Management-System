from flask import Flask, render_template, request, redirect, url_for
from database import (
    initialize_database,
    get_all_products,
    get_product,
    add_product,
    update_product,
    delete_product,
    update_stock
)

app = Flask(__name__)

initialize_database()


@app.route("/")
def index():
    products = get_all_products()

    total_products = len(products)

    total_stock = sum(
        product["quantity"]
        for product in products
    )

    inventory_value = sum(
        product["price"] * product["quantity"]
        for product in products
    )

    low_stock = sum(
        1
        for product in products
        if product["quantity"] <= product["reorder_level"]
    )

    category_stock = {}

    for product in products:
        category = product["category"]
        quantity = product["quantity"]

        if category in category_stock:
            category_stock[category] += quantity
        else:
            category_stock[category] = quantity

    return render_template(
        "index.html",
        products=products,
        total_products=total_products,
        total_stock=total_stock,
        inventory_value=inventory_value,
        low_stock=low_stock,
        category_stock=category_stock
    )


@app.route("/products")
def products():
    all_products = get_all_products()

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    filtered_products = all_products

    if search:
        search_lower = search.lower()

        filtered_products = [
            product
            for product in filtered_products
            if search_lower in product["name"].lower()
            or search_lower in product["category"].lower()
        ]

    if category and category.lower() != "all":
        filtered_products = [
            product
            for product in filtered_products
            if product["category"].lower() == category.lower()
        ]

    categories = sorted(
        set(product["category"] for product in all_products)
    )

    return render_template(
        "products.html",
        products=filtered_products,
        categories=categories,
        search=search,
        selected_category=category
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        reorder_level = int(request.form["reorder_level"])

        add_product(
            name,
            category,
            price,
            quantity,
            reorder_level
        )

        return redirect(url_for("products"))

    return render_template("add_product.html")


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit(product_id):
    product = get_product(product_id)

    if product is None:
        return "Product not found", 404

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        reorder_level = int(request.form["reorder_level"])

        update_product(
            product_id,
            name,
            category,
            price,
            quantity,
            reorder_level
        )

        return redirect(url_for("products"))

    return render_template(
        "edit_product.html",
        product=product
    )


@app.route("/delete/<int:product_id>", methods=["POST"])
def delete(product_id):
    delete_product(product_id)

    return redirect(url_for("products"))


@app.route("/stock/<int:product_id>", methods=["POST"])
def stock(product_id):
    action = request.form["action"]
    amount = int(request.form["amount"])

    if action == "remove":
        amount = -amount

    update_stock(product_id, amount)

    return redirect(url_for("products"))


if __name__ == "__main__":
    app.run(debug=True)