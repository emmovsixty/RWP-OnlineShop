import random
from flask import redirect, render_template, Flask, request, session, url_for
from lib_platform import username
from flask_mysqldb import MySQL, MySQLdb
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.secret_key = 'sport21'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'sport_store_db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)
# conn = mysql.connection.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registeruser',methods=['GET','POST'])
def registeruser():
    status = False
    if request.method == 'POST':
        username = request.form['Username']
        nama = request.form['nama']
        emailUser = request.form['emailUser']
        pswdUser = request.form['pwUser']
        conn = mysql.connection.cursor()
        conn.execute('INSERT INTO user(username,name,email,password) VALUES (%s,%s,%s,%s)',(username,nama,emailUser,pswdUser))
        mysql.connection.commit()
        conn.close()
        return redirect(url_for('loginuser'))
    return render_template('registrasiuser.html', status = status)


@app.route('/registeradmin',methods=['GET','POST'])
def registeradmin():
    status = False
    if request.method == 'POST':
        usernameadm = request.form['username-admin']
        namaadm = request.form['nama-admin']
        emailadm = request.form['email-admin']
        pswdadm = request.form['pswd-admin']
        conn = mysql.connection.cursor()
        conn.execute('INSERT INTO admin(username_adm,nama_adm,email_adm,pswd_adm) VALUES (%s,%s,%s,%s)',(usernameadm,namaadm,emailadm,pswdadm))
        mysql.connection.commit()
        conn.close()
        return redirect(url_for('loginadmin'))
    return render_template('registeradmin.html', status = status)


@app.route('/loginuser', methods=['GET','POST'])
def loginuser():
    if request.method == 'POST' and 'input-email' in request.form and 'input-password' in request.form:
        email = request.form['input-email']
        pswd = request.form['input-password']
        conn =  mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('SELECT * FROM user WHERE email = %s and password = %s',(email,pswd))
        account = conn.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['username'] = account['username']
            session['name'] = account['name']
            session['no_hp'] = account['no_telfon']
            session['alamat'] = account['alamat']
            return redirect(url_for('home'))
    return render_template('loginuser.html')


@app.route('/loginadmin', methods=['GET','POST'])
def loginadmin():
    if request.method == 'POST' and 'input-email-adm' in request.form and 'input-password-adm' in request.form:
        email_adm = request.form['input-email-adm']
        pswd = request.form['input-password-adm']
        conn =  mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('SELECT * FROM admin WHERE email_adm = %s and pswd_adm = %s',(email_adm,pswd))
        account = conn.fetchone()
        if account:
            session['loggedin'] = True
            session['email-adm'] = account['email_adm']
            session['username-adm'] = account['username_adm']
            session['nama_adm'] = account['nama_adm']
            return redirect(url_for('admin'))
    return render_template('loginadmin.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/pesanan')
def pesanan():
    return render_template('pesanan.html')

@app.route('/produku')
def produku():
    return render_template('produku.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/tambah_produk',methods=['POST','GET'])
def tambah_produk():
    if request.method == 'POST':
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        angka = '123456789'
        ang = ''.join(random.sample(angka,3))
        hur = ''.join(random.sample(upper,7))
        kode = ang+hur
        nama_produk = request.form['nama-produk']
        harga = request.form['harga']
        kategori = request.form['kategori']
        jumlah = request.form['jumlah']
        variasi = request.form['variasi']
        deskripsi = request.form['deskripsi']
        files = request.files.getlist('files[]')
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                mysql.connection.commit()
                conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                conn.execute('INSERT INTO produk (kode_produk,nama_produk,kategori,jumlah,deskripsi,harga,variasi,gambar) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(kode,nama_produk,kategori,jumlah,deskripsi,harga,variasi,filename,))
                mysql.connection.commit()
                conn.close()
                return redirect(url_for('admin'))
    return render_template('tambah_produk.html')

@app.route('/profile')
def profile():
    # conn = mysql.connection.cursor()
    # conn.execute('SELECT * FROM user')
    # data = conn.fetchall()
    # mysql.connection.commit()
    # conn.close()
    return render_template('profile.html')

@app.route('/shop-singel')
def shop_single():
    return render_template('singel-shop.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/admin')
def admin():
    conn = mysql.connection.cursor()
    conn.execute('SELECT * FROM produk')
    data = conn.fetchall()
    conn.close()
    return render_template('admin.html', data=data)

# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)