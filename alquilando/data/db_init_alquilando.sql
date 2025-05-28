-- Crear tabla Administrador
CREATE TABLE Administrador (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crear tabla Cliente
CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crear tabla Encargado
CREATE TABLE Encargado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crear tabla Propiedad
CREATE TABLE Propiedad (
    id SERIAL PRIMARY KEY,
    dpto VARCHAR(20),
    piso VARCHAR(10),
    numero VARCHAR(10),
    calle VARCHAR(100),
    cantidad_ambientes INT CHECK (cantidad_ambientes >= 1),
    petfriendly BOOLEAN DEFAULT FALSE,
    listada BOOLEAN DEFAULT TRUE,
    encargado_id INT REFERENCES Encargado(id)
);

-- Crear tabla Reserva
CREATE TABLE Reserva (
    id SERIAL PRIMARY KEY,
    fecha_in DATE NOT NULL,
    fecha_out DATE NOT NULL,
    cliente_id INT NOT NULL REFERENCES Cliente(id),
    propiedad_id INT NOT NULL REFERENCES Propiedad(id),
    CONSTRAINT fechas_validas CHECK (fecha_in < fecha_out)
);

-- Crear tabla Pago
CREATE TABLE Pago (
    id SERIAL PRIMARY KEY,
    reserva_id INT NOT NULL REFERENCES Reserva(id) ON DELETE CASCADE,
    monto NUMERIC(10,2) NOT NULL CHECK (monto > 0),
    completado BOOLEAN DEFAULT FALSE
);

-- Crear tabla Opinion
CREATE TABLE Opinion (
    id SERIAL PRIMARY KEY,
    comentario TEXT,
    cantidad_estrellas INT NOT NULL CHECK (cantidad_estrellas BETWEEN 1 AND 5),
    cliente_id INT NOT NULL REFERENCES Cliente(id),
    propiedad_id INT NOT NULL REFERENCES Propiedad(id)
);

-- Crear tabla Imagen
CREATE TABLE Imagen (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    propiedad_id INT NOT NULL REFERENCES Propiedad(id)
);








-- Insertar administradores
INSERT INTO Administrador (id, nombre, apellido, email, password) VALUES
(1, 'Lucía', 'Gómez', 'lucia@admin.com', 'admin123'),
(2, 'Carlos', 'Pérez', 'carlos@admin.com', 'admin456');

-- Insertar clientes
INSERT INTO Cliente (id, nombre, apellido, email, password) VALUES
(1, 'María', 'López', 'maria@cliente.com', 'clave1'),
(2, 'Juan', 'Martínez', 'juan@cliente.com', 'clave2');

-- Insertar encargados
INSERT INTO Encargado (id, nombre, apellido, email, password) VALUES
(1, 'Ana', 'Ramírez', 'ana@encargado.com', 'enc123'),
(2, 'Pedro', 'Sosa', 'pedro@encargado.com', 'enc456');

-- Insertar propiedades
INSERT INTO Propiedad (id, dpto, piso, numero, calle, cantidad_ambientes, petfriendly, listada, encargado_id) VALUES
(1, 'A', 3, 101, 'Calle Falsa', 2, true, true, 1),
(2, 'B', 1, 202, 'Av. Siempre Viva', 3, false, true, 2);

-- Insertar reservas
INSERT INTO Reserva (id, fecha_in, fecha_out, cliente_id, propiedad_id) VALUES
(1, '2025-06-01', '2025-06-07', 1, 1),
(2, '2025-07-10', '2025-07-15', 2, 2);

-- Insertar pagos
INSERT INTO Pago (id, reserva_id, monto, completado) VALUES
(1, 1, 50000.00, true),
(2, 2, 45000.00, false);

-- Insertar opiniones
INSERT INTO Opinion (id, comentario, cantidad_estrellas, cliente_id, propiedad_id) VALUES
(1, 'Muy linda propiedad, todo limpio.', 5, 1, 1),
(2, 'Buena ubicación pero algo ruidosa.', 3, 2, 2);

-- Insertar imágenes
INSERT INTO Imagen (id, url, propiedad_id) VALUES
(1, 'https://ejemplo.com/imagen1.jpg', 1),
(2, 'https://ejemplo.com/imagen2.jpg', 1),
(3, 'https://ejemplo.com/imagen3.jpg', 2);
