from database.mysql import get_connection, get_cursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/add-customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone_no = request.form["phone_no"]
        email = request.form["email"]
        address = request.form["address"]
        customer_id = request.form["customer_id"]

        connection, cursor = get_cursor()

        if customer_id == "":

            query = """
            INSERT INTO customer
            (full_name, phone_no, email, address)
            VALUES (%s, %s, %s, %s)
            """

            values = (full_name, phone_no, email, address)

        else: 

            query = """
            UPDATE customer
            SET
                full_name = %s,
                phone_no = %s,
                email = %s,
                address = %s
            WHERE customer_id = %s
            """

            values = (full_name, phone_no, email, address, customer_id)

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("customers"))

    return render_template(
        "add_customer.html",
        customer=None
        )

@app.route("/customers")
def customers():

    phone_no = request.args.get("phone_no")

    connection, cursor = get_cursor()

    if phone_no:

        cursor.execute(
            """
            SELECT *
            FROM customer
            WHERE phone_no = %s
            """,
            (phone_no,)
        )

    else:

        cursor.execute("SELECT * FROM customer")

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "customers.html",
        customers=data,
        phone_no=phone_no
    )

@app.route("/edit-customer/<int:customer_id>")
def edit_customer(customer_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT * 
        FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "add_customer.html",
        customer=customer
    )

@app.route("/delete-customer/<int:customer_id>")
def delete_customer(customer_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        DELETE FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("customers"))

@app.route("/measurements/<int:customer_id>", methods=["GET","POST"])
def measurements(customer_id):

    connection, cursor = get_cursor()

    if request.method == "POST":

        garment_type = request.form["garment_type"] 
        chest = request.form["chest"] or None
        shoulder = request.form["shoulder"] or None
        length = request.form["length"] or None
        sleeve = request.form["sleeve"] or None
        waist= request.form["waist"] or None
        notes = request.form["notes"] or None

        query = """
        INSERT INTO measurement
        (customer_id, garment_type, chest, shoulder, length, sleeve, waist, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (customer_id, garment_type, chest, shoulder, length, sleeve, waist, notes)

        cursor.execute(query, values)

        connection.commit()
   
        return redirect(
            url_for(
                "measurements",
                customer_id=customer_id)
            )

    cursor.execute(
        """
        SELECT *
        FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    cursor.execute(
        """
        SELECT * 
        FROM measurement
        WHERE customer_id = %s
        ORDER BY measurement_date DESC
        """,
        (customer_id,)
    )

    measurements = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "measurements.html",
        customer=customer,
        measurements=measurements
    )

@app.route("/all-orders")
def orders():

    connection, cursor = get_cursor()

    query = """
    SELECT
        c.full_name,
        o.order_id,
        o.delivery_date,
        o.current_status,
        o.total_amount
    FROM customer AS c
    JOIN orders AS o
    ON c.customer_id = o.customer_id;"""

    cursor.execute(query)

    data = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template(
        "orders.html",
        orders=data
    )


@app.route("/add-order/<int:customer_id>", methods=["GET", "POST"])
def add_order(customer_id):

    connection, cursor = get_cursor()

    if request.method == "POST":

        order_date = request.form["order_date"]
        delivery_date = request.form["delivery_date"]
        total_amount = request.form["total_amount"]
        current_status = request.form["current_status"]

        query = """
        INSERT INTO orders
        (customer_id, order_date, delivery_date, total_amount, current_status)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (customer_id, order_date, delivery_date, total_amount, current_status)

        cursor.execute(query, values)

        connection.commit()

        return redirect(
            url_for(
            "order_items",
            order_id=cursor.lastrowid
            )
        )
    
    cursor.execute(
        """
        SELECT *
        FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "add_order.html",
        customer=customer
    )

