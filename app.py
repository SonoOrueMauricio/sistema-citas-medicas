from flask import Flask, render_template, request
from database import conectar
from flask import redirect, url_for
from flask import request, jsonify

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
            return redirect(url_for('principal_usuario'))
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

            return redirect(url_for('login'))

        except Exception as e:
            print(e)
            mensaje = "❌ Error al registrar usuario"

    return render_template('registro.html', mensaje=mensaje)


@app.route('/principal_usuario')
def principal_usuario():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_especialidad, nombre FROM especialidad")
    especialidades = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('principal_usuario.html', especialidades=especialidades)


@app.route('/obtener_medicos/<int:id_especialidad>')
def obtener_medicos(id_especialidad):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_medico, nombres, apellidos
        FROM medico
        WHERE id_especialidad = %s
    """, (id_especialidad,))

    medicos = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultado = []

    for m in medicos:
        resultado.append({
            "id": m[0],
            "nombres": m[1] + " " + m[2]
        })

    return jsonify({"medicos": resultado})


@app.route('/guardar_cita', methods=['POST'])
def guardar_cita():
    data = request.get_json()
    descripcion = data['descripcion']
    especialidad = data['especialidad']
    fecha = data['fecha']
    hora = data['hora']
    medico = data['medico']

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO cita (id_paciente, id_medico, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s)
    """, (1, 1, fecha, hora, 'pendiente'))

    conexion.commit()
    cursor.close()
    conexion.close()

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
