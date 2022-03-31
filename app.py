from flask import Flask, redirect, url_for, request, render_template, make_response, session
from werkzeug.exceptions import MethodNotAllowed
from pymongo import MongoClient, cursor
from twilio.rest import Client
import pymongo
import datetime

# TWILIO
account_sid = 'AC943b891cffa631549e0a27d790e889b3'
auth_token = '7b52eef6001bb53360367ec68d1734ed'
TwilioClient = Client(account_sid, auth_token)
#############################################################

#############################################################
client = pymongo.MongoClient(
    "mongodb+srv://rraya:rubenraya@cluster0.w9ojs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Escuela
cuentas = db.alumno

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"


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
    # TWILIO
    message = TwilioClient.messages.create(
        from_='whatsapp:+14155238886',
        body='Hola %s! Hay un nuevo inicio de sesión' % email,
        to='whatsapp:+5215514200581'
    )
    print(message.sid)
    ############################################################
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
def getcookie():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))


@app.route('/homepage')
def homepage():
    return render_template('HomePage.html')


@app.route('/create_form')
def create_form():
    return render_template('CreateForm.html')


@app.route('/insert', methods=["POST"])
def insert():

    user = {
        "matricula": request.form['matricula'],
        "nombre": request.form['nombre'],
        "correo": request.form['correo'],
        "contrasena": request.form['contrasena']
    }
    try:
        cuentas.insert_one(user)
        return redirect(url_for('find_all'))

    except Exception as e:
        return '<p>Unexpected error: %s %s </p>' % type(e), e


@app.route('/update', methods=['POST'])
def update():

    try:
        filter = {"matricula": request.form['matricula']}
        user = {"$set": {
            "matricula": request.form['matricula'], "nombre": request.form['nombre'], "correo": request.form['correo'], "contrasena": request.form['contrasena']}}
        cuentas.update_one(filter, user)
        return redirect(url_for('find_all'))

    except Exception as e:
        return '<p>Unexpected error: %s %s </p>' % type(e), e


@app.route('/find_one/<matricula>')
def find_one(matricula):
    cursor = cuentas.find_one({"id": (matricula)})
    return '<b>find : %s!</b>' % (cursor)


@app.route('/delete/<matricula>')
def delete(matricula):
    cursor = cuentas.delete_one({'matricula': (matricula)})
    if cursor.deleted_count == 0:
        return '<b>El registro no esta...!!</b>'
    else:
        return redirect(url_for('find_all'))


@app.route('/find_all')
def find_all():
    cursor = cuentas.find({})
    user = []
    for doc in cursor:
        user.append(doc)

    return render_template("/Retrieve.html", data=user)
    # return '<b>Nombre: %s!</b>' % (user.nombre)


@app.route("/empty")
def empty():
    cursor = cuentas.find({})
    user = []
    for doc in cursor:
        user.append(doc)

    return render_template("/empty.html", data=user)

@app.route('/home')
def homeS():
    return render_template('home.html')


@app.route('/login')
def loginSinple():
    return render_template('login.html')

@app.route('/loginfull')
def loginFull():
    return render_template('LoginFull.html')


@app.route('/loginfull2')
def LoginFull2():
    return render_template('LoginFull2.html')
