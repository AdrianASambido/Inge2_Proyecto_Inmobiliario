from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2

from ..db import obtener_conexion

encargado_bp = Blueprint('encargado', __name__)

#-------------------------------------------------------------------
@encargado_bp.route('/menuEncargado')
def menu_encargado():
    return render_template('encargado/menuEncargado.html')

# -------------------------------------------------------
#               LISTA DE PROPIEDADES
# -------------------------------------------------------
@encargado_bp.route('/listado_propiedades')
def listado_propiedades():
    origen = request.args.get('origen', 'encargado')
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM propiedad")
    propiedades = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('encargado/listadoPropiedades.html', propiedades=propiedades, origen=origen)
