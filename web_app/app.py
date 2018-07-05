import sys, os

from flask_admin import Admin

sys.path.append(os.getcwd() + '/web_app')

from flask import Flask, render_template, request, session

from models import db, Ikan, Pembeli
from views import ViewIkan, ViewPembeli


def buat_app():


    app = Flask(__name__, static_folder='files')

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewIkan(Ikan, db.session))
    admin.add_view(ViewPembeli(Pembeli, db.session))

    @app.route('/', methods=['POST','GET'])
    def ikan(fish=None, id_ikan=None):

        ikan = Ikan()
        #
        if fish is not None:
            ikan = Ikan.query.filter_by(nama_ikan=fish).first()
        else:
            pass
        #
        urutan_ikan_dalam_tampilan_halaman = Ikan.query.order_by('urutan_ikan_dalam_tampilan_halaman')
        #
        if ikan is not None:
            id_ikan = ikan.query.first()
            id_ikan = ikan.id_ikan
            nama_ikan = ikan.query.first()
            nama_ikan = ikan.nama_ikan
            keterangan_ikan = ikan.query.first()
            keterangan_ikan = ikan.keterangan_ikan
            berat_ikan_dalam_Kg = ikan.query.first()
            berat_ikan_dalam_Kg = ikan.berat_ikan_dalam_Kg
            minimal_order_dalam_Kg = ikan.query.first()
            minimal_order_dalam_Kg = ikan.minimal_order_dalam_Kg
            harga_per_Kg = ikan.query.first()
            harga_per_Kg = ikan.harga_per_Kg
            fish_foto = ikan.query.first()
            fish_foto = ikan.foto_ikan

        session['ID_IKAN'] = id_ikan
        session['NAMA_IKAN'] = nama_ikan
        session['KETERANGAN_IKAN'] = keterangan_ikan
        session['BERAT_IKAN_DALAM_KG'] = berat_ikan_dalam_Kg
        session['MINIMAL_ORDER_DALAM_KG'] = minimal_order_dalam_Kg
        session['HARGA_PER_KG'] = harga_per_Kg
        # session['FOTO_IKAN'] = fish_foto

        if request.method == "get":
            return render_template('detail_ikan.html')
        else:
            pass

        return render_template("ikan.html", IKANS=urutan_ikan_dalam_tampilan_halaman)

    @app.route('/detail_ikan/<id_ikan>', methods = ["GET", "POST"])
    def detail_ikan(id_ikan=None):

        nama_ikan = request.args.get('nama_ikan')
        keterangan_ikan = request.args.get('keterangan_ikan')
        berat_ikan_dalam_Kg = request.args.get('berat_ikan_dalam_Kg')
        minimal_order_dalam_Kg = request.args.get('minimal_order_dalam_Kg')
        harga_per_Kg = request.args.get('harga_per_Kg')
        foto_ikan = request.args.get('foto_ikan')


        return render_template("detail_ikan.html", ID_IKAN=id_ikan,
                               NAMA_IKAN=nama_ikan, BERAT_IKAN= berat_ikan_dalam_Kg, HARGA_IKAN=harga_per_Kg,
                               KETERANGAN_IKAN=keterangan_ikan, MINIMAL_ORDER=minimal_order_dalam_Kg, FOTO_IKAN=foto_ikan)



    @app.route('/form_pemesan', methods = ["GET", "POST"])
    def form_pemesan():
        if request.method == 'get':
            return render_template('invoice.html')
        return render_template("form_data_pembeli.html")


    @app.route('/invoice')
    def invoice():
        return render_template("invoice.html")



    return app