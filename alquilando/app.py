from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta, date
from flask import flash
from flask_mail import Mail, Message
from flask import render_template, request, redirect, url_for
import psycopg2
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

UPLOAD_FOLDER = os.path.join('static', 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'avif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración PostgreSQL
DB_HOST = "localhost"
DB_NAME = "db_init_alquilando" #"alquilando_db"        
DB_USER = "postgres"
DB_PASSWORD = "adrianingedos"

#-------------------------------------------
def obtener_conexion():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
#-------------------------------------------
#           Página principal
#-------------------------------------------
@app.route('/')
def pagina_inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id, p.descripcion, p.ciudad, p.precio_por_noche, i.url
        FROM propiedad p
        JOIN imagen i ON p.id = i.propiedad_id
        WHERE p.activo = TRUE
        LIMIT 6
    """)
    propiedades = cursor.fetchall()
    return render_template('inicio.html', propiedades=propiedades)

#-----------------------------------------
#       RECUPERO DE E-MAIL
#-----------------------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'         # o tu servidor SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adrian.sambido40911@alumnos.info.unlp.edu.ar'# ⚠️ Tu email real
app.config['MAIL_PASSWORD'] = 'ipnp eklu ukdg bxdu' #'Informatica2021'      # ⚠️ Usá token de Gmail si tenés 2FA
app.config['MAIL_DEFAULT_SENDER'] = 'adrian.sambido40911@alumnos.info.unlp.edu.ar'

mail = Mail(app)
#Si usás Gmail y tenés autenticación de dos factores (2FA), necesitás un "App Password". 
#Lo podés generar desde: https://myaccount.google.com/apppasswords 

#---------------------------------------------------
#           RECUPERO DE CONTRASEÑA
#---------------------------------------------------
@app.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    mensaje = None
    if request.method == "POST":
        email = request.form["email"]

        try:
            conexion = psycopg2.connect(
                dbname="db_init_alquilando",
                user="postgres",         # ← Reemplazá con tu usuario
                password="adrianingedos",  # ← Y contraseña
                host="localhost",
                port="5432"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                try:
                    # Podés generar un token, o simplemente incluir una instrucción básica
                    msg = Message("Recuperación de contraseña - Alquilando",
                                recipients=[email])
                    msg.body = f"""
                    Hola, recibimos tu solicitud para recuperar la contraseña.

                    Si fuiste vos, hacé clic en el siguiente enlace para restablecerla:
                    http://localhost:5000/nueva_contraseña/{resultado[0]}

                    Si no fuiste vos, ignorá este mensaje.
                    """
                    mail.send(msg)
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
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for('login'))

# ----------------------------------------
#           CONTRASEÑA SEGURA
# ----------------------------------------
def es_contraseña_segura(password):
    return (len(password) >= 6 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))  
# ----------------------------------------
#       CONTROLES A REGISTRO USUARIO
# ----------------------------------------
def es_email_valido(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def solo_letras(texto):
    return re.fullmatch(r'[A-Za-z]{1,30}', texto)

def solo_numeros(texto, min_len, max_len):
    return texto.isdigit() and min_len <= len(texto) <= max_len
# ----------------------------------------
#           REGISTRO USUARIO
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
#               LISTA DE PROPIEDADES
# -------------------------------------------------------
@app.route('/listado_propiedades')
def listado_propiedades():
    origen = request.args.get('origen', 'encargado')  # valor por defecto: encargado
    # Conectás con la base, traés las propiedades, y las mandás al template
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT * FROM propiedad")  # ajustá la consulta según tus columnas
    propiedades = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('encargado/listadoPropiedades.html', propiedades=propiedades, origen=origen)
#------------------------------------------------
#       VER DETALLE DE LAS PROPIEDADES
#------------------------------------------------
@app.route('/detalle_propiedad/<int:propiedad_id>')
def ver_detalle_propiedad(propiedad_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM propiedad WHERE id = %s", (propiedad_id,))
    propiedad = cursor.fetchone()
    conexion.close()

    if propiedad:
        return render_template('detalle_propiedad.html', propiedad=propiedad)
    else:
        return "Propiedad no encontrada", 404
#-------------------------------------------------------------------
@app.route('/menuEncargado')
def menu_encargado():
    return render_template('encargado/menuEncargado.html')

@app.route('/menuAdministrador')
def menu_administrador():
    return render_template('administrador/menuAdministrador.html')

#-------------------------------------------------------------------
#                   BUSCAR PROPIEDAD
#-------------------------------------------------------------------
@app.route('/buscar_propiedad', methods=['GET', 'POST'])
def buscar_propiedad():
    propiedades = []
    mensaje = ""

    if request.method == 'POST':
        termino = request.form.get('termino', '').strip().lower()

        if termino:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta = """
                SELECT id, dpto, piso, numero, calle, ciudad, provincia, descripcion, 
                    precio_por_noche, capacidad_personas, tipo_propiedad
                FROM propiedad
                WHERE 
                    LOWER(dpto) LIKE %s OR
                    LOWER(piso) LIKE %s OR
                    LOWER(numero) LIKE %s OR
                    LOWER(calle) LIKE %s OR
                    LOWER(ciudad) LIKE %s OR
                    LOWER(provincia) LIKE %s
            """
            parametros = tuple(f'%{termino}%' for _ in range(6))

            cursor.execute(consulta, parametros)
            propiedades = cursor.fetchall()

            conn.close()

            if not propiedades:
                mensaje = "No se encontraron propiedades que coincidan con el término ingresado."
        else:
            mensaje = "Por favor, ingresá un término para buscar."

    return render_template('administrador/buscarPropiedad.html', propiedades=propiedades, mensaje=mensaje)

#-------------------------------------------------------------------
#                   EDITAR PROPIEDAD
#-------------------------------------------------------------------
@app.route('/editar_propiedad/<int:propiedad_id>', methods=['GET', 'POST'])
def editar_propiedad(propiedad_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        calle = request.form['calle']
        numero = request.form['numero']
        piso = request.form.get('piso', '')
        dpto = request.form.get('dpto', '')
        ciudad = request.form['ciudad']
        provincia = request.form['provincia']
        descripcion = request.form['descripcion']

        # actualizar propiedad
        cursor.execute("""
            UPDATE propiedad
            SET calle = %s, numero = %s, piso = %s, dpto = %s,
                ciudad = %s, provincia = %s, descripcion = %s
            WHERE id = %s
        """, (calle, numero, piso, dpto, ciudad, provincia, descripcion, propiedad_id))

        # eliminar imágenes seleccionadas
        ids_a_borrar = request.form.getlist('eliminar_imagen[]')
        for id_img in ids_a_borrar:
            cursor.execute("DELETE FROM imagen WHERE id = %s", (id_img,))

        # subir nuevas imágenes
        nuevas = request.files.getlist('imagenes')
        for img in nuevas:
            if img and allowed_file(img.filename):
                nombre = secure_filename(img.filename).replace(" ", "_")
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre)
                img.save(ruta)
                ruta_rel = os.path.join("img", nombre).replace("\\", "/")
                cursor.execute(
                    "INSERT INTO imagen (url, propiedad_id) VALUES (%s, %s)",
                    (ruta_rel, propiedad_id)
                )

        conexion.commit()
        flash("Propiedad actualizada correctamente.")
        return redirect(url_for('buscar_propiedad'))

    # GET: cargar datos actuales de la propiedad
    cursor.execute("""
        SELECT calle, numero, piso, dpto, ciudad, provincia, descripcion
        FROM propiedad
        WHERE id = %s
    """, (propiedad_id,))
    datos = cursor.fetchone()

    if not datos:
        flash("Propiedad no encontrada.")
        return redirect(url_for('buscar_propiedad'))

    campos = ['calle', 'numero', 'piso', 'dpto', 'ciudad', 'provincia', 'descripcion']
    propiedad = dict(zip(campos, datos))

    # cargar imágenes actuales
    cursor.execute("SELECT id, url FROM imagen WHERE propiedad_id = %s", (propiedad_id,))
    imagenes = cursor.fetchall()

    return render_template('administrador/editarPropiedad.html', propiedad_id=propiedad_id, propiedad=propiedad, imagenes=imagenes)

#-------------------------------------------------------------------
#               DAR DE ALTA PROPIEDAD
#-------------------------------------------------------------------
@app.route('/darDeAltaPropiedad', methods=['GET', 'POST'])
def dar_de_alta_propiedad():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM encargado")
    encargados = cursor.fetchall()

    if request.method == 'POST':
        datos = {
            'dpto': request.form.get('dpto', ''),
            'piso': request.form.get('piso', ''),
            'numero': request.form.get('numero', ''),
            'calle': request.form.get('direccion', ''),  # Cambia esto si tu campo en la tabla se llama distinto
            'cantidad_ambientes': request.form.get('cantidad_ambientes', 1),
            'petfriendly': bool(request.form.get('petfriendly')),
            'encargado_id': request.form['encargado_id'],
            'pais': request.form['pais'],
            'ciudad': request.form['ciudad'],
            'provincia': request.form['provincia'],
            'precio_por_noche': request.form['precio_por_noche'],
            'descripcion': request.form['descripcion'],
            'capacidad_personas': request.form['capacidad_personas'],
            'tipo_propiedad': request.form['tipo_propiedad'],
            'activo': 'activo' in request.form
        }

        imagen_archivo = request.files['imagen']
        if imagen_archivo and allowed_file(imagen_archivo.filename):
            nombre_archivo = secure_filename(imagen_archivo.filename)
            ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
            imagen_archivo.save(ruta_completa)
            ruta_relativa = os.path.join('img', nombre_archivo)
        else:
            flash("Formato de imagen inválido.")
            return redirect(request.url)

        # Insertar propiedad con todos los campos
        cursor.execute("""
            INSERT INTO propiedad (
                dpto, piso, numero, calle, cantidad_ambientes, petfriendly,
                encargado_id, pais, ciudad, provincia, precio_por_noche,
                descripcion, capacidad_personas, tipo_propiedad, activo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            datos['dpto'],
            datos['piso'],
            datos['numero'],
            datos['calle'],
            datos['cantidad_ambientes'],
            datos['petfriendly'],
            datos['encargado_id'],
            datos['pais'],
            datos['ciudad'],
            datos['provincia'],
            datos['precio_por_noche'],
            datos['descripcion'],
            datos['capacidad_personas'],
            datos['tipo_propiedad'],
            datos['activo']
        ))
        propiedad_id = cursor.fetchone()[0]

        # Insertar imagen
        cursor.execute("INSERT INTO imagen (url, propiedad_id) VALUES (%s, %s)", (ruta_relativa, propiedad_id))
        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Propiedad agregada con éxito.")
        return redirect(url_for('menu_administrador'))

    return render_template('administrador/darDeAltaPropiedad.html', encargados=encargados)
