from wtforms import TextAreaField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired, Required
from flask_wtf import FlaskForm

from web_app.models import Domisili


def pilih_domisili():
    return Domisili.query

class RegisterFormView(FlaskForm):
    nama_toko = StringField('Nama Toko Anda', validators=[DataRequired()], render_kw={"placeholder": "Nama Toko"})
    email = StringField('email', validators=[InputRequired(),
                                             Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()], render_kw={"placeholder": "Nomor Telepon"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})

    domisili = QuerySelectField('Domisili',
                                validators=[Required()],
                                query_factory=pilih_domisili)


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