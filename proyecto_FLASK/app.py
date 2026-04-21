from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "1234"

def conectar():
    return sqlite3.connect("mensajes.db")

# CREAR TABLA
with conectar() as con:
    con.execute("""
    CREATE TABLE IF NOT EXISTS mensajes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        telefono TEXT,
        direccion TEXT,
        servicio TEXT,
        mensaje TEXT,
        respuesta TEXT,
        fecha TEXT,
        estado TEXT
    )
    """)

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == "admin" and request.form['pwd'] == "1234":
            session['admin'] = True
            return redirect('/admin')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# PÁGINAS
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto', methods=['GET','POST'])
def contacto():
    if request.method == 'POST':
        datos = (
            request.form['nombre'],
            request.form['email'],
            request.form['telefono'],
            request.form['direccion'],
            request.form['servicio'],
            request.form['mensaje'],
            "",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "pendiente"
        )

        with conectar() as con:
            con.execute("INSERT INTO mensajes VALUES (NULL,?,?,?,?,?,?,?,?,?)", datos)

        return render_template('contacto.html', enviado=True)

    return render_template('contacto.html', enviado=False)

# ADMIN
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    with conectar() as con:
        mensajes = con.execute("SELECT * FROM mensajes ORDER BY id DESC").fetchall()

    return render_template('admin.html', mensajes=mensajes)

@app.route('/responder/<int:id>', methods=['POST'])
def responder(id):
    respuesta = request.form['respuesta']
    with conectar() as con:
        con.execute("UPDATE mensajes SET respuesta=?, estado='atendido' WHERE id=?", (respuesta,id))
    return redirect('/admin')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    with conectar() as con:
        con.execute("DELETE FROM mensajes WHERE id=?", (id,))
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)