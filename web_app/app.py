import sys, os

from flask_admin import Admin

sys.path.append(os.getcwd() + '/web_app')

from flask import Flask, render_template, request

from models import db, Ikan, Pembeli
from views import ViewIkan, ViewPembeli


def buat_app():


    app = Flask(__name__, static_folder='files')

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewIkan(Ikan, db.session))
    admin.add_view(ViewPembeli(Pembeli, db.session))


    # @app.route('/')
    # def index():
    #     return render_template("base-template.html")

    @app.route('/')
    @app.route('/<uri>')
    def ikan(uri=None):
        ikan = Ikan()
        if uri is not None:
            ikan = Ikan.query.filter_by(url=uri).first
        else:
            pass

        urutan_ikan_dalam_tampilan_halaman = Ikan.query.order_by('urutan_ikan_dalam_tampilan_halaman')

        return render_template("ikan.html", IKANS=urutan_ikan_dalam_tampilan_halaman)

    @app.route('/form_pemesan', methods = ["GET", "POST"])
    def form_pemesan():
        if request.method == 'get':
            return render_template('invoice.html')
        return render_template("form_data_pembeli.html")

    @app.route('/invoice')
    def invoice():
        return render_template("invoice.html")


    return app