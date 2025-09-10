from flask import Flask, render_template, request, redirect, url_for


import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import flask_secure_core

app = Flask(__name__)

flask_secure_core.init_fsl(
    app,
    db_name="fsl",
    db_user="fsl",
    db_password="fsl"
)


@app.route("/")
def index():
    return render_template("index.html")


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
    app.run(host="0.0.0.0", port=5000, debug=True)
