from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = "my secret"
app.database = "apidatabase.db"

con = sqlite3.connect(app.database)

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

    g.db = sqlite3.connect(app.database)
    cur = g.db.execute('SELECT *FROM visiters WHERE name IS NOT NULL AND surname IS NOT NULL')
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
    else:
        page_not_found()
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("You leave this page..")
    return redirect(url_for('welcome'))

@app.errorhandler(404)
def page_not_found():
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)