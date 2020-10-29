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
        ingred=fb.get('/','ingredients')
        return render_template("kitchen.html", sec=ingred.keys(), ingred=ingred)
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

@app.route('/search', methods=['GET', 'POST'])
def searc():
    try:
        _=session["uname"]
    except:
        return redirect("/")
    if request.method=="POST":
        recip = fb.get('/', 'Dish')
        a_ingred=list()
        for i in recip.values():
            a_ingred.append(" ".join(i["ingredients"][1:]).upper())
        f_dish=list()
        s = request.form["tb1"].split(", ")+request.form["tb2"].split(", ")
        s=[i for i in s if len(i)!=0]
        for i in range(len(a_ingred)):
            for j in s:
                if a_ingred[i].find(j)!=-1:
                    f_dish.append(list(recip.keys())[i])
        return render_template("ingredsearch.html", recipk=f_dish, recip=recip)
    return redirect("/")

@app.route('/gallery', methods=["POST", "GET"])
def gallery():
    try:
        _=session["uname"]
    except:
        return redirect("/")
    recip = fb.get('/', 'Dish')
    return render_template("gallery.html", recip=recip, recipk=recip.keys())

@app.route('/dish/<name>', methods=["POST", "GET"])
def dish(name):
    try:
        _=session["uname"]
    except:
        return redirect("/")
    if request.method=="POST":
        payl = dict(request.form)
        payl["fname"]=session["fname"]
        payl["lname"]=session["lname"]
        payl["uname"]=session["uname"]
        fb.put('/review/%s/'%(name),'%s'%(payl['subject']), data=payl)
    rev=fb.get('/review/', name)
    try:    
        reviews=list(rev.values())
    except:
        reviews=list()
    recip = fb.get('/Dish/', name)
    if recip==None:
        return redirect('/gallery')
    return render_template("dish.html", urname=name, reviews=reviews, recip=recip)

@app.route('/save/<name>')
def saver(name):
    try:
        _=session["uname"]
    except:
        return redirect("/")
    us=fb.get('/user/%s'%session['uname'], 'saved')
    if us==None:
        us=list()
    if name not in us:
        us.append(name)
    fb.put('/user/%s'%(session['uname']),'saved', us)
    return redirect('/saved')

@app.route('/saved')
def savedrecipes():
    try:
        us=fb.get('/user/%s'%session['uname'], 'saved')
    except:
        return redirect('/')
    recip = fb.get('/', 'Dish')
    return render_template("gallery.html", recip=recip, recipk=us)
    

if __name__=="__main__":
    app.run(debug=True)