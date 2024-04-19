from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    title = ""
    return render_template("index.html",title=title)
@app.route('/login')
def login():
    title = "Login"
    return render_template("index.html",title=title)


