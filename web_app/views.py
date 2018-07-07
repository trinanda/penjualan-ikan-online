import os
import os.path as op

from flask_admin.contrib.sqla import ModelView

from web_app.models import Ikan
from flask_admin import Admin, form
from sqlalchemy.event import listens_for
from flask_admin.contrib import sqla
from jinja2 import Markup
from flask import url_for
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class ViewPembeli(ModelView):
    column_list = ('ikan_id', 'kode_pembeli', 'nomor_telepon', 'nama_pembeli', 'alamat_pembeli',
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
class ViewIkan(ModelView):
    form_overrides = dict(keterangan_kamar=CKEditorField)
    column_list = ('id_ikan', 'nama_ikan', 'keterangan_ikan', 'berat_ikan_dalam_Kg', 'minimal_order_dalam_Kg',
                   'harga_per_Kg', 'foto_ikan')
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    # column_list = ('nama_kamar', 'foto_ikan', 'harga_kamar', 'kamar_tersedia')
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