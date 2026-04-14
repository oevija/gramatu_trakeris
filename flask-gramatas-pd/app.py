from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'kaza1'

@app.before_request
def gatekeeper():
    publiskie_celi = ['sakums', 'pieteikties', 'registreties', 'static']

    if 'id' not in session and request.endpoint not in publiskie_celi:
        return redirect("/pieteikties")

@app.route("/")
def sakums():
    return render_template("sakums.html")

@app.route("/pieteikties", methods=['GET', 'POST'])
def pieteikties():
    if request.method == 'POST':
        lietotajs = request.form.get('lietotajs')
        parole = request.form.get('parole')

        conn = sqlite3.connect("biblioteka.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM lietotaji WHERE lietotajvards = ?", (lietotajs,))
        atbilde = c.fetchone()
        conn.close()

        if atbilde and check_password_hash(atbilde['parole'], parole):
            session['id'] = atbilde['id']
            session['lietotajs'] = atbilde['lietotajvards']
            session['vards'] = atbilde['vards']
            session['tema'] = "dark"
            return redirect("/")
        else:
            return 'Nepareizi dati!'

    return render_template("pieteikties.html")

@app.route("/registreties", methods=['GET', 'POST'])
def registreties():
    if request.method == 'POST':
        lietotajvards = request.form.get("lietotajs")
        vards = request.form.get("vards")
        parole_txt = request.form.get("parole")
        parole = generate_password_hash(parole_txt)
        conn = sqlite3.connect("biblioteka.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        insert_sql = """
                    INSERT INTO lietotaji (lietotajvards, vards, parole)
                    VALUES (?, ?, ?)
                    """
        insert_dati = (lietotajvards, vards, parole)
        c.execute(insert_sql, insert_dati)
        conn.commit()
        return redirect("/pieteikties")

    return render_template("registreties.html")
    
@app.route("/pievienot", methods=['GET', 'POST'])
def pievienot():
    if request.method == 'POST':
        conn = sqlite3.connect("biblioteka.db")
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()

        nosaukums= request.form.get("nosaukums")
        autors = request.form.get("autors")
        lpp= int(request.form.get("lpp"))
        saku = request.form.get("saku")
        beidzu = request.form.get("beidzu")
        vertejums= int(request.form.get("vertejums"))

        insert = """INSERT OR IGNORE INTO gramatas(nosaukums,autors,lapas,saku_lasit,izlasits,vertejums) 
                VALUES(?,?,?,?,?,?)
            """
        cursor.execute(insert, (nosaukums, autors,lpp,saku,beidzu,vertejums))
        conn.commit()
        conn.close()
        return redirect(url_for('sakums'))
    else:
        return render_template("pievienot.html",vards =session['vards'])


@app.route("/visas_gramatas")
def visas_gramatas():
   ''' 
    conn = sqlite3.connect("biblioteka.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    klienta_id = session['id']
    sql_vaicajums = """ SELECT * FROM gramatas 
    """
        cur.execute(sql_vaicajums,)
    '''
    #return render_template("visas_gramatas.html")
@app.route('/iziet')
def logout():
    session.clear() 
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)