from flask import Flask, request, render_template, redirect, session
from firebase import firebase

app = Flask(__name__)
app.secret_key="2ko43n312kn"
fb=firebase.FirebaseApplication("https://fusionkitchen-bdb86.firebaseio.com/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        _=session['uname']
        return redirect('profile')
    except:
        pass
    if request.method == "POST":
        us=fb.get('/',request.form['uname'])
        if us['pwd']==request.form['pwd']:
            us.pop('pwd')
            for key in us.keys():
                session[key]=us[key]
            return redirect('profile')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        _=session['uname']
        return redirect('profile')
    except:
        pass
    if request.method == "POST":
        payl=request.form
        fb.put('/','%s'%(payl['uname']), data=payl)
    return render_template('signup.html')

@app.route('/profile')
def landing():
    try:
        _=session['uname']
    except:
        return redirect('/login')
    return render_template('user-profile.html', uname='%s %s'%(session['fname'], session['lname']), umail=session['email'])

@app.route('/')
def defaul():
    try:
        _=session['uname']
        return redirect('profile')
    except:
        pass
    return render_template('index.html')

@app.route('/logout')
def logou():
    try:
        _=session['uname']
    except:
        return redirect('/login')
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(host="0.0.0.0", port="80", debug=True)