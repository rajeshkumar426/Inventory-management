import os
import json
import sqlite3
from flask import Flask, url_for, request, redirect
from flask import render_template as render

DATABASE_NAME = 'inventory.sqlite'

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'database', DATABASE_NAME),
)


link = {x: x for x in ["product"]}
link["index"] = '/'


def init_database():
    '''
    initialize database 
    '''
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prod_name TEXT UNIQUE NOT NULL,
                    prod_quantity INTEGER NOT NULL,
                    prod_price INTEGER NOT NULL,
                    description Text
                    );
    """)
    db.commit()


@app.route('/', methods=['GET'])
def summary():
    '''
    Get all products detail
    '''
    init_database()
    msg = None
    q_data, products = None, None
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.execute("""
        SELECT prod_name, prod_quantity, prod_price FROM products
        """)
        q_data = cursor.fetchall()
    except sqlite3.Error as e:
        msg = f"An error occurred: {e.args[0]}"
    if msg:
        print(msg)

    return render('index.html', link=link, title="Summary", products=products, database=q_data)


@app.route('/product', methods=['POST', 'GET'])
def product():
    init_database()
    msg = None
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if request.method == 'POST':
        prod_name = request.form['prod_name']
        quantity = request.form['prod_quantity']
        price = request.form['prod_price']
        decription = request.form['description']

        transaction_allowed = False
        if prod_name not in ['', ' ', None]:
            if quantity not in ['', ' ', None]:
                transaction_allowed = True

        if transaction_allowed:
            try:
                cursor.execute("INSERT INTO products (prod_name, prod_quantity,prod_price, description) VALUES (?, ?, ?,?)", (prod_name, quantity, price, decription))
                db.commit()
            except sqlite3.Error as e:
                msg = f"An error occurred: {e.args[0]}"
            else:
                msg = f"{prod_name} added successfully"

            if msg:
                print(msg)

            return redirect(url_for('product'))

    return render('product.html',
                  link=link, products=products, transaction_message=msg,
                  title="Products Log")



@app.route('/delete')
def delete():
    '''
    Delete particular products on id
    '''
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    id_ = request.args.get('prod_id')
    cursor.execute("DELETE FROM products WHERE prod_id == ?", str(id_))
    db.commit()

    return redirect(url_for('product'))

@app.route('/get_product_details_on_id')
def get_product_details_on_id():
    '''
        Get product details on id
    '''
    id = request.args.get('prod_id')
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    cursor.execute("SELECT* from products WHERE prod_id == ?", str(id))
    products = cursor.fetchall()
    print(products)
    return render("products_details.html", link=link,products=products)

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    '''
        Edit or modify product details
    '''
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    
    prod_id = request.form['prod_id']
    prod_name = request.form['prod_name']
    prod_quantity = request.form['prod_quantity']
    prod_price = request.form['prod_price']

    if prod_name:
        cursor.execute("UPDATE products SET prod_name = ? WHERE prod_id == ?", (prod_name, str(prod_id)))
    if prod_quantity:
        cursor.execute("Update products SET prod_quantity = ? WHERE prod_id == ?", (prod_quantity, str(prod_id)))
    if prod_price:
        cursor.execute("Update products SET prod_price = ? WHERE prod_id == ? ", (prod_price, str(prod_id)))
    db.commit()

    return redirect(url_for('product'))

    return render(url_for(type_))


if __name__ == '__main__':
    app.run()