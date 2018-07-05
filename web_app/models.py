from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Enum, Numeric, Unicode, ForeignKey

db = SQLAlchemy()


class Ikan(db.Model):
    __tablename__ = 'ikan'
    id_ikan = Column(Integer, primary_key=True)
    nama_ikan = Column(String)
    keterangan_ikan = Column(String)
    berat_ikan_dalam_Kg = Column(Integer)
    minimal_order_dalam_Kg = Column(Integer)
    harga_per_Kg = Column(Integer)
    foto_ikan = Column(Unicode(128))


    TERSEDIA = 'tersedia'
    STOCK_HABIS = 'stock habis'
    ketersediaan = Column(Enum(TERSEDIA, STOCK_HABIS, name='Ketersediaan', default=TERSEDIA))

    FROZEN = 'frozen'
    FRESH = 'segar'
    kondisi = Column(Enum(FROZEN, FRESH, name='kondisi ikan', default=FROZEN))


    def __unicode__(self):
        return self.nama_ikan

    urutan_ikan_dalam_tampilan_halaman = Column(Integer)


class Pembeli(db.Model):
    __tablename__ = 'pembeli'
    nomor_pembeli = Column(Integer, primary_key=True, unique=True)
    nama_pembeli = Column(String)
    nomor_telepon = Column(Numeric)
    alamat_pembeli = Column(String)

    ikan_id = Column(Integer, ForeignKey(Ikan.id_ikan), nullable=False)
