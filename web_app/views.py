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
    if target.room_images:
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
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    # column_list = ('nama_kamar', 'room_images', 'harga_kamar', 'kamar_tersedia')
    def _list_thumbnail(view, context, model, name):
        if not model.room_images:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.room_images)))

    column_formatters = {
        'room_images': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'room_images': form.ImageUploadField('Foto Ikan',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }