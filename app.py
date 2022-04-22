from http import client
from flask import Flask, redirect, url_for, request, render_template, session
import datetime
import pymongo

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"
#############################################################


# MONGODB
#############################################################
mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Escuela
cuentas = db.alumno
#############################################################


@app.route('/')
def home():
    email = None
    if 'email' in session:
        email = session['email']
    return render_template('index.html', error=email)


@app.route('/login', methods=['GET'])
def login():
    email = None
    if 'email' in session:
        email = session['email']
        return render_template('index.html', error=email)

    return render_template('login.html', error=email)


@app.route('/login', methods=['POST'])
def login2Index():
    email = ""
    if 'email' in session:
        return render_template('index.html', error=email)

    email = request.form['email']
    password = request.form['password']
    session['email'] = email
    session['password'] = password

    return render_template('index.html', error=email)


@app.route('/signup', methods=['POST'])
def signup():
    email = ""
    if 'email' in session:
        return render_template('index.html', error=email)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        session['password'] = password
        session['name'] = name
    return render_template('index.html', error=email)


@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/usuarios.html", data=users)


@app.route("/insert")
def insertUsers():
    user = {
        "matricula": "1",
        "nombre": "Ruben Raya",
        "correo": "rraya@tec.mx",
        "contrasena": "1234",
    }

    try:
        cuentas.insert_one(user)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no esta disponible =>: %s %s" % type(e), e
