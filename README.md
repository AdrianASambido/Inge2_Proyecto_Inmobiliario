# 🏡 Alquilando

**Alquilando** es una aplicación web desarrollada como parte de la materia Ingeniería de Software 2 en la Facultad de Informática, UNLP. El proyecto simula una plataforma real para la gestión de alquileres, conectando propietarios e inquilinos de forma segura y organizada.

## 🚀 Funcionalidades

*   **Autenticación de usuarios:** Registro e inicio de sesión seguro para propietarios e inquilinos.
*   **Gestión de propiedades:** Los propietarios pueden listar, actualizar y administrar sus propiedades.
*   **Búsqueda de propiedades:** Los inquilinos pueden buscar y filtrar propiedades según distintos criterios.
*   **Gestión de contratos:** Herramientas para administrar contratos y acuerdos de alquiler.
*   **Sistema de mensajería:** Comunicación entre propietarios e inquilinos.

## 🛠️ Tecnologías utilizadas

*   **Backend:** Python, Flask
*   **Base de datos:** SQLite (desarrollo), PostgreSQL (producción)
*   **Frontend:** HTML, CSS, JavaScript
*   **Despliegue:** (A definir, ej: Docker, Heroku, AWS)

## ⚙️ Instalación

Para instalar el proyecto localmente, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/your-username/alquilando.git
    cd Proyecto_Inmobiliario
    ```
2.  **Crea y activa el entorno virtual (desde la raíz):**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```
3.  **Instala las dependencias:**
    ```bash
    pip install -r alquilando/requirements.txt
    ```
4.  **Inicializa la base de datos:**
    ```bash
    # Según tu configuración, ejecuta el script SQL o usa un comando Flask
    # Ejemplo:
    psql -U postgres -d db_init_alquilando -f alquilando/data/db_init_alquilando.sql
    ```
5.  **Ejecuta la aplicación (desde la raíz):**
    ```bash
    python run.py
    ```

## 💡 Uso

Una vez que la aplicación esté corriendo, navega a `http://127.0.0.1:5000` (o `http://localhost:5000`) en tu navegador web.

*   **Propietarios:** Registran una cuenta, inician sesión y publican sus propiedades.
*   **Inquilinos:** Registran una cuenta, inician sesión y buscan propiedades disponibles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1.  Haz un fork del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/TuFeature`).
3.  Realiza tus cambios.
4.  Haz commit (`git commit -m 'Agrega una funcionalidad'`).
5.  Haz push a la rama (`git push origin feature/TuFeature`).
6.  Abre un Pull Request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📧 Contacto

Por cualquier consulta, escribe a [your-email@example.com](mailto:your-email@example.com).
