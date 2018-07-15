#pesan ini akan masuk ke dalam folder kotak masuk si penerima
from smtplib import SMTP_SSL

try:
    server = SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('zidanecr7kaka@gmail.com', 'm@Fu7Ur3#')
    server.sendmail('zidanecr7kaka@gmail.com', 'sampah_rakyat3@yahoo.com', 'Hello zidanecr7kaka, i am here')
    server.quit()
    print('Email sukses terkirim')
except:
    print('Email gagal dikirim')