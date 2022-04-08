from flask import Flask, render_template, request

# FlASK
#############################################################
app = Flask(__name__)
#############################################################


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "GET"):
        return render_template("Login.html", data="email")
    else:
        email = None
        email = request.form["email"]
        password = request.form["password"]
        return render_template("index.html", data=email)
