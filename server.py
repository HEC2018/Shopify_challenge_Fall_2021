from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename

from flask.globals import current_app
#import imghdr
app = Flask(__name__)

app.config['UPLOAD_PATH'] = 'images/'

# restrict extensions for security
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']

# database cursor
def get_cursor():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    return (cur, conn)

# Initialize the sqlite database and fill up the `products` table with sample data.
def initialize_db():
    (cur, conn) = get_cursor()

    # Create products table with the sample data
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT, price INTEGER, stock INTEGER)")
    cur.execute("""INSERT INTO products (name, imgpath, price, stock) VALUES \
        ('University of Waterloo logo', 'images/Uwaterloo.png', 120, 999), \
        ('CN_Tower', 'images/CN-Tower-Toronto.jpg', 1000000000, 0), \
        ('Shopify logo', 'images/shopify.png', 2000, 666), \
        ('Many Books', 'images/book.jpg', 47900, 312)
    """)

    # Create an empty transactions table
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("CREATE TABLE transactions (timestamp TEXT, productid INTEGER, value INTEGER)")
    
    # Commit the db changes
    conn.commit()
    print("Initialize database")

# Clear all tables in the database
def initialize_db_clear():
    (cur, conn) = get_cursor()
    cur.execute("DELETE FROM products")
    conn.commit()
    print("All cleared")

# Home_page 
@app.route("/")
def home_page():
    (cur, _) = get_cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    
    # Pre-process all product info for HTML5 templates later
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/%s" % (row[2]),
            "price": "$%.2f" % (row[3]/100.0),
            "stock": "%d left" % (row[4]),
        })
    
    # Prepare the display for total sales 
    cur.execute("SELECT SUM(value) FROM transactions")
    result = cur.fetchone()[0]
    earnings = result/100.000 if result else 0

    return render_template("index.html", products = products, earnings = earnings)

# Purchase button on main page
@app.route("/buy/<product_id>")
def buy(product_id):
    # Try purchasing nothing. Invalid
    if not product_id:
        return render_template("message.html", message="Invalid product ID!")

    (cur, conn) = get_cursor()

    cur.execute("SELECT rowid, price, stock FROM products WHERE rowid = ?", (product_id,))
    result = cur.fetchone()

    # Try purchasing something not in database. Invalid
    if not result:
        return render_template("message.html", message="Invalid product ID!")
    
    (rowid, price, stock) = result
    # Not enough stock in inventory
    if stock <= 0:
        return render_template("message.html", message="Insufficient stock!")

    print("Processed transaction of value $%.2f" % (price/100.0))
    cur.execute("INSERT INTO transactions (timestamp, productid, value) VALUES " + \
        "(datetime(), ?, ?)", (rowid, price))

    cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = ?", (product_id,))
    conn.commit()
    return render_template("message.html", message="Purchase successful!")

# Clear all button on main page
@app.route('/clear_all')
def clear():
    initialize_db_clear()
    return render_template("message.html", message="Clear all images inventory. Back to the main stage")

# Upload button on main page
@app.route('/upload')
def upload():
    return render_template("upload.html")

# Upload functionalities for upload page
@app.route('/upload', methods=['POST'])
def upload_file():
    # Obtain info from an HTTP request
    uploaded_file = request.files['file']
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    print(f'price = {price}, quantity = {quantity}')
    filename = secure_filename(uploaded_file.filename)
    if filename != '': # check if uploaded a file
        file_ext = os.path.splitext(filename)[1].lower()
        print(file_ext)
        # Extension sanity check
        if file_ext in current_app.config['UPLOAD_EXTENSIONS']:
            file_name = filename.split(".")[0]
            (cur, conn) = get_cursor()
            cur.execute("SELECT rowid, price, stock FROM products WHERE name = ?", (file_name,))
            result = cur.fetchone()
            # Duplicate checking
            if result and result[1] == price:
                cur.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (quantity,file_name,))
                conn.commit()
            else:
                # Put up new rows
                image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                uploaded_file.save(os.path.join("static/",image_path))
                (cur, conn) = get_cursor()
                cur.execute("INSERT INTO products (name, imgpath, price, stock) VALUES (?,?,?,?)" , (filename.split(".")[0], image_path, price, quantity))
                conn.commit()
    return redirect(url_for('upload'))

# Reset button on the main page
@app.route("/reset")
def reset():
    initialize_db()
    return render_template("message.html", message="Database reset. Page back to Initial stage")

if __name__ == '__main__':
    initialize_db()
    app.run(debug = True)