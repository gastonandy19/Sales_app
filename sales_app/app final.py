"""
Simple Sales Recording Web Application
----------------------------------------
Backend built with Flask.

Python concepts demonstrated:
- Variables & data types (strings, integers, floats)
- Lists (storing multiple sales records)
- Dictionaries (each sale is a dict with product, quantity, price, total)
- Control flow (if/else, for loops)
- Functions (organizing logic into reusable blocks)
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, Response

app = Flask(__name__)

# ----------------------------------------------------------------------
# In-memory "database": a LIST of DICTIONARIES.
# Each dictionary represents one sale record.
# This resets every time the server restarts (fine for a class assignment).
# ----------------------------------------------------------------------
sales = []


def calculate_total(quantity, price):
    """Multiply quantity by price to get the total for one sale line."""
    return quantity * price


def calculate_day_total(sales_list):
    """Add up the 'total' value of every sale in the list."""
    day_total = 0
    for sale in sales_list:          # control flow: for loop
        day_total += sale["total"]
    return day_total


def summarize_sales(sales_list):
    """Return the live summary metrics for the day's sales."""
    total_sales = calculate_day_total(sales_list)
    total_units_sold = sum(sale["quantity"] for sale in sales_list)
    transaction_count = len(sales_list)

    best_selling_item = "N/A"
    best_selling_units = 0
    item_totals = {}
    for sale in sales_list:
        item_name = str(sale["product"]).strip().lower()
        item_totals[item_name] = item_totals.get(item_name, 0) + sale["quantity"]

    if item_totals:
        best_item_key, best_selling_units = max(
            item_totals.items(), key=lambda item: (item[1], item[0])
        )
        best_selling_item = best_item_key.title()

    return {
        "total_sales": round(total_sales, 2),
        "transaction_count": transaction_count,
        "total_units_sold": total_units_sold,
        "best_selling_item": best_selling_item,
        "best_selling_units": best_selling_units,
    }


def build_report_html(sales_list):
    """Build a simple HTML sales report for download."""
    summary = summarize_sales(sales_list)
    sales_rows = ""
    for sale in sales_list:
        sales_rows += (
            "<tr>"
            f"<td>{sale['id']}</td>"
            f"<td>{sale['product']}</td>"
            f"<td>{sale['quantity']}</td>"
            f"<td>{sale['price']:.2f}</td>"
            f"<td>{sale['total']:.2f}</td>"
            "</tr>"
        )

    if not sales_rows:
        sales_rows = "<tr><td colspan='5'>No sales recorded yet.</td></tr>"

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Daily Sales Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        th {{ background: #f2f2f2; }}
        .summary {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Daily Sales Report</h1>
    <div class=\"summary\">
        <p><strong>Total Sales:</strong> GHS {summary['total_sales']:.2f}</p>
        <p><strong>Transactions:</strong> {summary['transaction_count']}</p>
        <p><strong>Total Units Sold:</strong> {summary['total_units_sold']}</p>
        <p><strong>Best Selling Item:</strong> {summary['best_selling_item']}</p>
    </div>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Product</th>
                <th>Qty</th>
                <th>Price (GHS)</th>
                <th>Total (GHS)</th>
            </tr>
        </thead>
        <tbody>
            {sales_rows}
        </tbody>
    </table>
</body>
</html>
"""


@app.route("/")
def index():
    """Show the form plus a table of all sales entered so far."""
    day_total = calculate_day_total(sales)
    summary = summarize_sales(sales)
    return render_template("index.html", sales=sales, day_total=day_total, summary=summary)


@app.route("/api/summary")
def summary_api():
    """Return live summary numbers as JSON for the page widgets."""
    return jsonify(summarize_sales(sales))


@app.route("/api/report")
def download_report():
    """Return the HTML sales report for download."""
    report_html = build_report_html(sales)
    return Response(
        report_html,
        mimetype="text/html",
        headers={"Content-Disposition": "attachment; filename=sales_report.html"},
    )


@app.route("/api/reset", methods=["POST"])
def reset_sales():
    """Clear the current day's transactions after a confirmation step in the UI."""
    global sales
    sales = []
    return jsonify({"success": True, "message": "Daily transactions cleared."})


@app.route("/add", methods=["POST"])
def add_sale():
    """Handle the form submission and add a new sale record."""
    product = request.form.get("product", "").strip().title()
    quantity_raw = request.form.get("quantity", "")
    price_raw = request.form.get("price", "")

    # Basic validation (control flow: if/else)
    if product == "" or quantity_raw == "" or price_raw == "":
        return redirect(url_for("index"))

    try:
        quantity = int(quantity_raw)
        price = float(price_raw)
    except ValueError:
        # If the user typed letters instead of numbers, ignore the entry
        return redirect(url_for("index"))

    total = calculate_total(quantity, price)

    # Build a dictionary for this sale and add it to our list
    new_sale = {
        "id": len(sales) + 1,
        "product": product,
        "quantity": quantity,
        "price": price,
        "total": total,
    }
    sales.append(new_sale)

    return redirect(url_for("index"))


@app.route("/delete/<int:sale_id>")
def delete_sale(sale_id):
    """Bonus feature: remove a sale record by its id."""
    global sales
    sales = [s for s in sales if s["id"] != sale_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Run one clean Flask instance without the reloader to avoid stale state
    app.run(debug=False, use_reloader=False)
