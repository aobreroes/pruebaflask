from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import datetime
from flask_mysqldb import MySQL




app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

#conexion db

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'aobrero'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'proyectoflask'
app.config['MYSQL_PORT'] = 8889

mysql = MySQL(app)

# context processor

@app.context_processor
def date_now():
    return {

        'now': datetime.utcnow()

    }


@app.route('/')
def index():
    
    edad = 16
    return render_template('index.html', edad=edad, dato='Hola', lista=['esto', 'es', 'una', 'lista'])

@app.route('/sobre-mi')
@app.route('/sobre-mi/<string:nombre>')
def sobremi(nombre = None):

    texto = ""
    if nombre != None:
        texto = f"<h1>Bienvenido {nombre}</h1>"

    return render_template('sobre-mi.html', texto=texto)

@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto(redireccion = None):

    if redireccion is not None:
        return redirect(url_for('lenguajes'))

    return render_template('contacto.html')

@app.route ('/lenguajes-de-programacion')
def lenguajes():

    return render_template('lenguajes.html')

@app.route ('/insertar_coche', methods=['GET', 'POST'])
def insertarcoche():
    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        localidad = request.form['localidad']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES(null, %s, %s, %s, %s)", (marca, modelo, precio, localidad))
        cursor.connection.commit()

        flash('Coche introducido correctamente')

        return redirect(url_for('listarcoches'))


    return render_template('insertar_coche.html')

@app.route('/listar_coches')
def listarcoches():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches")
    coches = cursor.fetchall()
    cursor.close()

    return render_template('listar_coches.html', coches=coches)

@app.route('/view_coche/<coche_id>')
def viewcoche(coche_id):

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id=%s", (coche_id,))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('view_coche.html', coche=coche)

@app.route('/borrar_coche/<coche_id>')
def borrarcoche(coche_id):

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM coches WHERE id=%s", (coche_id,))
    mysql.connection.commit()

    return redirect(url_for('listarcoches'))

@app.route('/editar_coche/<coche_id>', methods=['GET', 'POST'])
def editcoche(coche_id):

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        localidad = request.form['localidad']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE coches SET marca = %s,  modelo = %s,  precio = %s,  localidad = %s WHERE id=%s", (marca, modelo, precio, localidad, coche_id))
        cursor.connection.commit()

        flash('Coche editado correctamente')

        return redirect(url_for('listarcoches'))
        


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id=%s", (coche_id,))
    coche = cursor.fetchall()
    cursor.close()


    return render_template('insertar_coche.html', coche=coche[0])

if __name__ == '__main__':

    app.run(debug=True)