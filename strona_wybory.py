from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'projekt123'

conn = psycopg2.connect(database='kvmilos')
cur = conn.cursor()

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        index = request.form.get('index')
        password = request.form.get('password')
        is_komisja = request.form.get('komisja') is not None
        if is_komisja:
            index = '0'

        cur.execute("SELECT * FROM Uzytkownicy WHERE indeks = %s AND haslo = %s", (index, password))
        result = cur.fetchone()
        if result is None:
            return render_template('login_failure.html')
        
        session['logged'] = True
        session['index'] = index

        if is_komisja:
            return redirect(url_for('komisja'))
        return redirect(url_for('wyborca'))
    else:
        return render_template('homepage.html')

@app.route("/wyborca")
def wyborca():
    if not session.get('logged') or session.get('index') == '0':
        return redirect(url_for('login'))
    index = session.get('index')
    return render_template('wyborca.html')

@app.route("/zglaszanie")
def zglaszanie():
    return render_template('zglaszanie.html')

@app.route("/glosowanie")
def glosowanie():
    return render_template('glosowanie.html')

@app.route("/ogladanie_wynikow")
def ogladanie_wynikow():
    return render_template('ogladanie_wynikow.html')

@app.route("/komisja")
def komisja():
    if not session.get('logged') or session.get('index') != '0':
        return redirect(url_for('login'))
    return render_template('komisja.html')