#-------------------------------------------------------------------
#           LISTADO DE PROPIEDADES POR ENCARGADO
#-------------------------------------------------------------------
@app.route('/ver_propiedades_encargado', methods=['GET', 'POST'])
def ver_propiedades_encargado():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()

    if request.method == 'POST':
        encargado_id = request.form['encargado_id']

        # Traer nombre y apellido del encargado
        cur.execute("SELECT nombre, apellido FROM encargado WHERE id = %s", (encargado_id,))
        encargado = cur.fetchone()

        # Traer propiedades del encargado con imagen (JOIN a tabla imagen)
        cur.execute("""
            SELECT p.dpto, p.piso, p.numero, p.calle, p.cantidad_ambientes, p.petfriendly,
                   p.listada, p.encargado_id, i.url, p.pais, p.favorita
            FROM propiedad p
            LEFT JOIN imagen i ON p.id = i.propiedad_id
            WHERE p.encargado_id = %s
        """, (encargado_id,))
        propiedades = cur.fetchall()

        cur.close()
        conn.close()
        return render_template('encargado/propiedadesPorEncargado.html',
                               encargado=encargado, propiedades=propiedades)

    # GET: lista de encargados
    cur.execute("SELECT id, nombre, apellido FROM encargado")
    encargados = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('administrador/seleccionarEncargado.html', encargados=encargados)
