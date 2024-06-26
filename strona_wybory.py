from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
from datetime import date

app = Flask(__name__)
app.secret_key = 'projekt123'

conn = psycopg2.connect(database='kvmilos')
cur = conn.cursor()

data = date.today()

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
            index = '000000'

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
    if not session.get('logged') or session.get('index') == '000000':
        return redirect(url_for('login'))
    index = session.get('index')
    return render_template('wyborca.html')

@app.route("/zglaszanie", methods = ['GET', 'POST'])
def zglaszanie():
    if not session.get('logged') or session.get('index') == '000000':
        return redirect(url_for('login'))
    cur.execute("SELECT * FROM Wybory WHERE termin_zglaszania >= %s", (data,))
    wybory = cur.fetchall()
    if request.method == 'POST':
        indeks_kandydata = request.form['index']
        id_wyborow = request.form['wybory']
        cur.execute("SELECT * FROM Uzytkownicy WHERE indeks = %s", (indeks_kandydata,))
        if cur.fetchone() is None:
            return render_template("wyborca_blad.html")
        else:
            cur.execute("INSERT INTO Kandydaci VALUES (%s, %s)", (indeks_kandydata, id_wyborow))
            conn.commit()
            return render_template('wyborca2.html')
    return render_template('zglaszanie.html', wybory=wybory)

@app.route("/glosowanie", methods = ['GET', 'POST'])
def glosowanie():
    if not session.get('logged') or session.get('index') == '000000':
        return redirect(url_for('login'))
    index = session.get('index')
    cur.execute("SELECT * FROM Wybory WHERE termin_rozpoczecia <= %s AND termin_zakonczenia >= %s", (data, data))
    wybory = cur.fetchall()
    if request.method == 'GET':
        return render_template('glosowanie.html', wybory=wybory)
    if request.method == 'POST':
        id_wyb = request.form['wybory']
        cur.execute("SELECT * FROM Wybory WHERE id = %s", (id_wyb))
        wybory = cur.fetchall()
        cur.execute("SELECT czy_glosowal FROM Glosowanie WHERE indeks = %s AND id_wybory = %s", (index, id_wyb))
        result = cur.fetchone()
        if result is not None and result[0] == True:
            return render_template("wyborca_blad.html")
        cur.execute("SELECT * FROM Kandydaci NATURAL JOIN Uzytkownicy WHERE id_wybory = %s", (id_wyb))
        kandydaci = cur.fetchall()
        session['wybory'] = wybory
        session['kandydaci'] = kandydaci
        return redirect(url_for('glosowanie2'))
    
@app.route("/glosowanie2", methods = ['GET', 'POST'])
def glosowanie2():
    if not session.get('logged') or session.get('index') == '000000':
        return redirect(url_for('login'))
    wybory = session.get('wybory')
    kandydaci = session.get('kandydaci')
    index = session.get('index')
    if request.method == 'GET':
        return render_template('glosowanie2.html', wybory=wybory, kandydaci=kandydaci)
    if request.method == 'POST':
        voted = request.form.getlist('kandydaci')
        for kandydat in voted:
            cur.execute("UPDATE Kandydaci SET glosy = glosy + 1 WHERE indeks = %s AND id_wybory = %s", (kandydat, wybory[0][0]))
            cur.execute("INSERT INTO Glosowanie VALUES (%s, %s, 't')", (index, wybory[0][0]))
        conn.commit()
        return render_template('wyborca2.html')
    
@app.route("/ogladanie_wynikow", methods = ['GET', 'POST'])
def ogladanie_wynikow():
    if not session.get('logged') or session.get('index') == '000000':
        return redirect(url_for('login'))
    cur.execute("SELECT * FROM Wybory WHERE czy_opublikowane = 't'")
    wybory = cur.fetchall()
    if request.method == 'GET':
        return render_template('ogladanie_wynikow.html', wybory=wybory)
    if request.method == 'POST':
        id_wyb = request.form['wybory']
        cur.execute("SELECT * FROM Kandydaci NATURAL JOIN Uzytkownicy WHERE id_wybory = %s ORDER BY glosy DESC", (id_wyb))
        kandydaci = cur.fetchall()
        # change the order: glosy will be kandydaci[0, 5, 6, 2]
        glosy = []
        for kandydat in kandydaci:
            glosy.append([kandydat[0], kandydat[5], kandydat[6], kandydat[2]])
        print(glosy)
        return render_template('ogladanie2.html', wybory=wybory, glosy = glosy)

@app.route("/komisja")
def komisja():
    if not session.get('logged') or session.get('index') != '000000':
        return redirect(url_for('login'))
    return render_template('komisja.html')

@app.route("/rej_wyborcy", methods = ['GET', 'POST'])
def rej_wyborcy():
    if not session.get('logged') or session.get('index') != '000000':
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('rej_wyborcy.html')
    else:
        indeks = request.form['index']
        haslo = request.form['haslo']
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        cur.execute("INSERT INTO Uzytkownicy VALUES (%s, %s, 'f', %s, %s)", (indeks, haslo, imie, nazwisko))
        conn.commit()
        return render_template('komisja2.html')

@app.route("/rej_wyborow", methods = ['GET', 'POST'])
def rej_wyborow():
    if not session.get('logged') or session.get('index') != '000000':
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('rej_wyborow.html')
    else:
        nazwa = request.form['nazwa']
        liczba_posad = request.form['liczba_posad']
        data_zgloszen = request.form['data_zgloszen']
        start_glosowania = request.form['start_glosowania']
        koniec_glosowania = request.form['koniec_glosowania']
        cur.execute("INSERT INTO Wybory (nazwa, liczba_posad, termin_zglaszania, termin_rozpoczecia, termin_zakonczenia) VALUES (%s, %s, %s, %s, %s)", (nazwa, liczba_posad, data_zgloszen, start_glosowania, koniec_glosowania))
        conn.commit()
        return render_template('komisja2.html')

@app.route("/publikacja", methods = ['GET', 'POST'])
def publikacja():
    if not session.get('logged') or session.get('index') != '000000':
        return redirect(url_for('login'))
    if request.method == 'GET':
        wybory = cur.execute("SELECT * FROM wybory WHERE czy_opublikowane = 'f' AND termin_zakonczenia >= %s", (data,))
        wybory = cur.fetchall()
        return render_template('publikacja.html', wybory=wybory)
    else:
        id_wyb = request.form['wybory']
        cur.execute("SELECT * FROM Wybory WHERE id = %s", (id_wyb))
        wybory = cur.fetchall()
        cur.execute("UPDATE Wybory SET czy_opublikowane = 't' WHERE id = %s", (id_wyb))
        conn.commit()
        return render_template('komisja2.html')