import flask
from flask import Flask, Response, request, render_template, redirect, url_for
import flask_login

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

