from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
import psycopg2

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Configuración PostgreSQL
DB_HOST = ""
DB_NAME = ""
DB_USER = "postgres"
DB_PASSWORD = "N1C0L45M0N74N4R1i$"

# Página principal
@app.route('/')
def pagina_inicio():
    hoy = date.today().isoformat()
    return render_template('inicio.html', fecha_actual=hoy)

#-----------------------------------------
#CERRAR SESION
#-----------------------------------------
'''
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('inicio'))
'''
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for('login'))
#    return redirect(url_for('login_usuario o inicio cualquiera'))

# ----------------------------------------
# REGISTRO USUARIO
# ----------------------------------------
@app.route('/registroUsuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        dni = request.form.get('dni', '').strip()
        telefono = request.form.get('telefono', '').strip()
        numero_tarjeta = request.form.get('numero_tarjeta', '').strip()
        nacionalidad = request.form.get('nacionalidad', '').strip()

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM cliente WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un usuario con ese email.")
                return redirect(url_for('registro_usuario'))

            cursor.execute('''
                INSERT INTO cliente (nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('login_usuario'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('registro_usuario'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('usuario/registroUsuario.html')

# ----------------------------------------
# EDITAR PERFIL
# ----------------------------------------
@app.route('/editarPerfil')
def editar_perfil():
    return render_template('usuario/editarPerfil.html')


# ----------------------------------------
# REGISTRO ENCARGADO
# ----------------------------------------
@app.route('/registroEncargado', methods=['GET', 'POST'])
def registro_encargado():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM encargado WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un encargado con ese email.")
                return redirect(url_for('registro_encargado'))

            cursor.execute('INSERT INTO encargado (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
                           (nombre, apellido, email, password))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('login_encargado'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('registro_encargado'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('encargado/registroEncargado.html')

# ----------------------------------------
# REGISTRO ADMINISTRADOR
# ----------------------------------------
@app.route('/registroAdministrador', methods=['GET', 'POST'])
def registro_administrador():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM administrador WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un admin con ese email.")
                return redirect(url_for('registro_administrador'))

            cursor.execute('INSERT INTO administrador (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
                           (nombre, apellido, email, password))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('login_administrador'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('registro_administrador'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('administrador/registroAdministrador.html')


# ----------------------------------------
# CHAT
# ----------------------------------------
@app.route('/chat')
def chat():
    if 'usuario_id' not in session:
        return redirect(url_for('login_usuario'))
    return render_template('usuario/chat.html')

#-----------------------------------------
# LOGIN DE LOS TRES USUARIOS
#-----------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        tabla = tipo if tipo in ['cliente', 'encargado', 'administrador'] else None
        if not tabla:
            flash("Tipo de usuario inválido.")
            return redirect(url_for('login'))

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {tabla} WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                password_almacenada = usuario[4] if len(usuario) > 4 else None
                if password == password_almacenada:
                    session['usuario_id'] = usuario[0]
                    session['usuario_tipo'] = tipo
                    session['usuario_nombre'] = usuario[1]
                    session['usuario_apellido'] = usuario[2]
                    return redirect(url_for('sesion_iniciada'))
                else:
                     flash("Contraseña incorrecta.")
                     session.clear()
            else:
                # Verificamos si existe en otra tabla
                otras_tablas = ['cliente', 'encargado', 'administrador']
                otras_tablas.remove(tabla)
                encontrado_en_otra = False

                for otra in otras_tablas:
                    cursor.execute(f"SELECT * FROM {otra} WHERE email = %s", (email,))
                    if cursor.fetchone():
                        encontrado_en_otra = True
                        flash(f"El email existe pero no corresponde al tipo seleccionado ({tipo}).")
                        break

                if not encontrado_en_otra:
                    flash("Email no registrado.")
                    session.clear()

        except Exception as e:
            print(f"[ERROR] Error de login: {e}")
            flash("Error del servidor.")

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('login.html')

#----------------------------------------
#SESION INICIADA
#-----------------------------------------
@app.route('/sesion_iniciada')
def sesion_iniciada():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('usuario/sesionIniciada.html', 
                           tipo=session.get('usuario_tipo'),
                           nombre=session.get('usuario_nombre'))
# ----------------------------------------

#-----------------------------------------
# RECUPERO DE CONTRASEÑA
#-----------------------------------------
@app.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    return render_template('recuperarContraseñaDesdeEmail.html')
#-----------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
