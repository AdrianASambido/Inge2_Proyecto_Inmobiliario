# 🏡 Alquilando

**Alquilando** is a web application developed as part of the Software Engineering 2 course at the Facultad de Informática, UNLP. The project simulates a real-world platform for managing property rentals, connecting landlords and tenants in a secure and organized environment.

## 🚀 Features

*   **User Authentication:** Secure login and registration for landlords and tenants.
*   **Property Management:** Landlords can list, update, and manage their properties.
*   **Property Search:** Tenants can search and filter properties based on various criteria.
*   **Rental Agreements:** Tools for managing rental contracts and agreements.
*   **Messaging System:** Communication platform between landlords and tenants.

## 🛠️ Technologies Used

*   **Backend:** Python, Flask
*   **Database:** SQLite (for development), PostgreSQL (for production)
*   **Frontend:** HTML, CSS, JavaScript
*   **Deployment:** (To be specified, e.g., Docker, Heroku, AWS)

## ⚙️ Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/alquilando.git
    cd alquilando
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Initialize the database:**
    ```bash
    # Assuming you have a script or Flask command for this
    flask init-db
    ```
5.  **Run the application:**

    To run the application, navigate to the root directory of the project (`C:\Facultad_Informatica\Proyecto_Inmobiliario`) and execute:
    ```bash
    python run.py
    ```
    If Flask is not globally installed, ensure you activate the virtual environment first. From the `alquilando` directory:
    ```bash
    cd alquilando
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On macOS/Linux
    cd ..
    python run.py
    ```

## 💡 Usage

Once the application is running, navigate to `http://127.0.0.1:5000` (or `http://localhost:5000`) in your web browser.

*   **Landlords:** Register an account, log in, and start listing your properties.
*   **Tenants:** Register an account, log in, and browse available properties.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
