from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import psycopg2
import os

from ..db import obtener_conexion
from ..utils import es_contraseña_segura, es_email_valido, solo_letras, solo_numeros
from ..config import Config
from flask import current_app # Import current_app

auth_bp = Blueprint('auth', __name__)

#-----------------------------------------
#       RECUPERO DE E-MAIL
#-----------------------------------------
@auth_bp.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    mensaje = None
    if request.method == "POST":
        email = request.form["email"]

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                try:
                    msg = Message("Recuperación de contraseña - Alquilando",
                                recipients=[email])
                    msg.body = f"""
                    Hola, recibimos tu solicitud para recuperar la contraseña.

                    Si fuiste vos, hacé clic en el siguiente enlace para restablecerla:
                    http://localhost:5000/nueva_contraseña/{resultado[0]}

                    Si no fuiste vos, ignorá este mensaje.
                    """
                    current_app.extensions['mail'].send(msg) # Use current_app to access mail
                    mensaje = "Correo enviado con instrucciones para recuperar la contraseña."
                except Exception as e:
                    mensaje = f"Error al enviar el correo: {e}"

                    cursor.close()
                    conexion.close()
        except Exception as e:
            mensaje = f"Error al conectar con la base de datos: {e}"
                       
    return render_template("usuario/recuperarContraseña.html", mensaje=mensaje)

#-----------------------------------------
#           CERRAR SESION
#-----------------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for('auth.login'))

# ----------------------------------------
#           REGISTRO USUARIO
# ----------------------------------------
@auth_bp.route('/registroUsuario', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.registro_usuario'))

        if not solo_letras(apellido):
            flash("El apellido solo debe contener letras (hasta 30 caracteres).")
            return redirect(url_for('auth.registro_usuario'))

        if not solo_letras(nacionalidad):
            flash("La nacionalidad solo debe contener letras (hasta 30 caracteres).")
            return redirect(url_for('auth.registro_usuario'))

        if not es_email_valido(email):
            flash("Correo electrónico inválido. Asegurate de que tenga formato correcto (ej: usuario@dominio.com).")
            return redirect(url_for('auth.registro_usuario'))

        if not solo_numeros(dni, 7, 8):
            flash("El DNI debe contener solo números (7 u 8 dígitos).")
            return redirect(url_for('auth.registro_usuario'))

        if not solo_numeros(telefono, 1, 16):
            flash("El teléfono debe contener solo números (sin guiones, hasta 16 dígitos).")
            return redirect(url_for('auth.registro_usuario'))

        if not solo_numeros(numero_tarjeta, 16, 16):
            flash("La tarjeta de crédito debe tener exactamente 16 números, sin guiones.")
            return redirect(url_for('auth.registro_usuario'))

        if not es_contraseña_segura(password):
            flash("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.")
            return redirect(url_for('auth.registro_usuario'))
        
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM cliente WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un usuario con ese email.")
                return redirect(url_for('auth.registro_usuario'))

            cursor.execute('''
                INSERT INTO cliente (nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            flash('Se le ha enviado una notificación a su dirección de correo electrónico')
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('auth.registro_usuario'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('usuario/registroUsuario.html')

# ----------------------------------------
#           REGISTRO ENCARGADO
# ----------------------------------------
@auth_bp.route('/registroEncargado', methods=['GET', 'POST'])
def registro_encargado():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM encargado WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un encargado con ese email.")
                return redirect(url_for('auth.registro_encargado'))

            cursor.execute('INSERT INTO encargado (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
                           (nombre, apellido, email, password))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('auth.registro_encargado'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('encargado/registroEncargado.html')

# ----------------------------------------
#          REGISTRO ADMINISTRADOR
# ----------------------------------------
@auth_bp.route('/registroAdministrador', methods=['GET', 'POST'])
def registro_administrador():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM administrador WHERE email = %s', (email,))
            if cursor.fetchone():
                flash("Ya existe un admin con ese email.")
                return redirect(url_for('auth.registro_administrador'))

            cursor.execute('INSERT INTO administrador (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)',
                           (nombre, apellido, email, password))
            conn.commit()

            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"[ERROR] Error en el registro: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('auth.registro_administrador'))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('administrador/registroAdministrador.html')

#-----------------------------------------
#       LOGIN DE LOS TRES USUARIOS
#-----------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        ahora = datetime.now()
        if 'intentos_login' not in session:
            session['intentos_login'] = {}

        intentos_info = session['intentos_login'].get(email, {'intentos': 0, 'bloqueado_hasta': None})

        if intentos_info['bloqueado_hasta']:
            bloqueado_hasta = datetime.fromisoformat(intentos_info['bloqueado_hasta'])
            if ahora < bloqueado_hasta:
                flash(f"Demasiados intentos fallidos. Intentá de nuevo después de las {bloqueado_hasta.strftime('%H:%M:%S')}.")
                return redirect(url_for('auth.login'))
            else:
                intentos_info = {'intentos': 0, 'bloqueado_hasta': None}

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            tablas = ['cliente', 'encargado', 'administrador']
            usuario = None
            tipo_encontrado = None

            for tabla in tablas:
                cursor.execute(f"SELECT * FROM {tabla} WHERE email = %s", (email,))
                resultado = cursor.fetchone()
                if resultado:
                    usuario = resultado
                    tipo_encontrado = tabla
                    break

            if usuario:
                password_almacenada = usuario[4] if len(usuario) > 4 else None
                if password == password_almacenada:
                    session['usuario_id'] = usuario[0]
                    session['usuario_tipo'] = tipo_encontrado
                    session['usuario_nombre'] = usuario[1]
                    session['usuario_apellido'] = usuario[2]

                    if email in session['intentos_login']:
                        del session['intentos_login'][email]

                    return redirect(url_for('auth.sesion_iniciada'))

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
#           SESION INICIADA
#-----------------------------------------
@auth_bp.route('/sesion_iniciada')
def sesion_iniciada():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('usuario/sesionIniciada.html', 
                           tipo=session.get('usuario_tipo'),
                           nombre=session.get('usuario_nombre'))
