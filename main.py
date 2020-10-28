#!/usr/bin/env python3

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
        us=fb.get('/user/',request.form['uname'])
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
        fb.put('/user/','%s'%(payl['uname']), data=payl)
        us=fb.get('/user/',payl['uname'])
        us.pop('pwd')
        for key in us.keys():
            session[key]=us[key]
        return redirect('/')
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
        return redirect('/profile')
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

@app.route('/gallery', methods=["POST", "GET"])
def gallery():
    try:
        _=session["uname"]
        return render_template("gallery.html")
    except:
        return redirect("/")

@app.route('/dish/<name>', methods=["POST", "GET"])
def dish(name):
    try:
        _=session["uname"]
    except:
        return redirect("/")
    if request.method=="POST":
        payl = dict(request.form)
        print(type(payl))
        payl["fname"]=session["fname"]
        payl["lname"]=session["lname"]
        payl["uname"]=session["uname"]
        fb.put('/review/%s/'%(name),'%s'%(payl['subject']), data=payl)
    rev=fb.get('/review/', name)
    reviews=list(rev.values())
    return render_template("dish.html", urname=name, reviews=reviews)

if __name__=="__main__":
    app.run(debug=True)