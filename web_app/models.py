from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Enum, Numeric, Unicode, ForeignKey, DateTime

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
    kondisi_ikan = Column(Enum(FROZEN, FRESH, name='kondisi_ikan', default=FRESH))


    def __unicode__(self):
        return self.nama_ikan

    urutan_ikan_dalam_tampilan_halaman = Column(Integer)


class Pembeli(db.Model):
    __tablename__ = 'pembeli'
    nomor_pembeli = Column(Integer, primary_key=True, unique=True)
    nama_pembeli = Column(String)
    nomor_telepon = Column(Numeric)
    alamat_pembeli = Column(String)
    nama_ikan_yang_dipesan = Column(String)
    jumlah_pesanan = Column(String)
    harga_total_pesanan = Column(Integer)
    tanggal_pemesanan = Column(DateTime)

    ikan_id = Column(Integer, ForeignKey(Ikan.id_ikan), nullable=False)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

    status = db.Column(db.Enum(PENDING, CONFIRMED, REJECTED, name='status', default=PENDING))

    def __init__(self, id_ikan, nomor_pembeli, nomor_telepon, nama_pembeli, nama_ikan_yang_dipesan,
                 jumlah_pesanan, harga_total_pesanan, tanggal_pemesanan, status_pembayaran):
        self.ikan_id = id_ikan
        self.nomor_telepon = nomor_pembeli
        self.nama_pembeli = nama_pembeli
        self.nomor_telepon = nomor_telepon
        self.nama_ikan_yang_dipesan = nama_ikan_yang_dipesan
        self.jumlah_pesanan = jumlah_pesanan
        self.harga_total_pesanan = harga_total_pesanan
        self.tanggal_pemesanan = tanggal_pemesanan
        self.status_pembayaran = status_pembayaran


