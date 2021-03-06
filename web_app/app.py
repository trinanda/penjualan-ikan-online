import sys, os
import flask_admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password, login_user, logout_user
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pdfkit
from geopy import Nominatim
from twilio.rest import Client
from werkzeug.utils import redirect

from web_app.settings import TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER, TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER, \
    TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN, TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN

sys.path.append(os.getcwd() + '/web_app')
from flask_admin import helpers as admin_helpers
from flask import Flask, render_template, request, session, url_for, flash, make_response
from models import db, Ikan, Pembeli, Penjual, Role, Domisili
from views import ViewIkan, ViewPembeli, MyModelView, DomisiliView
from flask_wtf import FlaskForm, RecaptchaField
import string
import random
import geocoder
from form import RegisterFormView, LoginFormView, AddIkanForm, EditIkanForm


def buat_app():

    app = Flask(__name__, static_folder='files')

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    url_index = 'http://127.0.0.1:9999/'

    bootstrap = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, Penjual, Role)
    security = Security(app, user_datastore)

    # Create admin
    admin = flask_admin.Admin(app,'Admin Dashboard',base_template='my_master.html',template_mode='bootstrap3')

    # admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ViewIkan(Ikan, db.session))
    admin.add_view(ViewPembeli(Pembeli, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(Penjual, db.session))
    admin.add_view(DomisiliView(Domisili, db.session))

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

        ikan = Ikan('','','','','','','','')
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

        penjual_id = db.session.query(Penjual.id).join(Ikan).filter(Ikan.id_ikan == id_ikan).first()[0]

        penjual_cabang = db.session.query(Penjual.nama_toko).filter(Penjual.id == penjual_id).first()[0]

        print('penjual_id', penjual_id)
        print('penjual_cabang', penjual_cabang)

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
                               FOTO_IKAN=foto_ikan, PENJUAL_CABANG=penjual_cabang)



    @app.route('/form_pemesan', methods = ["GET", "POST"])
    def form_pemesan(status_pembayarans="pending"):

        if 'HARGA_PER_KG' in session.keys():
            harga_per_Kg = session['HARGA_PER_KG']
        else:
            harga_per_Kg = None

        pesan_berapa_kg = request.args.get('pesan_berapa_kg')
        harga_total_pesanan = int(harga_per_Kg) * int(pesan_berapa_kg)
        session['HARGA_TOTAL_PESANAN'] = harga_total_pesanan

        class LoginForm(FlaskForm):
            recaptcha = RecaptchaField()

        captha = LoginForm()
        if captha.validate_on_submit():
            if request.method == 'POST':

                def generator_random(size=6, chars=string.ascii_uppercase + string.digits):
                    return ''.join(random.choice(chars) for x in range(size))

                generate_invoice = 'IF' + generator_random() + 'INV'
                kode_pembeli = generate_invoice
                session['KODE_PEMBELI'] = kode_pembeli

                nama_pemesan = request.form.get('nama_pemesan')
                no_hp_or_wa = request.form.get('no_hp_or_wa')
                alamat_lengkap = request.form.get('alamat_lengkap')

                session['NAMA_PEMESAN'] = nama_pemesan
                session['NOMOR_HP_OR_WA'] = no_hp_or_wa
                session['ALAMAT_LENGKAP'] = alamat_lengkap

                import time
                tanggal_pesanan_invoice = time.strftime("%d/%m/%Y")
                tanggal_pemesanan = time.strftime("%Y-%m-%d %H:%M:%S")
                # tanggal_pemesanan_untuk_admin = time.strftime("%Y-%m-%d %H:%M:%S")
                session['TANGGAL_PEMESANAN'] = tanggal_pesanan_invoice

                ikan_id = session['ID_IKAN']
                nama_ikan = session['NAMA_IKAN']
                pesan_berapa_kg = pesan_berapa_kg
                session['PESAN_BERAPA_KG'] = pesan_berapa_kg
                pesan_berapa_kg = session['PESAN_BERAPA_KG']
                harga_per_Kg = session['HARGA_PER_KG']
                harga_total_pesanan = session['HARGA_TOTAL_PESANAN']
                status_pembayaran = status_pembayarans

                msg_to_admin = "Pelanggan atas nama " + nama_pemesan + " dengan kode " + kode_pembeli + " dan nomor telepon " \
                               + no_hp_or_wa + " dan alamat " + alamat_lengkap + " telah memesan ikan " + nama_ikan + \
                               " sebanyak " + str(pesan_berapa_kg) + " dan harga total nya adalah " + str(harga_total_pesanan)
                message_to_pemesan = "Terima kasih " + nama_pemesan + " telah menggunakan layanan kami untuk memesan ikan, " + \
                                     " kami akan segera menghubungi Anda untuk melakukan verifikasi"

                #####################################################################
                #################
                ##### TWILIO ####
                ############################ SMS for User ###########################
                # for user notifications
                # Your Account SID from twilio.com/console
                # account_sid_user = TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER
                # # # # Your Auth Token from twilio.com/console
                # auth_token_user = TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER
                # # #
                # sms_client = Client(account_sid_user, auth_token_user)
                # # #
                # nomor_telepon_pemesan = no_hp_or_wa
                # try:
                #     message_pemesan = sms_client.messages.create(
                #         to=nomor_telepon_pemesan,
                #         from_="+12014307127",   # this upgraded number
                #         body=message_to_pemesan)
                # except:
                #     return '<h1 align="center">Pada kolom nomor telepon mohon masukan beserta kode negara <br> ' \
                #            'contoh: +628123123123</h1>'
                # print(message_pemesan.sid)
                #
                #
                # ####################################################################
                # ########################### SMS for Admin ##########################
                #
                # # for admin notifications
                # # Your Account SID from twilio.com/console
                # account_sid_admin = TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN
                # # # Your Auth Token from twilio.com/console
                # auth_token_admin = TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN
                #
                # sms_admin = Client(account_sid_admin, auth_token_admin)
                # message_admin = sms_admin.messages.create(
                #     to="++6282285250554",
                #     from_="+12132961837",  # this non upgrade number
                #     body=msg_to_admin)
                #
                # print(message_admin.sid)

                #####-->/ TWILIO ########
                ######################################################################

                insert_to_db = Pembeli(ikan_id, kode_pembeli, nama_pemesan, no_hp_or_wa, alamat_lengkap, nama_ikan, pesan_berapa_kg,
                                       harga_total_pesanan, tanggal_pemesanan, status_pembayaran)
                db.session.add(insert_to_db)
                db.session.commit()


                return render_template('invoice.html', NAMA_IKAN=nama_ikan, JUMLAH_PESANAN=pesan_berapa_kg,
                                       HARGA_SATU_IKAN=harga_per_Kg, HARGA_TOTAL=harga_total_pesanan,
                                       TANGGAL_PESANAN=tanggal_pesanan_invoice, KODE_INVOICE=kode_pembeli,
                                       NAMA_PEMBELI=nama_pemesan, ALAMAT_PEMBELI=alamat_lengkap, NOMOR_HP_PEMBELI=no_hp_or_wa)

        return render_template("form_data_pembeli.html", captha=captha)


    @app.route('/invoice', methods = ['GET', 'POST'])
    def invoice():
        nama_pemesan = session['NAMA_PEMESAN']
        alamat_lengkap = session['ALAMAT_LENGKAP']
        no_hp_or_wa = session['NOMOR_HP_OR_WA']
        nama_ikan = session['NAMA_IKAN']
        jumlah_pesanan = session['PESAN_BERAPA_KG']
        harga = session['HARGA_PER_KG']
        harga_total = session['HARGA_TOTAL_PESANAN']
        kode_pembeli = session['KODE_PEMBELI']
        tanggal_pemesanan = session['TANGGAL_PEMESANAN']

        if request.method == "POST":
            data_pdf = render_template("invoice.html", NAMA_IKAN=nama_ikan, JUMLAH_PESANAN=jumlah_pesanan,
                                           HARGA_SATU_IKAN=harga, HARGA_TOTAL=harga_total,
                                           TANGGAL_PESANAN=tanggal_pemesanan, KODE_INVOICE=kode_pembeli,
                                           NAMA_PEMBELI=nama_pemesan, ALAMAT_PEMBELI=alamat_lengkap, NOMOR_HP_PEMBELI=no_hp_or_wa)


            css = "web_app/static/style.css"
            pdf = pdfkit.from_string(data_pdf, False, css=css)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'applications/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'
            return response


    @app.route('/lokasi', methods = ['POST', 'GET'])
    def lokasi():
        if request.method == "get":
            cordinat = request.form.get('data')
            return render_template("nearby_places.html", STATE=cordinat)
        return render_template('lokasi.html')


    @app.route('/getvalue')
    def getvalue(current_user_position=None):

        cordinat = request.args.get('data')

        ######################### GEOPY #################################
        # geolocator = Nominatim(user_agent="jual_ikan")
        # location = geolocator.reverse(cordinat)
        # get_json_value = location.raw
        #
        # # get_village_name = get_json_value['address']['village']
        # get_county_name = get_json_value['address']['county']
        # get_state_name = get_json_value['address']['state']
        ######################### GEOPY #################################

        ######################### GEOCODER #################################
        try:
            g = geocoder.google(cordinat, method='reverse')
            get_county_name = g.json['county']
            get_state_name = g.json['state']
        except TypeError:
            return 'gagal mendapatkan kordinat, silahkan kembali dan ulangi!!!'
        ######################### GEOCODER #################################

        current_user_position_information = get_county_name + ', ' + get_state_name

        # print('g', g)
        print('get_county_name', get_county_name)
        print('get_state_name', get_state_name)

        urutan_ikan_dalam_tampilan_halamanerr = db.session.query(Ikan.id_ikan, Ikan.nama_ikan, Ikan.berat_ikan_dalam_Kg,Ikan.foto_ikan,
                                                                 Ikan.harga_per_Kg, Penjual).join(Penjual).filter(Penjual.domisili ==
                                                                                                                  get_county_name)

        print('gggg', urutan_ikan_dalam_tampilan_halamanerr)

        return render_template("nearby_places.html", IKANS=urutan_ikan_dalam_tampilan_halamanerr, CURRENT_LOCATION=current_user_position_information)


    @app.route('/nearby')
    def nearby(current_user_position=None):

        cordinat = request.args.get('data')
        geolocator = Nominatim(user_agent="jual_ikan")
        location = geolocator.reverse(cordinat)
        get_json_value = location.raw
        get_state_name = get_json_value['address']['state']

        # current_user_position = get_state_name
        current_user_position = 'Sumatera Selatan'

        urutan_ikan_dalam_tampilan_halamanerr = db.session.query(Ikan.id_ikan, Ikan.nama_ikan, Ikan.berat_ikan_dalam_Kg, Ikan.foto_ikan,
                                                                 Penjual).join(Penjual).filter(Penjual.domisili==current_user_position)

        return render_template("nearby_places.html", IKANS=urutan_ikan_dalam_tampilan_halamanerr, STATE=get_state_name)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = RegisterFormView()
        try:
            if form.validate_on_submit():
                hashed_password = form.password.data
                new_user = Penjual(nama_toko=form.nama_toko.data, email=form.email.data, nomor_telepon=form.nomor_telepon.data,
                                password=hashed_password, domisili=str(form.domisili.data))
                db.session.add(new_user)
                db.session.commit()

                return "<h1> Sukses mendaftar, Anda baru bisa login ketika akun sudah di aktivkan oleh " \
                       "admin. <br> kembali ke menu <a href=" + url_index + ">utama</a></h1>"
        except:
            return "<h2> Data yang di inputkan harus unique, sepertinya salah satu data yang Anda Masukan sudah terdaftar, " \
                   "Mohon ulangi input data dengan teliti...!!!  <br> <a href=" + url_index + "signup>Ulangi Input Data</a></h2>"

        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginFormView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                session['email'] = request.form['email']
                user = Penjual.query.filter_by(email=form.email.data).first()
                if verify_password(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
                else:
                    return '<h1>Invalid username or password</h1>'

        return render_template('login.html', form=form)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if 'email' in session:
            nama_toko = current_user.nama_toko
            all_user_data = Ikan.query.filter_by(user_id=current_user.id)
            return render_template('dashboard.html', ikan=all_user_data, NAMA_TOKO=nama_toko)
        else:
            return redirect(url_for('index'))

    @app.route('/user_profile')
    @login_required
    def user_profile():
        return render_template('user_profile.html')

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def tambah_ikan():
        form = AddIkanForm(request.form)
        if request.method == 'POST' and 'photo' in request.files:
            if form.validate_on_submit():
                filename = photos.save(request.files['photo'])
                new_ikan = Ikan(form.nama_ikan.data, form.keterangan_ikan.data, form.berat_ikan_dalam_Kg.data,
                                form.harga_per_Kg.data, form.minimal_order_dalam_Kg.data, form.ketersediaan.data,
                                current_user.id, False, filename)
                db.session.add(new_ikan)
                db.session.commit()
                return redirect(url_for('dashboard'))

        return render_template('tambah_ikan.html', form=form)

    @app.route('/ikan_delete/<ikan_id>')
    def ikan_delete(ikan_id):
        data = db.session.query(Ikan, Penjual).join(Penjual).filter(Ikan.id_ikan == ikan_id).first()
        if data.Ikan.is_public:
            return render_template('ikan_detail.html', ikan=data)
        else:
            try:
                if current_user.is_authenticated and data.Ikan.user_id == current_user.id:
                    data = Ikan.query.filter_by(id_ikan=ikan_id).first()
                    db.session.delete(data)
                    db.session.commit()
            except:
                return 'Tidak bisa delete data ikan, karena ikan sedang digunakan'
        return redirect(url_for('dashboard'))

    @app.route('/ikan_edit/<ikan_id>', methods=['GET', 'POST'])
    def ikan_edit(ikan_id):
        nama_toko = current_user.nama_toko
        data = db.session.query(Ikan, Penjual).join(Penjual).filter(Ikan.id_ikan == ikan_id).first()
        form = EditIkanForm(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                if current_user.is_authenticated and data.Ikan.user_id == current_user.id:
                    data = Ikan.query.filter_by(id_ikan=ikan_id).first()
                    new_nama_ikan = form.nama_ikan.data
                    new_keterangan_ikan = form.keterangan_ikan.data
                    new_berat_ikan_dalam_Kg = form.berat_ikan_dalam_Kg.data
                    new_harga_per_Kg = form.harga_per_Kg.data
                    new_minimal_order_dalam_Kg = form.minimal_order_dalam_Kg.data
                    new_stock = form.ketersediaan.data
                    try:
                        data.nama_ikan = new_nama_ikan
                        data.keterangan_ikan = new_keterangan_ikan
                        data.berat_ikan_dalam_Kg = new_berat_ikan_dalam_Kg
                        data.harga_per_Kg = new_harga_per_Kg
                        data.minimal_order_dalam_Kg = new_minimal_order_dalam_Kg
                        data.stock = new_stock

                        db.session.commit()

                    except Exception as e:
                        return {'error': str(e)}
                return redirect(url_for('dashboard'))

        return render_template('edit_ikan.html', form=form, ikan=data, NAMA_TOKO=nama_toko)


    @app.route('/ikan/<ikan_id>')
    def ikan_details(ikan_id):
        ikan_with_user = db.session.query(Ikan, Penjual).join(Penjual).filter(Ikan.id_ikan == ikan_id).first()
        if ikan_with_user is not None:
            if ikan_with_user.Ikan.is_public:
                return render_template('ikan_detail.html', ikan=ikan_with_user)
            else:
                if current_user.is_authenticated and ikan_with_user.Ikan.user_id == current_user.id:
                    return render_template('ikan_detail.html', ikan=ikan_with_user)
                # else:
                #    flash('Error! Incorrect permissions to access this mantan.', 'error')
        else:
            flash('Error! Recipe does not exist.', 'error')
        return redirect(url_for('index'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('ikan'))


    return app