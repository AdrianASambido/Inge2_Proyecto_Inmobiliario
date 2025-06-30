from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

from ..db import obtener_conexion
from ..utils import allowed_file
from ..config import Config

admin_bp = Blueprint('admin', __name__)

#-------------------------------------------------------------------
@admin_bp.route('/menuAdministrador')
def menu_administrador():
    return render_template('administrador/menuAdministrador.html')

#-------------------------------------------------------------------
#                   BUSCAR PROPIEDAD
#-------------------------------------------------------------------
@admin_bp.route('/buscar_propiedad', methods=['GET', 'POST'])
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
@admin_bp.route('/editar_propiedad/<int:propiedad_id>', methods=['GET', 'POST'])
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
                ruta = os.path.join(Config.UPLOAD_FOLDER, nombre)
                img.save(ruta)
                ruta_rel = os.path.join("img", nombre).replace("\\", "/")
                cursor.execute(
                    "INSERT INTO imagen (url, propiedad_id) VALUES (%s, %s)",
                    (ruta_rel, propiedad_id)
                )

        conexion.commit()
        flash("Propiedad actualizada correctamente.")
        return redirect(url_for('admin.buscar_propiedad'))

    # GET: cargar datos actuales de la propiedad
    cursor.execute("""
        SELECT calle, numero, piso, dpto, ciudad, provincia, descripcion
        FROM propiedad
        WHERE id = %s
    """, (propiedad_id,))
    datos = cursor.fetchone()

    if not datos:
        flash("Propiedad no encontrada.")
        return redirect(url_for('admin.buscar_propiedad'))

    campos = ['calle', 'numero', 'piso', 'dpto', 'ciudad', 'provincia', 'descripcion']
    propiedad = dict(zip(campos, datos))

    # cargar imágenes actuales
    cursor.execute("SELECT id, url FROM imagen WHERE propiedad_id = %s", (propiedad_id,))
    imagenes = cursor.fetchall()

    return render_template('administrador/editarPropiedad.html', propiedad_id=propiedad_id, propiedad=propiedad, imagenes=imagenes)

#-------------------------------------------------------------------
#               DAR DE ALTA PROPIEDAD
#-------------------------------------------------------------------
@admin_bp.route('/darDeAltaPropiedad', methods=['GET', 'POST'])
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
            'calle': request.form.get('direccion', ''),
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
            # Ensure the upload directory exists
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            ruta_completa = os.path.join(Config.UPLOAD_FOLDER, nombre_archivo)
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
        return redirect(url_for('admin.menu_administrador'))

    return render_template('administrador/darDeAltaPropiedad.html', encargados=encargados)

#-------------------------------------------------------------------
#           LISTADO DE PROPIEDADES POR ENCARGADO
#-------------------------------------------------------------------
@admin_bp.route('/ver_propiedades_encargado', methods=['GET', 'POST'])
def ver_propiedades_encargado():
    conn = obtener_conexion()
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
@admin_bp.route('/ver_propiedades')
def ver_propiedades():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM propiedad")
    propiedades = cursor.fetchall()
    conn.close()
    return render_template('administrador/ver_propiedades.html', propiedades=propiedades)

# ----------------------------------------
#           AGREGAR ENCARGADO
# ----------------------------------------
@admin_bp.route('/agregar_encargado')
def agregar_encargado():
    if session.get('usuario_tipo') != 'administrador':
        flash("Acceso no autorizado.")
        return redirect(url_for('auth.login'))
    return render_template('administrador/agregarEncargado.html')
