from wtforms import TextAreaField, IntegerField, SelectField
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired, Required
from flask_wtf import FlaskForm
from wtforms_alchemy import QuerySelectField

from web_app.models import Domisili, db


# DOMISILI = ['Aceh','Bali','Banten','Bengkulu','Gorontalo','Jakarta','Jambi','Jawa Barat','Jawa Tengah','Jawa Timur',
#             'Kalimantan Barat','Kalimantan Selatan','Kalimatan Tengah','Kalimantan Timur','Kalimantan Utara',
#             'Kepulauan Bangka Belitung','Kepulauan Riau','Lampung','Maluku','Maluku Utara','Nusa Tenggara Barat',
#             'Nusa Tenggara Timur','Papua','Papua Barat','Riau','Sulawesi Barat','Sulawesi Selatan','Sulawesi Tengah',
#             'Sulawesi Tenggara','Sulawesi Utara','Sumatera Barat','Sumatera Selatan','Sumatera Utara','Yogyakarta']



def pilih_domisili():
    return Domisili.query


def get_pk(obj):
    return str(obj)

class RegisterFormView(FlaskForm):
    nama_toko = StringField('Nama Toko Anda', validators=[DataRequired()], render_kw={"placeholder": "Nama Toko"})
    email = StringField('email', validators=[InputRequired(),
                                             Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()], render_kw={"placeholder": "Nomor Telepon"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})

    domisili = QuerySelectField(u'Domicile', query_factory=pilih_domisili, get_pk=get_pk)

    # domisili = QuerySelectField('Domisili',
    #                             validators=[Required()],
    #                             query_factory=pilih_domisili)

    # domisili = SelectField('Domisili', validators=[DataRequired()],
    #                        choices=[(DOMISILI[0], DOMISILI[0]), (DOMISILI[1], DOMISILI[1]), (DOMISILI[2], DOMISILI[2]),                                                                             (
    #                                 DOMISILI[3], DOMISILI[3]), (DOMISILI[4], DOMISILI[4]), (DOMISILI[5], DOMISILI[5]),                                                                             (
    #                                 DOMISILI[6], DOMISILI[6]), (DOMISILI[7], DOMISILI[7]), (DOMISILI[8], DOMISILI[8]),                                                                             (
    #                                 DOMISILI[9], DOMISILI[9]), (DOMISILI[10], DOMISILI[10]),(DOMISILI[11], DOMISILI[11]),                                                                             (
    #                                 DOMISILI[12], DOMISILI[12]), (DOMISILI[13], DOMISILI[13]),(DOMISILI[14], DOMISILI[14]),                                                                             (
    #                                 DOMISILI[15], DOMISILI[15]), (DOMISILI[16], DOMISILI[16]),(DOMISILI[17], DOMISILI[17]),                                                                             (
    #                                 DOMISILI[18], DOMISILI[18]), (DOMISILI[19], DOMISILI[19]),(DOMISILI[20], DOMISILI[20]),                                                                             (
    #                                 DOMISILI[21], DOMISILI[21]), (DOMISILI[22], DOMISILI[22]),(DOMISILI[23], DOMISILI[23]),                                                                             (
    #                                 DOMISILI[24], DOMISILI[24]), (DOMISILI[25], DOMISILI[25]),(DOMISILI[26], DOMISILI[26]),                                                                             (
    #                                 DOMISILI[27], DOMISILI[27]), (DOMISILI[28], DOMISILI[28]),(DOMISILI[29], DOMISILI[29]),                                                                             (
    #                                 DOMISILI[30], DOMISILI[30]), (DOMISILI[31], DOMISILI[31]),(DOMISILI[32], DOMISILI[32]),                                                                             (
    #                                 DOMISILI[33], DOMISILI[33])])

    # domisili = SelectField('Domisili', validators=[DataRequired],
    #                        choices=pilih_domisili())

class LoginFormView(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')


TERSEDIA = 'tersedia'
STOCK_HABIS = 'stock habis'


class AddIkanForm(FlaskForm):
    nama_ikan = StringField('Nama Ikan', validators=[DataRequired()])
    keterangan_ikan = StringField('Keterangan Ikan', validators=[DataRequired()])
    berat_ikan_dalam_Kg = StringField('Nama Ikan', validators=[DataRequired()])
    harga_per_Kg = IntegerField('Harga Ikan', validators=[DataRequired()])
    minimal_order_dalam_Kg = StringField('Minimal Order', validators=[DataRequired()])
    ketersediaan = SelectField('status_ikan',choices=[(TERSEDIA, TERSEDIA), (STOCK_HABIS, STOCK_HABIS)])


class EditIkanForm(FlaskForm):
    nama_ikan = StringField('Nama Ikan', validators=[DataRequired()])
    keterangan_ikan = StringField('Keterangan Ikan', validators=[DataRequired()])
    berat_ikan_dalam_Kg = StringField('Nama Ikan', validators=[DataRequired()])
    harga_per_Kg = IntegerField('Harga Ikan', validators=[DataRequired()])
    minimal_order_dalam_Kg = StringField('Minimal Order', validators=[DataRequired()])
    ketersediaan = SelectField('status_ikan',choices=[(TERSEDIA, TERSEDIA), (STOCK_HABIS, STOCK_HABIS)])