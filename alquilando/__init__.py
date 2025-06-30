from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail
import os

from .config import Config
from .db import obtener_conexion
from .utils import allowed_file, es_contraseña_segura, es_email_valido, solo_letras, solo_numeros

# Import Blueprints
from .routes.auth import auth_bp
from .routes.admin import admin_bp
from .routes.encargado import encargado_bp
from .routes.usuario import usuario_bp

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(encargado_bp)
app.register_blueprint(usuario_bp)

# You might want to keep some general routes here if they don't fit into a specific blueprint,
# or move them to a 'main' or 'general' blueprint.
# For now, the root route will be handled by the 'usuario' blueprint.
