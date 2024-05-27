import sqlite3, os, hashlib
from flask import Flask, jsonify, render_template, request, g

app = Flask(__name__)
app.database = "sample.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/restock')
def restock():
    return render_template('restock.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        uname,pword = (request.form['username'],request.form['password'])
        g.db = connect_db()
        cur = g.db.execute("SELECT * FROM employees WHERE username = '%s' AND password = '%s'" %(uname, hash_pass(pword)))
        if cur.fetchone():
            g.db.close()        
            return render_template("admin.html")
        g.db.close()                

    return render_template("login.html")
# #API routes
# @app.route('/api/v1.0/storeLoginAPI/', methods=['POST'])
# def loginAPI():
#     if request.method == 'POST':
#         uname,pword = (request.json['username'],request.json['password'])
#         g.db = connect_db()
#         cur = g.db.execute("SELECT * FROM employees WHERE username = '%s' AND password = '%s'" %(uname, hash_pass(pword)))
#         if cur.fetchone():
#             return render_template("admin.html")
#         else:
#             result = {'status': 'fail'}
#         g.db.close()
#         return jsonify(result)



@app.route('/api/v1.0/storeAPI', methods=['GET'])
def storeapi():
    if request.method == 'GET':
        g.db = connect_db()
        curs = g.db.execute("SELECT * FROM shop_items")
        cur2 = g.db.execute("SELECT * FROM employees")
        items = [{'items':[dict(name=row[0], quantity=row[1], price=row[2]) for row in curs.fetchall()]}]
        empls = [{'employees':[dict(username=row[0], password=row[1]) for row in cur2.fetchall()]}]
        g.db.close()
        return jsonify(items+empls)

@app.route('/api/v1.0/storeAPI/<item>', methods=['GET'])
def searchAPI(item):
    g.db = connect_db()
    #curs = g.db.execute("SELECT * FROM shop_items WHERE name=?", item) #The safe way to actually get data from db
    curs = g.db.execute("SELECT * FROM shop_items WHERE name = '%s'" %item)
    results = [dict(name=row[0], quantity=row[1], price=row[2]) for row in curs.fetchall()]
    g.db.close()
    return jsonify(results)

@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error)

def connect_db():
    return sqlite3.connect(app.database)

# Create password hashes
def hash_pass(passw):
	m = hashlib.md5()
	m.update(passw.encode('utf-8'))
	return m.hexdigest()

if __name__ == "__main__":

    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        with sqlite3.connect(app.database) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE shop_items(name TEXT, quantitiy TEXT, price TEXT)""")
            c.execute("""CREATE TABLE shop_items_old(quantitiy NUMBER, price TEXT)""")
            c.execute("""CREATE TABLE employees(username TEXT, password TEXT)""")
            c.execute('INSERT INTO shop_items VALUES("water", "40", "100")')
            c.execute('INSERT INTO shop_items VALUES("juice", "40", "110")')
            c.execute('INSERT INTO shop_items VALUES("candy", "100", "10")')
            

            c.execute('INSERT INTO shop_items_old VALUES("1", "67")')
            c.execute('INSERT INTO shop_items_old VALUES("3", "70")')
            c.execute('INSERT INTO shop_items_old VALUES("4", "123")')
            c.execute('INSERT INTO shop_items_old VALUES("17", "116")')
            c.execute('INSERT INTO shop_items_old VALUES("19", "125")')
            c.execute('INSERT INTO shop_items_old VALUES("6", "104")')
            c.execute('INSERT INTO shop_items_old VALUES("7", "105")')
            c.execute('INSERT INTO shop_items_old VALUES("8", "53")')
            c.execute('INSERT INTO shop_items_old VALUES("12", "95")')
            c.execute('INSERT INTO shop_items_old VALUES("5", "84")')
            c.execute('INSERT INTO shop_items_old VALUES("13", "53")')
            c.execute('INSERT INTO shop_items_old VALUES("14", "112")')
            c.execute('INSERT INTO shop_items_old VALUES("15", "97")')
            c.execute('INSERT INTO shop_items_old VALUES("2", "84")')
            c.execute('INSERT INTO shop_items_old VALUES("9", "95")')
            c.execute('INSERT INTO shop_items_old VALUES("10", "105")')
            c.execute('INSERT INTO shop_items_old VALUES("11", "53")')
            c.execute('INSERT INTO shop_items_old VALUES("16", "114")')
            c.execute('INSERT INTO shop_items_old VALUES("18", "97")')

            c.execute('INSERT INTO employees VALUES("ram", "{}")'.format(hash_pass("mainhibataunga")))
            c.execute('INSERT INTO employees VALUES("shyam", "{}")'.format(hash_pass("chickennoodles")))
            c.execute('INSERT INTO employees VALUES("ghanshyam", "{}")'.format(hash_pass("selvamSirZindabad")))
            connection.commit()
            connection.close()

    app.run() # runs on machine ip address to make it visible on netowrk
