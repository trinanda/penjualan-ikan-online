import os
import os.path as op

from flask_admin.contrib.sqla import ModelView

from web_app.models import Ikan
from flask_admin import Admin, form
from sqlalchemy.event import listens_for
from flask_admin.contrib import sqla
from jinja2 import Markup
from flask import url_for, abort, redirect, request
from wtforms import TextAreaField, IntegerField, SelectField
from wtforms.widgets import TextArea

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_wtf import FlaskForm



class UserAkses(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('user'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminAkses(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))





class ViewPembeli(AdminAkses):
    column_list = ('kode_pembeli', 'nama_pembeli', 'nomor_telepon', 'alamat_pembeli',
                   'nama_ikan_yang_dipesan', 'jumlah_pesanan', 'harga_total_pesanan', 'tanggal_pemesanan', 'status_pembayaran')
    pass


# cekdeitor
class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)

class CKEditorField(TextAreaField):
    widget = CKEditorWidget()

# cekdeitor


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


# Delete hooks for models, delete files if models are getting deleted
@listens_for(Ikan, 'after_delete')
def del_image(mapper, connection, target):
    if target.foto_ikan:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass


# Administrative views
class ViewIkan(UserAkses):
    form_overrides = dict(keterangan_ikan=CKEditorField)
    column_list = ('id_ikan', 'nama_ikan', 'keterangan_ikan', 'berat_ikan_dalam_Kg', 'minimal_order_dalam_Kg',
                   'harga_per_Kg', 'foto_ikan')
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    def _list_thumbnail(view, context, model, name):
        if not model.foto_ikan:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.foto_ikan)))

    column_formatters = {
        'foto_ikan': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'foto_ikan': form.ImageUploadField('Foto Ikan',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }



# Create customized model view class
class MyModelView(AdminAkses):
    pass


DOMISILI = ['Aceh','Bali','Banten','Bengkulu','Gorontalo','Jakarta','Jambi','Jawa Barat','Jawa Tengah','Jawa Timur',
            'Kalimantan Barat','Kalimantan Selatan','Kalimatan Tengah','Kalimantan Timur','Kalimantan Utara',
            'Kepulauan Bangka Belitung','Kepulauan Riau','Lampung','Maluku','Maluku Utara','Nusa Tenggara Barat',
            'Nusa Tenggara Timur','Papua','Papua Barat','Riau','Sulawesi Barat','Sulawesi Selatan','Sulawesi Tengah',
            'Sulawesi Tenggara','Sulawesi Utara','Sumatera Barat','Sumatera Selatan','Sumatera Utara','Yogyakarta']


class RegisterFormView(FlaskForm):
    nama_toko = StringField('Nama Toko Anda', validators=[DataRequired()], render_kw={"placeholder": "Nama Toko"})
    email = StringField('email', validators=[InputRequired(),
                                             Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()], render_kw={"placeholder": "Nomor Telepon"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})
    # domisili = StringField('Domisili', validators=[DataRequired()],
    #                                render_kw={"placeholder": "Domisili penjualan"})

    domisili = SelectField('Domisili', validators=[DataRequired()], choices=[(DOMISILI[0],DOMISILI[0]),(DOMISILI[1],DOMISILI[1]),(DOMISILI[2],DOMISILI[2]),
                                                                             (DOMISILI[3], DOMISILI[3]),(DOMISILI[4],DOMISILI[4]),(DOMISILI[5],DOMISILI[5]),
                                                                             (DOMISILI[6], DOMISILI[6]),(DOMISILI[7],DOMISILI[7]),(DOMISILI[8],DOMISILI[8]),
                                                                             (DOMISILI[9], DOMISILI[9]),(DOMISILI[10],DOMISILI[10]),(DOMISILI[11],DOMISILI[11]),
                                                                             (DOMISILI[12], DOMISILI[12]),(DOMISILI[13],DOMISILI[13]),(DOMISILI[14],DOMISILI[14]),
                                                                             (DOMISILI[15], DOMISILI[15]),(DOMISILI[16],DOMISILI[16]),(DOMISILI[17],DOMISILI[17]),
                                                                             (DOMISILI[18], DOMISILI[18]),(DOMISILI[19],DOMISILI[19]),(DOMISILI[20],DOMISILI[20]),
                                                                             (DOMISILI[21], DOMISILI[21]),(DOMISILI[22], DOMISILI[22]),(DOMISILI[23], DOMISILI[23]),
                                                                             (DOMISILI[24], DOMISILI[24]),(DOMISILI[25], DOMISILI[25]),(DOMISILI[26], DOMISILI[26]),
                                                                             (DOMISILI[27], DOMISILI[27]),(DOMISILI[28], DOMISILI[28]),(DOMISILI[29], DOMISILI[29]),
                                                                             (DOMISILI[30], DOMISILI[30]),(DOMISILI[31], DOMISILI[31]),(DOMISILI[32], DOMISILI[32]),
                                                                             (DOMISILI[33], DOMISILI[33])])

class LoginFormView(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')


TERSEDIA = 'tersedia'
STOCK_HABIS = 'stock habis'

FROZEN = 'frozen'
FRESH = 'segar'

class AddIkanForm(FlaskForm):
    nama_ikan = StringField('Nama Ikan', validators=[DataRequired()])
    keterangan_ikan = StringField('Keterangan Ikan', validators=[DataRequired()])
    berat_ikan_dalam_Kg = StringField('Nama Ikan', validators=[DataRequired()])
    harga_per_Kg = IntegerField('Harga Ikan', validators=[DataRequired()])
    minimal_order_dalam_Kg = StringField('Minimal Order', validators=[DataRequired()])
    ketersediaan = SelectField('status_ikan',choices=[(TERSEDIA, TERSEDIA), (STOCK_HABIS, STOCK_HABIS)])
    kondisi_ikan = SelectField('status_ikan',choices=[(FROZEN, FROZEN), (FRESH, FRESH)])


class EditIkanForm(FlaskForm):
    nama_ikan = StringField('Nama Ikan', validators=[DataRequired()])
    keterangan_ikan = StringField('Keterangan Ikan', validators=[DataRequired()])
    berat_ikan_dalam_Kg = StringField('Nama Ikan', validators=[DataRequired()])
    harga_per_Kg = IntegerField('Harga Ikan', validators=[DataRequired()])
    minimal_order_dalam_Kg = StringField('Minimal Order', validators=[DataRequired()])
    ketersediaan = SelectField('status_ikan',choices=[(TERSEDIA, TERSEDIA), (STOCK_HABIS, STOCK_HABIS)])
    kondisi_ikan = SelectField('status_ikan',choices=[(FROZEN, FROZEN), (FRESH, FRESH)])