import sys, os
sys.path.append(os.getcwd() + '/web_app')

from flask import Flask, render_template, request

from models import db


def buat_app():


    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template("base-template.html")

    @app.route('/ikan')
    def ikan():
        return render_template("ikan.html")

    @app.route('/form_pemesan', methods = ["GET", "POST"])
    def form_pemesan():
        if request.method == 'get':
            return render_template('invoice.html')
        return render_template("form_data_pembeli.html")

    @app.route('/invoice')
    def invoice():
        return render_template("invoice.html")


    return app