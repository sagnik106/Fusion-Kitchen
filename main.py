from flask import Flask, request, render_template, redirect, session
from firebase import firebase

app = Flask(__name__)
app.secret_key="2ko43n312kn"
fb=firebase.FirebaseApplication("https://fusionkitchen-bdb86.firebaseio.com/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        us=fb.get('/',request.form['uname'])
        if us['pwd']==request.form['pwd']:
            us.pop('pwd')
            for key in us.keys():
                session[key]=us[key]
            return redirect('landing')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        payl=request.form
        fb.put('/','%s'%(payl['uname']), data=payl)
    return render_template('signup.html')

@app.route('/landing')
def landing():
    try:
        _=session['uname']
    except:
        return redirect('/')
    return render_template('landing.html', msg='%s %s'%(session['fname'], session['lname']))

@app.route('/')
def defaul():
    return redirect('/login')

if __name__=="__main__":
    app.run(host="0.0.0.0", port="5464", debug=True)