from app import app
from flask import render_template

@app.route('/')
def roof():
    return "Hellooooooo, World!<p style='color:red' >Welcome to CITS5505 good luck. </p>"


@app.route('/index')
def index():
    return render_template("index.html")

