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
   # return render_template('inicio.html', fecha_actual=hoy)#
    #return render_template('inicio.html')
    return render_template('encargado/registroEncargado.html', fecha_actual=hoy)
   # return render_template('administrador/registroAdministrador.html', fecha_actual=hoy)
# ----------------------------------------
# LOGIN USUARIO
# ----------------------------------------
@app.route('/loginUsuario', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM cliente WHERE email = %s AND password = %s', (email, password))
            cliente = cursor.fetchone()

            if cliente:
                nombre = cliente[1]
                apellido = cliente[2]
                return render_template('usuario/sesionIniciada.html')
            #    return f"Bienvenido {nombre} {apellido}!"

            else:
                flash("Email o contraseña incorrectos.")
                return redirect(url_for('login_usuario'))

        except Exception as e:
            print(f"[ERROR] Error al iniciar sesión de usuario: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('login_usuario'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
            
    return render_template('usuario/loginUsuario.html')
#    return render_template('usuario/sesionIniciada.html')
   

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

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM cliente WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un usuario con ese email.")
                return redirect(url_for('registro_usuario'))

            cursor.execute('INSERT INTO cliente (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
                           (nombre, apellido, email, password))
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
# LOGIN ENCARGADO
# ----------------------------------------
@app.route('/loginEncargado', methods=['GET', 'POST'])
def login_encargado():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        print(f"[DEBUG] Email ingresado: {email}, Password ingresado: {password}")
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM encargado WHERE email = %s', (email,))
            usuario_por_email = cursor.fetchone()

            if usuario_por_email:
                password_almacenada = usuario_por_email[4] if len(usuario_por_email) > 4 else None
                if password == password_almacenada:
                    nombre = usuario_por_email[1]
                    apellido = usuario_por_email[2]
                    # Guardar datos en sesión
                    session['nombre'] = nombre
                    session['apellido'] = apellido
                    session['rol'] = 'encargado'
                    encargado_id = usuario_por_email[0]
                    session['encargado_id'] = encargado_id
                    return redirect(url_for('menu_encargado'))

                else:
                    flash("Contraseña incorrecta.")
            else:
                flash("El email no existe en nuestra base de datos.")

        except Exception as e:
            print(f"[ERROR] Fallo de conexión o consulta: {e}")
            flash("Error en el servidor.")

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('encargado/loginEncargado.html')


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

            cursor.execute('SELECT * FROM Encargado WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un encargado con ese email.")
                return redirect(url_for('registro_usuario'))

            cursor.execute('INSERT INTO Encargado (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
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
# LOGIN ADMINISTRADOR
# ----------------------------------------
@app.route('/loginAdministrador', methods=['GET', 'POST'])
def login_administrador():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM Administrador WHERE email = %s', (email,))
            usuario_por_email = cursor.fetchone()

            if usuario_por_email:
                password_almacenada = usuario_por_email[4] if len(usuario_por_email) > 4 else None
                if password == password_almacenada:
                    nombre = usuario_por_email[1]
                    apellido = usuario_por_email[2]
                    return f"Bienvenido {nombre} {apellido}!"
                else:
                    flash("Contraseña incorrecta.")
            else:
                flash("El email no existe en nuestra base de datos.")

        except Exception as e:
            print(f"[ERROR] Fallo de conexión o consulta: {e}")
            flash("Error en el servidor.")

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('administrador/loginAdministrador.html')



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

            cursor.execute('SELECT * FROM Administrador WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un admin con ese email.")
                return redirect(url_for('registro_administrador'))

            cursor.execute('INSERT INTO Administrador (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
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
# MENU ENCARGADO
# ----------------------------------------

@app.route('/menu_encargado')
def menu_encargado():
    print(f"[DEBUG] Accediendo a /menu_encargado, sesión: {dict(session)}")
    if 'nombre' not in session:
        print("[DEBUG] No hay 'nombre' en sesión. Redirigiendo a login.")
        return redirect(url_for('login_encargado'))
    nombre = session['nombre']
    return render_template('encargado/menuEncargado.html', nombre=nombre)

    

@app.route('/encargado/propiedades')
def listado_propiedades():
    encargado_id = session['encargado_id']
    propiedades = []

    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        query = '''
        SELECT p.id, p.calle, p.dpto, p.piso, p.numero, p.cantidad_ambientes, p.petfriendly, p.listada,
               (SELECT url FROM imagen i WHERE i.propiedad_id = p.id LIMIT 1) AS imagen_url
        FROM propiedad p
        WHERE p.encargado_id = %s;
        '''
        cursor.execute(query, (encargado_id,))
        propiedades = cursor.fetchall()

    except Exception as e:
        print(f"[ERROR] al consultar propiedades: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    return render_template('encargado/listadoPropiedades.html', propiedades=propiedades)

#CERRAR SESION 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_encargado'))

# ----------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
