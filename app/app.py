import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

# Rutas para Admi ------------------------------------------------


@app.route('/cerrar_sesion/admi')
def cerrar_sesion_admi():
    # Elimina la información de la sesión al cerrar sesión
    session.pop('admin', None)
    return redirect(url_for('admi'))


def check_login_admi(username, password):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()
    query = "SELECT * FROM ADMIS WHERE USERNAME=? AND CONTRASEÑA=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route("/admi", methods=["GET", "POST"])
def admi():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_login_admi(username, password)

        if user:
            # Almacena el nombre de usuario en la sesión
            session['admin'] = username
            return redirect(url_for('enlaces_admi'))
        else:
            return render_template('auth/admi.html', error='Credenciales incorrectas')

    return render_template('auth/admi.html', error=None)


@app.route("/admi/index", methods=["GET", "POST"])
def admi_index():
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla ADMIS
    cursor.execute('SELECT * FROM ADMIS')
    registros = cursor.fetchall()

    conn.close()

    return render_template("admi/ver_admi.html", registros=registros)


@app.route("/admi/enlaces")
def enlaces_admi():
    return render_template("admi/index.html")


@app.route("/admi/enlaces/registros")
def registros_admi():
    return render_template("admi/registros.html")


@app.route("/admi/enlaces/ver")
def ver_admi():
    return render_template("admi/ver.html")


@app.route("/admi/enlaces/actualizar/")
def actualizar_enlace():
    return render_template("admi/actualizar.html")


