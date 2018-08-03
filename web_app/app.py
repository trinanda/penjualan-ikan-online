import sys, os
import flask_admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password, login_user, logout_user
from werkzeug.utils import redirect

sys.path.append(os.getcwd() + '/web_app')
from flask_admin import Admin, helpers as admin_helpers
from flask import Flask, render_template, request, session, url_for, flash
from models import db, Ikan, Pembeli, Penjual, Role
from views import ViewIkan, ViewPembeli, MyModelView, RegisterFormView, LoginFormView, AddIkanForm, EditIkanForm


def buat_app():

    app = Flask(__name__, static_folder='files')

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    bootstrap = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

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

        # current_user_position = 'Sumatera Selatan'

        # try:
        #     result, lokasi = db.session.query(Ikan, User).join(User).filter(User.domisili == current_user_position).first()
        # except:
        #     pass
        #
        # print('ggg', lokasi)

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
    def nearby(current_user_position=None):

        # urutan_ikan_dalam_tampilan_halaman = Ikan.query.order_by('urutan_ikan_dalam_tampilan_halaman')

        current_user_position = 'Sumatera Selatan'

        # try:
        #     result, nearby_fish = db.session.query(Ikan, User).join(User).filter(User.domisili == current_user_position).first()
        # except:
        #     nearby_fish = 'Data Not Valid'

        urutan_ikan_dalam_tampilan_halamanerr = db.session.query(Ikan.id_ikan, Ikan.nama_ikan, Ikan.berat_ikan_dalam_Kg, Ikan.foto_ikan,
                                                                 Penjual).join(Penjual).filter(Penjual.domisili==current_user_position)
        print('xxx', urutan_ikan_dalam_tampilan_halamanerr)
        # urutan_ikan_dalam_tampilan_halamanerr = Ikan.query.filter_by(user_id=3)

        return render_template("nearby_places.html", IKANS=urutan_ikan_dalam_tampilan_halamanerr)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = RegisterFormView()

        try:
            if form.validate_on_submit():
                hashed_password = form.password.data
                new_user = Penjual(nama_toko=form.nama_toko.data, email=form.email.data, nomor_telepon=form.nomor_telepon.data,
                                password=hashed_password, domisili=form.domisili.data)
                db.session.add(new_user)
                db.session.commit()

                return "<h1>User telah berhasil dibuat, silahkan coba untuk login \
                           <a href='http://127.0.0.1:9999/login'>Login</a></h1>"
                # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        except:
            return """<html><h2> Data yang di inputkan harus unique, sepertinya salah satu data yang Anda \
                        Masukan sudah terdaftar, Mohon ulangi input data dengan teliti...!!!  <br>
                       <a href='http://127.0.0.1:9999/signup'>Ulangi Input Data</a></h2></html>"""

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
        if request.method == 'POST':
            if form.validate_on_submit():
                new_ikan = Ikan(form.nama_ikan.data, form.keterangan_ikan.data, form.berat_ikan_dalam_Kg.data,
                                form.harga_per_Kg.data, form.minimal_order_dalam_Kg.data, form.ketersediaan.data,
                                current_user.id, False)
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