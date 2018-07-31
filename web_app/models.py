from flask_security import RoleMixin, UserMixin
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


    def __repr__(self):
        return '{}'.format(self.nama_ikan)

    urutan_ikan_dalam_tampilan_halaman = Column(Integer)


class Pembeli(db.Model):
    __tablename__ = 'pembeli'
    kode_pembeli = Column(String, primary_key=True, unique=True)
    nama_pembeli = Column(String)
    nomor_telepon = Column(String)
    alamat_pembeli = Column(String)
    nama_ikan_yang_dipesan = Column(String)
    jumlah_pesanan = Column(String)
    harga_total_pesanan = Column(Integer)
    tanggal_pemesanan = Column(DateTime)

    ikan_id = Column(Integer, ForeignKey(Ikan.id_ikan), nullable=False)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

    status_pembayaran = db.Column(db.Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    def __init__(self, id_ikan, kode_pembeli, nama_pemesan, no_hp_or_wa, alamat_lengkap, nama_ikan,
                 pesan_berapa_kg, harga_total_pesanan, tanggal_pemesanan, status):
        self.ikan_id = id_ikan
        self.kode_pembeli = kode_pembeli
        self.nomor_telepon = no_hp_or_wa
        self.nama_pembeli = nama_pemesan
        self.alamat_pembeli = alamat_lengkap
        self.nama_ikan_yang_dipesan = nama_ikan
        self.jumlah_pesanan = pesan_berapa_kg + ' Kg'
        self.harga_total_pesanan = harga_total_pesanan
        self.tanggal_pemesanan = tanggal_pemesanan
        self.status_pembayaran = status



roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama_toko = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    lokasi = Column(String)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

