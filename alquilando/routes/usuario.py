from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2

from ..db import obtener_conexion

usuario_bp = Blueprint('usuario', __name__)

#-------------------------------------------
#           Página principal
#-------------------------------------------
@usuario_bp.route('/')
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

#------------------------------------------------
#       VER DETALLE DE LAS PROPIEDADES
#------------------------------------------------
@usuario_bp.route('/detalle_propiedad/<int:propiedad_id>')
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
#                       EDITAR PERFIL
#-------------------------------------------------------------------
@usuario_bp.route('/editarPerfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario_id' not in session or 'usuario_tipo' not in session:
        flash("Primero debes iniciar sesión.")
        return redirect(url_for('auth.login'))

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
        return redirect(url_for('auth.login'))

    conn = obtener_conexion()
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
        return redirect(url_for('usuario.editar_perfil'))

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
        return redirect(url_for('auth.sesion_iniciada'))

# ----------------------------------------
#                   CHAT
# ----------------------------------------
@usuario_bp.route('/chat')
def chat():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))  
    return render_template('usuario/chat.html')
