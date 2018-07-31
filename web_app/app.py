import sys, os
import flask_admin
from flask_security import SQLAlchemyUserDatastore, Security
sys.path.append(os.getcwd() + '/web_app')
from flask_admin import Admin, helpers as admin_helpers
from flask import Flask, render_template, request, session, url_for
from models import db, Ikan, Pembeli, User, Role
from views import ViewIkan, ViewPembeli, MyModelView


def buat_app():

    app = Flask(__name__, static_folder='files')

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Create admin
    admin = flask_admin.Admin(app,'Admin Dashboard',base_template='my_master.html',template_mode='bootstrap3')

    # admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewIkan(Ikan, db.session))
    admin.add_view(ViewPembeli(Pembeli, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

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


        if request.method == "POST":
            return render_template('detail_ikan.html')
        else:
            pass

        return render_template("ikan.html", IKANS=urutan_ikan_dalam_tampilan_halaman)

    @app.route('/detail_ikan/<id_ikan>', methods = ["GET", "POST"])
    def detail_ikan(id_ikan=None):


        foto_ikan = request.args.get('foto_ikan')

        id_ikan = Ikan.query.filter_by(id_ikan=id_ikan).first()
        id_ikan = id_ikan.id_ikan
        nama_ikan = Ikan.query.filter_by(id_ikan=id_ikan).first()
        nama_ikan = nama_ikan.nama_ikan
        keterangan_ikan = Ikan.query.filter_by(id_ikan=id_ikan).first()
        keterangan_ikan = keterangan_ikan.keterangan_ikan
        berat_ikan_dalam_Kg = Ikan.query.filter_by(id_ikan=id_ikan).first()
        berat_ikan_dalam_Kg = berat_ikan_dalam_Kg.berat_ikan_dalam_Kg
        minimal_order_dalam_Kg = Ikan.query.filter_by(id_ikan=id_ikan).first()
        minimal_order_dalam_Kg = minimal_order_dalam_Kg.minimal_order_dalam_Kg
        harga_per_Kg = Ikan.query.filter_by(id_ikan=id_ikan).first()
        harga_per_Kg = harga_per_Kg.harga_per_Kg

        if request.method == "get":
            pesan_berapa_kg = request.form.get('pesan_berapa_kg')
            return render_template("form_data_pembeli.html")

        session['NAMA_IKAN'] = nama_ikan
        session['KETERANGAN_IKAN'] = keterangan_ikan
        session['BERAT_IKAN_DALAM_KG'] = berat_ikan_dalam_Kg
        session['MINIMAL_ORDER_DALAM_KG'] = minimal_order_dalam_Kg
        session['HARGA_PER_KG'] = harga_per_Kg
        session['ID_IKAN'] = id_ikan



        return render_template("detail_ikan.html", ID_IKAN=id_ikan, NAMA_IKAN=nama_ikan, BERAT_IKAN= berat_ikan_dalam_Kg,
                               HARGA_IKAN=harga_per_Kg, KETERANGAN_IKAN=keterangan_ikan, MINIMAL_ORDER=minimal_order_dalam_Kg,
                               FOTO_IKAN=foto_ikan)



    @app.route('/form_pemesan', methods = ["GET", "POST"])
    def form_pemesan(status_pembayarans="pending"):

        if 'HARGA_PER_KG' in session.keys():
            harga_per_Kg = session['HARGA_PER_KG']
        else:
            harga_per_Kg = None

        pesan_berapa_kg = request.args.get('pesan_berapa_kg')
        harga_total_pesanan = int(harga_per_Kg) * int(pesan_berapa_kg)
        session['HARGA_TOTAL_PESANAN'] = harga_total_pesanan

        if request.method == 'POST':

            import string
            import random
            def generator_random(size=6, chars=string.ascii_uppercase + string.digits):
                return ''.join(random.choice(chars) for x in range(size))

            generate_invoice = 'IF' + generator_random() + 'INV'
            kode_pembeli = generate_invoice


            nama_pemesan = request.form.get('nama_pemesan')
            no_hp_or_wa = request.form.get('no_hp_or_wa')
            alamat_lengkap = request.form.get('alamat_lengkap')

            import time
            tanggal_pesanan_invoice = time.strftime("%d/%m/%Y")
            tanggal_pemesanan = time.strftime("%Y-%m-%d %H:%M:%S")
            # tanggal_pemesanan_untuk_admin = time.strftime("%Y-%m-%d %H:%M:%S")

            ikan_id = session['ID_IKAN']
            nama_ikan = session['NAMA_IKAN']
            pesan_berapa_kg = pesan_berapa_kg
            session['PESAN_BERAPA_KG'] = pesan_berapa_kg
            pesan_berapa_kg = session['PESAN_BERAPA_KG']
            harga_per_Kg = session['HARGA_PER_KG']
            harga_total_pesanan = session['HARGA_TOTAL_PESANAN']
            status_pembayaran = status_pembayarans
            insert_to_db = Pembeli(ikan_id, kode_pembeli, nama_pemesan, no_hp_or_wa, alamat_lengkap, nama_ikan, pesan_berapa_kg,
                                   harga_total_pesanan, tanggal_pemesanan, status_pembayaran)
            db.session.add(insert_to_db)
            db.session.commit()


            return render_template('invoice.html', NAMA_IKAN=nama_ikan, JUMLAH_PESANAN=pesan_berapa_kg,
                                   HARGA_SATU_IKAN=harga_per_Kg, HARGA_TOTAL=harga_total_pesanan,
                                   TANGGAL_PESANAN=tanggal_pesanan_invoice, KODE_INVOICE=kode_pembeli,
                                   NAMA_PEMBELI=nama_pemesan, ALAMAT_PEMBELI=alamat_lengkap, NOMOR_HP_PEMBELI=no_hp_or_wa)

        return render_template("form_data_pembeli.html")


    @app.route('/invoice')
    def invoice():
        return render_template("invoice.html")

    @app.route('/nearby')
    def nearby():

        return render_template("nearby_places.html")

    return app