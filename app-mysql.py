from flask import Flask, render_template, request, redirect, url_for, cli
import datetime 
import os
from dotenv import load_dotenv

load_dotenv()
cli.show_server_banner = lambda *x: None

## if using mysql
import mysql.connector
def db_conn():
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    return mysql.connector.connect(user=db_user, password=db_pass, host=db_host, database=db_name)

## if using sqlite
# import sqlite3
# def db_conn():
#     return sqlite3.connect('berita.db')

def get_post(id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_berita WHERE id = %s', (id,))
    res = cursor.fetchall()[0]
    conn.close()
    return res

def fetchAll():
    conn = db_conn()
    cursor = conn.cursor()
    query = ("SELECT * from tbl_berita ORDER BY id")
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

app = Flask("berita")

@app.route("/")
def home():
    table = fetchAll()
    return render_template("table.html", table=table, c=len(table))

@app.route("/search")
def search():
    q = '%' + request.args.get('query') + '%'
    
    conn = db_conn()
    cursor = conn.cursor()
    query = ("SELECT * from tbl_berita where judul like %s ORDER BY id")
    cursor.execute(query, (q, ))
    res = cursor.fetchall()
    conn.close()

    return render_template("table.html", table=res, c=len(res))

@app.route("/view")
def view():
    id = request.args.get('id')
    data = get_post(id)
    isi = data[3].replace('\\\\n', '\n').replace('\\\\r', '\r').replace('\\r', '\r').replace('\\n', '\n').replace('\r', '')
    return render_template('view.html', data=data, isi=isi.split('\n'))

@app.route("/edit")
def edit():
    id = request.args.get('id')
    data = get_post(id)
    isi = data[3].replace('\\\\n', '\n').replace('\\\\r', '\r').replace('\\r', '\r').replace('\\n', '\n').replace('\r', '')
    return render_template('edit.html', data=data, isi=isi)

@app.route("/update")
def update():
    id = request.args.get('id')
    judul = request.args.get('judul')
    isi = request.args.get('isi')
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    query = "UPDATE tbl_berita SET judul = %s, tanggal = %s, isi = %s WHERE id = %s"

    conn = db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (judul, date, isi, id,))
        conn.commit()
    except:
        print("error occured")
    conn.close()
    return redirect('/')


@app.route("/create")
def create():
    return render_template('create.html')

@app.route("/store")
def store():
    judul = request.args.get('judul')
    isi = request.args.get('isi')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = fetchAll()
    id = data.pop()[0]+1
    query = "INSERT INTO tbl_berita (id, judul, tanggal, isi) values (%s, %s, %s, %s)"

    conn = db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (id, judul, date, isi,))
        conn.commit()
    except:
        print("error occured")
    conn.close()
    return redirect('/')

@app.route("/delete")
def delete():
    id = request.args.get('id')
    query = "delete from tbl_berita where id = %s"

    conn = db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (id, ))
        conn.commit()
    except:
        print("error occured")
    conn.close()
    return redirect('/')
    
port = os.getenv('PORT')
print("server running on http://localhost:"+str(port))
app.run(host='0.0.0.0', port=port, debug=False)