#-------------------------------------------------------------------
#                       VER PROPIEDADES
#-------------------------------------------------------------------
@app.route('/ver_propiedades')
def ver_propiedades():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM propiedad")  # o filtrá por encargado si lo necesitás
    propiedades = cursor.fetchall()
    conn.close()
    return render_template('administrador/ver_propiedades.html', propiedades=propiedades)
#-------------------------------------------------------------------
#                       EDITAR PERFIL
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
#           AGREGAR ENCARGADO
# ----------------------------------------
@app.route('/agregar_encargado')
def agregar_encargado():
    # Podemos validar que sea administrador también
    if session.get('usuario_tipo') != 'administrador':
        flash("Acceso no autorizado.")
        return redirect(url_for('login'))
    return render_template('administrador/agregarEncargado.html')

# ----------------------------------------
#           REGISTRO ENCARGADO
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
#          REGISTRO ADMINISTRADOR
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
#                   CHAT
# ----------------------------------------
@app.route('/chat')
def chat():
    if 'usuario_id' not in session:
        return redirect(url_for('login_usuario'))  
    return render_template('usuario/chat.html')
#-----------------------------------------
#       LOGIN DE LOS TRES USUARIOS
#-----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('login'))
            else:
                intentos_info = {'intentos': 0, 'bloqueado_hasta': None}

        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
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

                    return redirect(url_for('sesion_iniciada'))

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
@app.route('/sesion_iniciada')
def sesion_iniciada():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('usuario/sesionIniciada.html', 
                           tipo=session.get('usuario_tipo'),
                           nombre=session.get('usuario_nombre'))

#-----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
