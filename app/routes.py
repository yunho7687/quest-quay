from app import app
@app.route('/')
@app.route('/index')
def index():
    return "Hellooooooo, World!<p style='color:red' >Welcome to CITS5505 good luck. </p>"

