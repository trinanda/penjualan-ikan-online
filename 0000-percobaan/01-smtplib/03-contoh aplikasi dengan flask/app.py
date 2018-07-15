from flask import Flask, render_template, request
from smtplib import SMTP

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        gmail_username = request.form['gmail_username']
        gmail_password = request.form['gmail_password']
        to = request.form['to']
        subject = request.form['subject']
        message = request.form['message']

        msg = """
        From %s\nTo: %s\nSubject: %s\n\n%s
        """ % (gmail_username, to, subject, message)

        try:
            server = SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_username, gmail_password)
            server.sendmail(gmail_username, to, msg)
            server.quit()
            return render_template('kirim_sukses.html', to=to)
        except:
            return render_template('kirim_gagal.html')

    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)