@app.route("/order-items/<int:order_id>", methods=["GET", "POST"])
def order_items(order_id):

    connection, cursor = get_cursor()

    if request.method == "POST":

        print("FORM DATA:", request.form.to_dict())

        measurement_id = request.form["measurement_id"]
        product_name = request.form["product_name"]
        quantity = request.form["quantity"]
        item_status = request.form["item_status"]
        unit_price = request.form["unit_price"]
        special_instruction = request.form["special_instruction"]

        item_id = request.form["item_id"]

        if item_id == "":

            query = """
            INSERT INTO order_item
            (order_id, measurement_id, product_name, quantity, item_status, unit_price, special_instruction)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """ 

            values = (
                order_id,
                measurement_id,
                product_name,
                quantity,
                item_status,
                unit_price,
                special_instruction
            )

        else:

            query = """
            UPDATE order_item
            SET 
                measurement_id = %s,
                product_name = %s,
                quantity = %s,
                item_status = %s,
                unit_price = %s,
                special_instruction = %s
            WHERE item_id = %s
            """

            values = (
                measurement_id,
                product_name,
                quantity,
                item_status,
                unit_price,
                special_instruction,
                item_id
            )

        cursor.execute(query, values)
        connection.commit()

        cursor.execute(
            """
            SELECT COALESCE(SUM(unit_price * quantity), 0) AS total
            FROM order_item
            WHERE order_id = %s
            """,
            (order_id,)
        )

        total = cursor.fetchone()["total"]

        print(total)

        cursor.execute(
            """
            UPDATE orders
            SET total_amount = %s
            WHERE order_id = %s
            """,
            (total, order_id)
        )

        connection.commit()

        return redirect(
            url_for(
                "order_items",
                order_id=order_id
            )
        )

    cursor.execute(
        """
        SELECT * 
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    print(order)

    customer_id = order["customer_id"]

    cursor.execute(
        """
        SELECT *
        FROM measurement
        WHERE customer_id = %s
        ORDER BY measurement_date Desc
        """,
        (customer_id,)
    )

    measurements = cursor.fetchall()

    cursor.execute(
        """
        SELECT *
        FROM order_item
        WHERE order_id = %s
        """,
        (order_id,)
    )

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "order_items.html",
        order=order,
        measurements=measurements,
        items=items
    )

@app.route("/delete-order-item/<int:item_id>")
def delete_order_item(item_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT order_id
        FROM order_item
        WHERE item_id = %s
        """,
        (item_id,)
    )

    item = cursor.fetchone()

    order_id = item["order_id"]

    cursor.execute(
        """
        DELETE FROM order_item
        WHERE item_id = %s
        """,
        (item_id,)
    )

    cursor.execute(
        """
        SELECT COALESCE(SUM(unit_price * quantity), 0) AS total
        FROM order_item
        WHERE order_id = %s
        """,
        (order_id,)
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        UPDATE orders
        SET total_amount = %s
        WHERE order_id = %s
        """,
        (total, order_id)
    )

    connection.commit()
    
    cursor.close()
    connection.close()

    return redirect(
        url_for(
            "order_items",
            order_id=order_id
        )
    )

@app.route("/edit-order-item/<int:item_id>")
def edit_order_item(item_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT * 
        FROM order_item
        WHERE item_id = %s
        """,
        (item_id,)
    )

    item = cursor.fetchone()

    order_id = item["order_id"]

    cursor.execute(
        """
        SELECT * 
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    customer_id = order["customer_id"]

    cursor.execute(
        """
        SELECT *
        FROM measurement
        WHERE customer_id = %s
        ORDER BY measurement_date DESC
        """,
        (customer_id,)
    )

    measurements = cursor.fetchall()

    cursor.execute(
        """
        SELECT *
        FROM order_item
        WHERE order_id = %s
        """,
        (order_id,)
    )

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "order_items.html",
        item=item,
        order=order,
        measurements=measurements,
        items=items
    )

@app.route("/payments/<int:order_id>", methods=["GET", "POST"])
def payments(order_id):

    connection, cursor = get_cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        payment_date = request.form["payment_date"]
        notes = request.form["notes"]
        
        cursor.execute(
            """
            INSERT INTO payment
            (order_id, amount, payment_method, payment_date, notes)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, amount, payment_method, payment_date, notes)
        )

        connection.commit()

        return redirect(
            url_for("payments", order_id=order_id)
        )

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    customer_id = order["customer_id"]

    cursor.execute(
        """
        SELECT * 
        FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    cursor.execute(
        """
        SELECT *
        FROM payment 
        WHERE order_id = %s
        ORDER BY payment_date DESC
        """,
        (order_id,)
    )

    payments = cursor.fetchall()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS paid
        FROM payment
        WHERE order_id = %s
        """,
        (order_id,)
    )

    paid = cursor.fetchone()["paid"]

    remaining = order["total_amount"] - paid

    cursor.close()
    connection.close()

    return render_template(
        "payment.html",
        order=order,
        customer=customer,
        payments=payments,
        paid=paid,
        remaining=remaining
    )

@app.route("/delete-payment/<int:payment_id>")
def delete_payment(payment_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT order_id
        FROM payment
        WHERE payment_id = %s
        """,
        (payment_id,)
    )

    payment = cursor.fetchone()

    order_id = payment["order_id"]

    cursor.execute(
        """
        DELETE FROM payment
        WHERE payment_id = %s
        """,
        (payment_id,)
    )

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount),0) AS paid
        FROM payment
        WHERE order_id = %s
        """,
        (order_id,)
    )

    paid = cursor.fetchone()["paid"]

    cursor.execute(
        """
        SELECT total_amount
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    remaining = order["total_amount"] - paid

    connection.commit()

    return redirect(
        url_for(
            "payments",
            order_id=order_id
        )
    )

@app.route("/edit-payment/<int:payment_id>", methods=["GET", "POST"])
def edit_payment(payment_id):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT *
        FROM payment
        WHERE payment_id = %s
        """,
        (payment_id,)
    )

    payment = cursor.fetchone()

    order_id = payment["order_id"]
  
    if request.method == "POST":

        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        payment_date = request.form["payment_date"]
        notes = request.form["notes"]

        cursor.execute(
            """
            UPDATE payment
            SET
                amount = %s,
                payment_method = %s,
                payment_date = %s,
                notes = %s
            WHERE payment_id = %s
            """,
            (
                amount,
                payment_method,
                payment_date,
                notes,
                payment_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(
            url_for(
                "payments",
                order_id=order_id
            )
        )

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    customer_id = order["customer_id"]

    cursor.execute(
        """
        SELECT *
        FROM customer
        WHERE customer_id = %s
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    connection.close()
    cursor.close()

    return render_template(
        "payment.html",
        payment=payment,
        order=order,
        customer=customer
    )


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)