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

        print("POST request received")

        garment_type = request.form["garment_type"] 
        chest = request.form["chest"] or None
        shoulder = request.form["shoulder"] or None
        length = request.form["length"] or None
        sleeve = request.form["sleeve"] or None
        waist= request.form["waist"] or None
        notes = request.form["notes"] or None

        print(customer_id, garment_type, chest, shoulder, length, sleeve, waist, notes)

        query = """
        INSERT INTO measurement
        (customer_id, garment_type, chest, shoulder, length, sleeve, waist, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (customer_id, garment_type, chest, shoulder, length, sleeve, waist, notes)

        print(values)

        cursor.execute(query, values)

        print("Executed!")

        connection.commit()

        print("Committed!")
   
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

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)