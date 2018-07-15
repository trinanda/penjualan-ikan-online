#pesan ini akan masuk ke dalam folder spam si penerima
from smtplib import SMTP

try:
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('zidanecr7kaka@gmail.com', 'm@Fu7Ur3#')
    server.sendmail('zidanecr7kaka@gmail.com', 'sampah_rakyat3@yahoo.com', ' Hello yahoo, can you see me..?, i am here')
    server.quit()
    print('Email sukses terkirim')
except:
    print('Email gagal terkirim')