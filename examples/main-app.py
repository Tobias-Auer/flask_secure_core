from flask import Flask, render_template, request, redirect, url_for


import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import flask_secure_core as fsl

app = Flask(__name__)

fsl.init_fsl(
    app,
    db_name="fsl",
    db_user="fsl",
    db_password="fsl"
)

app.config.from_pyfile('FlaskConfig.py')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ex1")
@app.require_login()

def example1():
    return "Only available when the user is logged in."

@app.route("/ex2")
@app.require_permission("2")

def example2():
    return "Only available when the user has staff privileges."

@app.route("/ex3")
@app.require_permission("1")
def example3():
    return "Only available when the user is an admin."

@app.route("/ex4")
@app.require_permission("0")
def example4():
    return "Only available when the user is a superuser."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
