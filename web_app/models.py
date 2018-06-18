from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Enum, Numeric

db = SQLAlchemy()


class Ikan():
    __tablename__ = 'ikan'
    id_ikan = Column(Integer, primary_key=True)
    nama_ikan = Column(String)
    ukuran = Column(Integer)
    minimal_order = Column(Integer)

    TERSEDIA = 'tersedia'
    STOCK_HABIS = 'stock habis'
    ketersediaan = Column(Enum(TERSEDIA, STOCK_HABIS, name='Ketersediaan', default=TERSEDIA))

    FROZEN = 'frozen'
    FRESH = 'segar'
    kondisi = Column(Enum(FROZEN, FRESH, name='kondisi ikan', default=FROZEN))


class Pembeli():
    __tablename__ = 'pembeli'
    nomor_pembeli = Column(Integer, primary_key=True, unique=True)
    nama_pembeli = Column(String)
    nomor_telepon = Column(Numeric)
    alamat_pembeli = Column(String)
