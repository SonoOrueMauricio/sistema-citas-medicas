from flask import Flask, render_template, request
from database import conectar
from flask import redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""

    if request.method == 'POST':
        print("Entró al POST")

        username = request.form['username']
        password = request.form['password']

        print("Usuario:", username)
        print("Password:", password)

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM usuario 
            WHERE username = %s AND password = %s
        """, (username, password))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            return redirect('/principal_usuario')
        else:
            mensaje = "❌ Usuario o contraseña incorrectos"

    return render_template('login.html', mensaje=mensaje)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = ""

    if request.method == 'POST':

        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        telefono = request.form['telefono']
        correo = request.form['correo']
        username = request.form['username']
        password = request.form['password']

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuario (username, password, rol)
                VALUES (%s, %s, %s)
                RETURNING id_usuario
            """, (username, password, "paciente"))

            id_usuario = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO paciente (id_usuario, dni, nombres, apellidos, telefono, correo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_usuario, dni, nombres, apellidos, telefono, correo))

            conexion.commit()

            cursor.close()
            conexion.close()

            mensaje = "✅ Usuario registrado correctamente"

        except Exception as e:
            print(e)
            mensaje = "❌ Error al registrar usuario"

    return render_template('registro.html', mensaje=mensaje)


@app.route('/panel')
def panel():
    return "<h1>✅ Bienvenido al sistema</h1>"


@app.route('/principal_usuario')
def principal_usuario():
    return render_template('principal_usuario.html')


if __name__ == '__main__':
    app.run(debug=True)
