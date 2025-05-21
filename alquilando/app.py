from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import psycopg2 

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Configuración de conexión PostgreSQL
DB_HOST = "localhost"
DB_NAME = "db_init_alquilando"
DB_USER = "postgres"
DB_PASSWORD = "adrianingedos"

# 👉 Ruta principal que muestra la página de inicio (con logo, botones, etc.)


@app.route('/')
def pagina_inicio():
    hoy = date.today().isoformat()  # formato YYYY-MM-DD
    return render_template('inicio.html', fecha_actual=hoy)

#@app.route('/')
#def pagina_inicio():
#    return render_template('inicio.html')

# 👉 Ruta para el login de encargados (formulario que ya tenés en loginEncargado.html)
@app.route('/loginEncargado', methods=['GET'])
def login_form():
    return render_template('loginEncargado.html')

# 👉 Ruta que procesa el login del encargado
@app.route('/loginEncargado', methods=['POST'])
@app.route('/loginUsuario', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cliente WHERE email = %s AND password = %s', (email, password))
            cliente = cursor.fetchone()

            if cliente:
                nombre = cliente[1]
                apellido = cliente[2]
                return f"Bienvenido {nombre} {apellido}!"
            else:
                flash("Email o contraseña incorrectos.")
                return redirect(url_for('login_usuario'))

        except Exception as e:
            print(f"[ERROR] Error al iniciar sesión de usuario: {e}")
            flash("Error en el servidor.")
            return redirect(url_for('login_usuario'))
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('loginUsuario.html')
@app.route('/registroUsuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
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
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('registroUsuario.html')

def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    print(f"[DEBUG] Email ingresado: '{email}'")
    print(f"[DEBUG] Password ingresado: '{password}'")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM encargado WHERE email = %s', (email,))
        usuario_por_email = cursor.fetchone()
        print(f"[DEBUG] Usuario encontrado por email: {usuario_por_email}")
        
        if usuario_por_email:
            password_almacenada = usuario_por_email[4] if len(usuario_por_email) > 4 else None
            print(f"[DEBUG] Contraseña almacenada: '{password_almacenada}'")
            print(f"[DEBUG] ¿Coinciden contraseñas?: {password == password_almacenada}")
            
            query = 'SELECT * FROM encargado WHERE email = %s AND password = %s'
            cursor.execute(query, (email, password))
            encargado = cursor.fetchone()
            print(f"[DEBUG] Resultado final de la consulta: {encargado}")
            
            if encargado:
                nombre = encargado[1]
                apellido = encargado[2]
                return f"Bienvenido {nombre} {apellido}!"
            else:
                flash("Contraseña incorrecta.")
                return redirect(url_for('login_form'))
        else:
            flash("El email no existe en nuestra base de datos.")
            return redirect(url_for('login_form'))

    except Exception as e:
        print(f"[ERROR] Fallo de conexión o consulta: {e}")
        flash("Error en el servidor al conectar con la base de datos.")
        return redirect(url_for('login_form'))
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
