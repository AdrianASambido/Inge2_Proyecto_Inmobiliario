import re
import os
from werkzeug.utils import secure_filename
from .config import Config

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def es_contraseña_segura(password):
    return (len(password) >= 6 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))

def es_email_valido(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def solo_letras(texto):
    return re.fullmatch(r'[A-Za-z]{1,30}', texto)

def solo_numeros(texto, min_len, max_len):
    return texto.isdigit() and min_len <= len(texto) <= max_len
