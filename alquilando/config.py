import os

class Config:
    SECRET_KEY = 'clave_secreta_segura'
    UPLOAD_FOLDER = os.path.join('static', 'img')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'avif'}

    # Configuración PostgreSQL
    DB_HOST = "localhost"
    DB_NAME = "db_init_alquilando"
    DB_USER = "postgres"
    DB_PASSWORD = "adrianingedos"

    # Configuración Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'adrian.sambido40911@alumnos.info.unlp.edu.ar'
    MAIL_PASSWORD = 'ipnp eklu ukdg bxdu'
    MAIL_DEFAULT_SENDER = 'adrian.sambido40911@alumnos.info.unlp.edu.ar'
