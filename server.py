from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename

from flask.globals import current_app
#import imghdr
app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'images/'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']
def get_cursor():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    return (cur, conn)

"""Initialize the sqlite database and fill up the `products` table with sample data."""
def initialize_db():
    (cur, conn) = get_cursor()

    # Create products table with sample data
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT, price INTEGER, stock INTEGER)")
    cur.execute("""INSERT INTO products (name, imgpath, price, stock) VALUES \
        ('University of Waterloo logo', 'images/Uwaterloo.png', 120, 999), \
        ('CN_Tower', 'images/CN-Tower-Toronto.jpg', 1000000000, 0), \
        ('Shopify logo', 'images/shopify.png', 2000, 666), \
        ('Many Books', 'images/book.jpg', 47900, 312)
    """)

    # Create empty transactions table
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("CREATE TABLE transactions (timestamp TEXT, productid INTEGER, value INTEGER)")
    
    # Commit the db changes
    conn.commit()
    print("Initialized database")

@app.route("/")
def home_page():
    (cur, _) = get_cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    print("Retrieved %d database entries" % len(rows))
    
    # Pre-process product info for HTML templates
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/%s" % (row[2]),
            "price": "$%.2f" % (row[3]/100.0),
            "stock": "%d left" % (row[4]),
        })
    
    # Display total sales so far
    cur.execute("SELECT SUM(value) FROM transactions")
    result = cur.fetchone()[0]
    earnings = result/100.0 if result else 0

    return render_template("index.html", products=products, earnings=earnings)

@app.route("/buy/<product_id>")
def buy(product_id):
    if not product_id:
        return render_template("message.html", message="Invalid product ID!")

    (cur, conn) = get_cursor()

    cur.execute("SELECT rowid, price, stock FROM products WHERE rowid = ?", (product_id,))
    result = cur.fetchone()

    if not result:
        return render_template("message.html", message="Invalid product ID!")
    (rowid, price, stock) = result

    if stock <= 0:
        return render_template("message.html", message="Insufficient stock!")

    print("Processed transaction of value $%.2f" % (price/100.0))
    cur.execute("INSERT INTO transactions (timestamp, productid, value) VALUES " + \
        "(datetime(), ?, ?)", (rowid, price))

    cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = ?", (product_id,))
    conn.commit()
    return render_template("message.html", message="Purchase successful!")

@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    print(f'price = {price}, quantity = {quantity}')
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        print(file_ext)
        if file_ext in current_app.config['UPLOAD_EXTENSIONS']:
            file_name = filename.split(".")[0]
            (cur, conn) = get_cursor()
            cur.execute("SELECT rowid, price, stock FROM products WHERE name = ?", (file_name,))
            result = cur.fetchone()
            if result and result[1] == price:
                cur.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (quantity,file_name,))
                conn.commit()
            else:
                image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                uploaded_file.save(os.path.join("static/",image_path))
                (cur, conn) = get_cursor()
                cur.execute("INSERT INTO products (name, imgpath, price, stock) VALUES (?,?,?,?)" , (filename.split(".")[0], image_path, price, quantity))
                conn.commit()
    return redirect(url_for('upload'))

@app.route("/reset")
def reset():
    initialize_db()
    return render_template("message.html", message="Database reset. Page back to Initial stage")

if __name__ == '__main__':
    initialize_db()
    app.run(debug = True)