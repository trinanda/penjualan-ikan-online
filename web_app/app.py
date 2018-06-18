import sys, os
sys.path.append(os.getcwd() + '/web_app')

from flask import Flask, render_template

from models import db


def buat_app():


    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')


    return app