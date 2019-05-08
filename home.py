from flask import Flask, render_template, redirect, url_for, request, session, flash, g
import re
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = "my secret"
app.database = "apidatabase.db"

con = sqlite3.connect("apidatabase.db")
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please enter your name..')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from visiters')
    visiters = [dict(name=row[0], surname=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("index.html", visiters=visiters)

@app.route('/welcome')
def welcome():
    return  render_template("welcome.html")

@app.route('/login',methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
       # if request.form["name"].re.search('[0-9]') is None and request.form["surname"].re.search('[0-9]') is None:
        #   error = "Please check your name/surname"
       # else:
            session['logged_in'] = True
            name = request.form["name"]
            surname = request.form["surname"]
            with sqlite3.connect("apidatabase.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO visiters(name, surname) VALUES(?,?)", (name, surname))
                con.commit()
                flash("Welcome visiter!")
            return redirect(url_for('home'))
            con.close()
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("You leave this page..")
    return redirect(url_for('welcome'))

def connect_db():
    return sqlite3.connect(app.database)

if __name__ == '__main__':
    app.run(debug=True)