from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to the Main Example App!"

@app.route("/ex1")
def example1():
    return "Only available when the user is logged in."

@app.route("/ex2")
def example2():
    return "Only available when the user has staff privileges."

@app.route("/ex3")
def example3():
    return "Only available when the user is an admin."

@app.route("/ex4")
def example4():
    return "Only available when the user is a superuser."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