@app.route("/admi/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar_admi(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener el registro específico de la tabla ADMIS
    cursor.execute('SELECT * FROM ADMIS WHERE ID = ?', (id,))
    registro = cursor.fetchone()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        username = request.form["username"]
        num_id = request.form["num_id"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        contraseña = request.form["contraseña"]

        # Actualizar el registro en la base de datos
        cursor.execute('''
            UPDATE ADMIS
            SET NOMBRE = ?, APELLIDO = ?, USERNAME = ?,
                NUM_ID = ?, CORREO = ?, TELEFONO = ?, CONTRASEÑA = ?
            WHERE ID = ?
        ''', (nombre, apellido, username, num_id, correo, telefono, contraseña, id))

        conn.commit()
        conn.close()

        return redirect(url_for("admi_index"))
    conn.close()

    return render_template("admi/update.html", registro=registro)


@app.route("/admi/register", methods=["GET", "POST"])
def admi_insert():
    if request.method == "POST":
        # Obtine los datos del formulario
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        num_id = request.form["num_id"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        username = request.form["username"]
        contraseña = request.form["contraseña"]

        conn = sqlite3.connect('instance/WCS.db')
        cursor = conn.cursor()

        # Inserta el nuevo dato en la base de datos
        cursor.execute(
            'INSERT INTO ADMIS (NOMBRE, APELLIDO, NUM_ID, CORREO, TELEFONO, USERNAME, CONTRASEÑA) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (nombre, apellido, num_id, correo, telefono, username, contraseña)
        )
        conn.commit()
        conn.close()

        # Redirige a la página principal después de la inserción
        return redirect(url_for('admi'))

    return render_template("admi/admi_register.html")


@app.route("/admi/<int:id>")
def eliminar_admi(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM admis WHERE ID = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admi_index'))


# Rutas para Manejador ------------------------------------------------

@app.route('/cerrar_sesion/manejador')
def cerrar_sesion_manejador():
    # Elimina la información de la sesión al cerrar sesión
    session.pop('manejador', None)
    return redirect(url_for('manejador'))


def check_login_manejador(username, password):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM MANEJADORES WHERE USERNAME=? AND CONTRASEÑA=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route("/manejador", methods=["GET", "POST"])
def manejador():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_login_manejador(username, password)

        if user:
            # Autenticación exitosa, puedes redirigir a la página principal
            session['manejador'] = username
            return redirect(url_for('manejador_index'))
        else:
            # Autenticación fallida, puedes mostrar un mensaje de error
            return render_template('auth/manejador.html', error='Credenciales incorrectas')

    return render_template("auth/manejador.html", error=None)


@app.route('/manejador/index')
def manejador_index():

    return redirect(url_for('registrar_detalles'))


@app.route("/manejador/ver")
def ver_manejador():
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla ADMIS
    cursor.execute('SELECT * FROM manejadores')
    registros = cursor.fetchall()

    conn.close()

    return render_template("manejador/ver_manejador.html", registros=registros)


@app.route("/manejador/register", methods=["GET", "POST"])
def manejador_insert():
    if request.method == "POST":
        # Obtine los datos del formulario
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        num_id = request.form["num_id"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        username = request.form["username"]
        contraseña = request.form["contraseña"]

        conn = sqlite3.connect('instance/WCS.db')
        cursor = conn.cursor()

        # Inserta el nuevo dato en la base de datos
        cursor.execute(
            'INSERT INTO MANEJADORES (NOMBRE, APELLIDO, NUM_ID, CORREO, TELEFONO, USERNAME, CONTRASEÑA) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (nombre, apellido, num_id, correo, telefono, username, contraseña)
        )
        conn.commit()
        conn.close()

        # Redirige a la página principal después de la inserción
        return redirect(url_for('manejador'))

    return render_template("manejador/manejador_register.html")


@app.route("/manejador/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar_manejador(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM MANEJADORES WHERE ID = ?', (id,))
    registro = cursor.fetchone()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        username = request.form["username"]
        num_id = request.form["num_id"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        contraseña = request.form["contraseña"]

        # Actualizar el registro en la base de datos
        cursor.execute('''
            UPDATE Manejadores
            SET NOMBRE = ?, APELLIDO = ?, USERNAME = ?,
                NUM_ID = ?, CORREO = ?, TELEFONO = ?, CONTRASEÑA = ?
            WHERE ID = ?
        ''', (nombre, apellido, username, num_id, correo, telefono, contraseña, id))

        conn.commit()
        conn.close()

        return redirect(url_for("ver_manejador"))
    conn.close()

    return render_template("manejador/update.html", registro=registro)


@app.route("/manejador/<int:id>")
def eliminar_manejador(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM MANEJADORES WHERE ID = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('ver_manejador'))

    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Verifica si hay una sesión activa y si el usuario es un manejador
    if 'usuario' in session and session['tipo_usuario'] == 'manejador':
        cursor.execute('SELECT * FROM camiones WHERE ID = ?', (id,))
        registro = cursor.fetchone()

        if registro:
            if request.method == "POST":
                # Obtén los datos del formulario
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                username = request.form["username"]
                num_id = request.form["num_id"]
                correo = request.form["correo"]
                telefono = request.form["telefono"]
                contraseña = request.form["contraseña"]

                # Actualiza el registro en la base de datos
                cursor.execute('''
                    UPDATE camiones
                    SET NOMBRE = ?, APELLIDO = ?, USERNAME = ?,
                        NUM_ID = ?, CORREO = ?, TELEFONO = ?, CONTRASEÑA = ?
                    WHERE ID = ?
                ''', (nombre, apellido, username, num_id, correo, telefono, contraseña, id))

                conn.commit()
                conn.close()

                return redirect(url_for("ver_manejador"))

            conn.close()

            return render_template("manejador/update.html", registro=registro)
        else:
            conn.close()
            return "Registro no encontrado"
    else:
        # Redirige a la página de inicio de sesión si no hay una sesión activa o el usuario no es un manejador
        return redirect(url_for("manejador"))


# Rutas Para Camiones ------------------------------------------------


@app.route("/camiones/ver")
def ver_camiones():

    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla ADMIS
    cursor.execute('SELECT * FROM Camiones')
    registros = cursor.fetchall()

    conn.close()

    return render_template("camiones/index.html", registros=registros)


@app.route("/camiones/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar_camiones(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener el registro específico de la tabla manejadorS
    cursor.execute('SELECT * FROM camiones WHERE ID = ?', (id,))
    registro = cursor.fetchone()

    if request.method == "POST":
        placa = request.form['placa']
        modelo = request.form['modelo']
        capacidad = request.form['capacidad']
        id_manejador = request.form['id_manejador']

        # Actualizar el registro en la base de datos
        cursor.execute("""
            UPDATE CAMIONES
            SET PLACA = ?, MODELO = ?, CAPACIDAD = ?, ID_MANEJADOR = ?
            WHERE ID = ?
        """, (placa, modelo, capacidad, id_manejador, id))

        conn.commit()
        conn.close()

        return redirect(url_for("ver_camiones"))
    conn.close()

    return render_template("camiones/update.html", registro=registro)


@app.route("/camiones/registros", methods=["GET", "POST"])
def registrar_camiones():
    if request.method == "POST":
        # Obtener los datos del formulario
        placa = request.form["placa"]
        modelo = request.form["modelo"]
        capacidad = request.form["capacidad"]
        id_manejador = request.form["id_manejador"]

        conn = sqlite3.connect("instance/WCS.db")
        cursor = conn.cursor()

        # Verificar que las claves foráneas existan
        cursor.execute('SELECT 1 FROM MANEJADORES WHERE ID = ?',
                       (id_manejador,))
        maneja_exists = cursor.fetchone()

        errors = {}

        # Verificar si las claves foráneas existen antes de realizar la inserción
        if not maneja_exists:
            errors['id_manejador'] = 'El ID del manejador no existe.'

        # Verificar si hay errores
        if errors:
            error_message = 'Errores en las claves foráneas. Verifica las IDs:'
            conn.close()
            return render_template('camiones/create.html', error_message=error_message, errors=errors)
        else:
            # Insertar el nuevo dato en la base de datos
            cursor.execute(
                "INSERT INTO CAMIONES (PLACA, MODELO, CAPACIDAD, ID_MANEJADOR) VALUES (?, ?, ?, ?)",
                (placa, modelo, capacidad, id_manejador),
            )
            conn.commit()
            conn.close()

            # Redirigir a la página principal después de la inserción
            flash('Inserción exitosa!', 'success')
            return redirect(url_for("enlaces_admi"))

    return render_template("camiones/create.html")


@app.route("/camiones/<int:id>")
def eliminar_camiones(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM CAMIONES WHERE ID = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('ver_camiones'))


# Rutas para Puntos de Recoleccion ------------------------------------------------


@app.route("/puntosr/ver")
def ver_puntosr():
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla ADMIS
    cursor.execute('SELECT * FROM puntos_recoleccion')
    registros = cursor.fetchall()

    conn.close()

    return render_template("puntos_recoleccion/index.html", registros=registros)


@app.route("/puntosr/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar_puntosr(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener el registro específico de la tabla PUNTOS_RECOLECCION
    cursor.execute('SELECT * FROM PUNTOS_RECOLECCION WHERE ID = ?', (id,))
    registro = cursor.fetchone()

    if request.method == "POST":
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad = request.form['capacidad']
        ultima_fecha_recoleccion = request.form['ultima_fecha_recoleccion']
        id_camiones = request.form['id_camiones']

        # Actualizar el registro en la base de datos
        cursor.execute("""
            UPDATE PUNTOS_RECOLECCION
            SET NOMBRE = ?, UBICACION = ?, CAPACIDAD = ?, ULTIMA_FECHA_RECOLECCION = ?, ID_CAMIONES = ?
            WHERE ID = ?
        """, (nombre, ubicacion, capacidad, ultima_fecha_recoleccion, id_camiones, id))

        conn.commit()
        conn.close()

        return redirect(url_for("ver_puntosr"))

    conn.close()

    return render_template("puntos_recoleccion/update.html", registro=registro)


@app.route("/puntosr/registros", methods=["GET", "POST"])
def registrar_puntosr():
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form["nombre"]
        ubicacion = request.form["ubicacion"]
        capacidad = request.form["capacidad"]
        ultima_fecha_recoleccion = request.form["ultima_fecha_recoleccion"]
        id_camiones = request.form["id_camiones"]

        conn = sqlite3.connect('instance/WCS.db')
        cursor = conn.cursor()

        # Verificar si el ID del camión existe
        cursor.execute(
            'SELECT 1 FROM CAMIONES WHERE ID = ?', (id_camiones,))
        camion_exists = cursor.fetchone()

        errors = {}

        if not camion_exists:
            errors['id_camion'] = 'El ID del camión no existe.'

        if errors:
            error_message = 'Errores en las claves foráneas. Verifica las IDs:'
            conn.close()
            return render_template('puntos_recoleccion/create.html', error_message=error_message, errors=errors)
        else:
            # Insertar el nuevo dato en la base de datos
            cursor.execute(
                'INSERT INTO PUNTOS_RECOLECCION (NOMBRE, UBICACION, CAPACIDAD, ULTIMA_FECHA_RECOLECCION, ID_CAMIONES) VALUES (?, ?, ?, ?, ?)',
                (nombre, ubicacion, capacidad,
                 ultima_fecha_recoleccion, id_camiones)
            )
            conn.commit()
            conn.close()

            flash('Registro exitoso', 'success')
            return redirect(url_for('enlaces_admi'))

    return render_template("puntos_recoleccion/create.html")


@app.route("/puntosr/<int:id>")
def eliminar_puntosr(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM PUNTOS_RECOLECCION WHERE ID = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('ver_puntosr'))

# Rutas de Detalle de recoleccion ------------------------------------------------


@app.route("/detalle_recoleccion/ver")
def ver_detalles():

    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla ADMIS
    cursor.execute('SELECT * FROM detalles_recoleccion')
    registros = cursor.fetchall()

    conn.close()

    return render_template("detalle_recoleccion/index.html", registros=registros)


@app.route("/detalles_recoleccion/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar_detalles(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    # Obtener el registro específico de la tabla DETALLES_RECOLECCION
    cursor.execute('SELECT * FROM DETALLES_RECOLECCION WHERE ID = ?', (id,))
    registro = cursor.fetchone()

    if request.method == "POST":
        id_manejador = request.form['id_manejador']
        id_camion = request.form['id_camion']
        id_punto_recoleccion = request.form['id_punto_recoleccion']
        fecha = request.form['fecha']
        plastico = request.form['plastico']
        carton = request.form['carton']
        organicos = request.form['organicos']

        # Actualizar el registro en la base de datos
        cursor.execute("""
            UPDATE DETALLES_RECOLECCION
            SET ID_MANEJADOR = ?, ID_CAMION = ?, ID_PUNTO_RECOLECCION = ?, FECHA = ?,
                PLASTICO = ?, CARTON = ?, ORGANICOS = ?
            WHERE ID = ?
        """, (id_manejador, id_camion, id_punto_recoleccion, fecha, plastico, carton, organicos, id))

        conn.commit()
        conn.close()

        return redirect(url_for("ver_detalles"))

    conn.close()

    return render_template("detalle_recoleccion/update.html", registro=registro)


@app.route("/detalle_recoleccion/registros", methods=["GET", "POST"])
def registrar_detalles():
    if request.method == "POST":
        # Obtener los datos del formulario
        id_manejador = request.form["id_manejador"]
        id_camion = request.form["id_camion"]
        id_punto_recoleccion = request.form["id_punto_recoleccion"]
        fecha = request.form["fecha"]
        plastico = request.form["plastico"]
        carton = request.form["carton"]
        organicos = request.form["organicos"]

        conn = sqlite3.connect('instance/WCS.db')
        cursor = conn.cursor()

        # Verificar que las claves foráneas existan
        cursor.execute('SELECT 1 FROM MANEJADORES WHERE ID = ?',
                       (id_manejador,))
        maneja_exists = cursor.fetchone()

        cursor.execute('SELECT 1 FROM CAMIONES WHERE ID = ?', (id_camion,))
        camion_exists = cursor.fetchone()

        cursor.execute(
            'SELECT 1 FROM PUNTOS_RECOLECCION WHERE ID = ?', (id_punto_recoleccion,))
        punto_exists = cursor.fetchone()

        errors = {}

        # Verificar si las claves foráneas existen antes de realizar la inserción
        if not maneja_exists:
            errors['id_manejador'] = 'El ID del manejador no existe.'

        if not camion_exists:
            errors['id_camion'] = 'El ID del camión no existe.'

        if not punto_exists:
            errors['id_punto_recoleccion'] = 'El ID del punto de recolección no existe.'

        # Verificar si hay errores
        if errors:
            error_message = 'Errores en las claves foráneas. Verifica las IDs:'
            conn.close()
            return render_template('detalle_recoleccion/create.html', error_message=error_message, errors=errors)
        else:
            # Insertar el nuevo dato en la base de datos
            cursor.execute(
                'INSERT INTO DETALLES_RECOLECCION (ID_MANEJADOR, ID_CAMION, ID_PUNTO_RECOLECCION, FECHA, PLASTICO, CARTON, ORGANICOS) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (id_manejador, id_camion, id_punto_recoleccion,
                 fecha, plastico, carton, organicos)
            )
            conn.commit()
            conn.close()

            # Redirigir a la página principal después de la inserción
            flash('Inserción exitosa!', 'success')
            return redirect(url_for('manejador_index'))

    return render_template("detalle_recoleccion/create.html")


@app.route("/detalles/<int:id>")
def eliminar_detalles(id):
    conn = sqlite3.connect('instance/WCS.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM DETALLES_RECOLECCION WHERE ID = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('ver_detalles'))


if __name__ == "__main__":
    app.run(debug=True)
