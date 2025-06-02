from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta, date
from flask import flash
import psycopg2
import re

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Configuración PostgreSQL
DB_HOST = "localhost"
DB_NAME = "db_init_alquilando"
DB_USER = "postgres"
DB_PASSWORD = "adrianingedos"

# Página principal
@app.route('/')
def pagina_inicio():
    hoy = date.today().isoformat()
    return render_template('inicio.html', fecha_actual=hoy)

#-----------------------------------------
#CERRAR SESION
#-----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for('login'))

# ----------------------------------------
# CONTRASEÑA SEGURA

# ----------------------------------------
def es_contraseña_segura(password):
    return (len(password) >= 6 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))  

# ----------------------------------------
# CONTROLES A REGISTRO USUARIO
# ----------------------------------------
def es_email_valido(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def solo_letras(texto):
    return re.fullmatch(r'[A-Za-z]{1,30}', texto)

def solo_numeros(texto, min_len, max_len):
    return texto.isdigit() and min_len <= len(texto) <= max_len
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

        # Validaciones
        if not solo_letras(nombre):
            flash("El nombre solo debe contener letras (hasta 30 caracteres).")
            return redirect(url_for('registro_usuario'))

        if not solo_letras(apellido):
            flash("El apellido solo debe contener letras (hasta 30 caracteres).")
            return redirect(url_for('registro_usuario'))

        if not solo_letras(nacionalidad):
            flash("La nacionalidad solo debe contener letras (hasta 30 caracteres).")
            return redirect(url_for('registro_usuario'))

        if not es_email_valido(email):
            flash("Correo electrónico inválido. Asegurate de que tenga formato correcto (ej: usuario@dominio.com).")
            return redirect(url_for('registro_usuario'))

        if not solo_numeros(dni, 7, 8):
            flash("El DNI debe contener solo números (7 u 8 dígitos).")
            return redirect(url_for('registro_usuario'))

        if not solo_numeros(telefono, 1, 16):
            flash("El teléfono debe contener solo números (sin guiones, hasta 16 dígitos).")
            return redirect(url_for('registro_usuario'))

        if not solo_numeros(numero_tarjeta, 16, 16):
            flash("La tarjeta de crédito debe tener exactamente 16 números, sin guiones.")
            return redirect(url_for('registro_usuario'))

        if not es_contraseña_segura(password):
            flash("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.")
            return redirect(url_for('registro_usuario'))
        
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
            # después de guardar el usuario y antes de redirigir
            flash('Se le ha enviado una notificación a su dirección de correo electrónico')
            #return redirect(url_for('sesionIniciada'))  # o la vista a la que vayas
            return redirect(url_for('login_usuario'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('registro_usuario'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('usuario/registroUsuario.html')

# -------------------------------------------------------
# RUTAS: EDITAR PERFIL, MENU ENCARGADO, MENUA ADMINISTRADOR
# -------------------------------------------------------
@app.route('/listado_propiedades')
def listado_propiedades():
    return render_template('encargado/listadoPropiedades.html')
    
@app.route('/menuEncargado')
def menu_Encargado():
    return render_template('encargado/menuEncargado.html')

@app.route('/menuAdministrador')
def menu_Administrador():
    return render_template('administrador/menuAdministrador.html')
#-------------------------------------------------------------------
#EDITAR PERFIL
#-------------------------------------------------------------------
@app.route('/editarPerfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario_id' not in session or 'usuario_tipo' not in session:
        flash("Primero debes iniciar sesión.")
        return redirect(url_for('login'))

    id_usuario = session['usuario_id']
    tipo_usuario = session['usuario_tipo']

    tabla = ""
    template = ""
    campos = []

    if tipo_usuario == "cliente":
        tabla = "cliente"
        template = "usuario/editarPerfil.html"
        campos = ['nombre', 'apellido', 'email', 'password', 'dni', 'telefono', 'numero_tarjeta', 'nacionalidad']
    elif tipo_usuario == "encargado":
        tabla = "encargado"
        template = "encargado/editarPerfilEncargado.html"
        campos = ['nombre', 'apellido', 'email', 'password']
    elif tipo_usuario == "administrador":
        tabla = "administrador"
        template = "Administrador/editarPerfilAdministrador.html"
        campos = ['nombre', 'apellido', 'email', 'password']
    else:
        flash("Tipo de usuario no válido.")
        return redirect(url_for('login'))

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()

    if request.method == 'POST':
        valores = [request.form.get(campo, '') for campo in campos]
        set_clause = ", ".join([f"{campo} = %s" for campo in campos])

        query = f'''
            UPDATE {tabla}
            SET {set_clause}
            WHERE id = %s
        '''
        cur.execute(query, (*valores, id_usuario))
        conn.commit()

        flash("Perfil actualizado correctamente.")
        cur.close()
        conn.close()
        return redirect(url_for('editar_perfil'))

    # Método GET: obtener datos actuales del usuario
    select_fields = ", ".join(campos)
    cur.execute(f'''
        SELECT {select_fields}
        FROM {tabla}
        WHERE id = %s
    ''', (id_usuario,))
    datos = cur.fetchone()
    cur.close()
    conn.close()

    if datos:
        usuario = dict(zip(campos, datos))
        return render_template(template, usuario=usuario)
    else:
        flash("No se encontraron datos del usuario.")
        return redirect(url_for('sesion_iniciada'))
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

        ahora = datetime.now()
        if 'intentos_login' not in session:
            session['intentos_login'] = {}

        intentos_info = session['intentos_login'].get(email, {'intentos': 0, 'bloqueado_hasta': None})

        if intentos_info['bloqueado_hasta']:
            bloqueado_hasta = datetime.fromisoformat(intentos_info['bloqueado_hasta'])
            if ahora < bloqueado_hasta:
                flash(f"Demasiados intentos fallidos. Intentá de nuevo después de las {bloqueado_hasta.strftime('%H:%M:%S')}.")
                return redirect(url_for('login'))
            else:
                intentos_info = {'intentos': 0, 'bloqueado_hasta': None}

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

                    # Limpiar intentos para este email
                    if email in session['intentos_login']:
                        del session['intentos_login'][email]

                    # Redirección según tipo de usuario
                    if tipo == 'cliente':
                        return redirect(url_for('sesion_iniciada'))
                    elif tipo == 'encargado':
                        return redirect(url_for('menu_encargado'))
                    elif tipo == 'administrador':
                        return redirect(url_for('menu_Administrador'))
                else:
                    intentos_info['intentos'] += 1
                    if intentos_info['intentos'] >= 3:
                        intentos_info['bloqueado_hasta'] = (ahora + timedelta(minutes=5)).isoformat()
                        flash("Demasiados intentos. Intentalo en 5 minutos.")
                    else:
                        flash("Contraseña incorrecta.")
            else:
                flash("Email no registrado.")

            session['intentos_login'][email] = intentos_info

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
#-----------------------------------------
# RECUPERO DE CONTRASEÑA
#-----------------------------------------
@app.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    return render_template('usuario/recuperarContraseñaDesdeEmail.html')
#-----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
