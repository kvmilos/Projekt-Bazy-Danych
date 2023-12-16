from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database='kvmilos')
cur = conn.cursor()

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/login", methods=['POST'])
def login():
    index = request.form.get('index')
    password = request.form.get('password')
    is_komisja = request.form.get('komisja') is not None
    if is_komisja:
        index = '000000'

    cur.execute("SELECT * FROM Uzytkownicy WHERE indeks = %s AND haslo = %s", (index, password))
    result = cur.fetchone()
    if result is None:
        return render_template('login_failure.html')
    if is_komisja:
        return render_template('komisja.html')
    return render_template('wyborca.html')