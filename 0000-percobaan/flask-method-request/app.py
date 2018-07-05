from flask import Flask, render_template, request

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'get':
      nama = request.form['nama']
      email = request.form['email']
      komentar = request.form['komentar']
      return render_template('response.html',
         nama=nama, email=email, komentar=komentar)
   return render_template('form.html')

if __name__ == '__main__':
   application.run(debug=True)