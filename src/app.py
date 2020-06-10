from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/<string:name>")
def hello_world(name=None):
    return render_template("hello.html", name=name)

@app.route("/")
def hi():
    return "Hello"
