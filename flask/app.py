from flask import Flask
 
app = Flask(__name__)
 
 
@app.route('/', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    ip = user_ip()
    host = socket.gethostname() 
    
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == '19970902':
            session['logged_in'] = True
            return redirect('/status')
        else:
            session['logged_in'] = False

    return render_template('auth.html', ip=ip, host=host)

 
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0')