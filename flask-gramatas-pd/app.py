from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'kaza1'

# --- PIEKĻUVES KONTROLE (GATEKEEPER) ---
#@app.before_request
#def gatekeeper():

    #publiskie_celi = ['sakums', 'pieteikties', 'registreties', 'static']
    
    # Ja lietotājs nav sesijā un mēģina piekļūt ne-publiskam ceļam
    #if 'id' not in session and request.endpoint not in publiskie_celi:
        #return redirect("/pieteikties")

@app.route("/")
def sakums():
    return render_template("sakums.html")

@app.route("/pieteikties")
def pieteikties():
    
    return render_template("pieteikties.html", methods=['GET', 'POST'])

@app.route("/registreties", methods=['GET', 'POST'])
def registreties():
    
    return render_template("registreties.html")



@app.route('/iziet')
def logout():
    session.clear() # Iztīra visu sesiju
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)