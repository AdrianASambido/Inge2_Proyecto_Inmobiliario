-- Tabla: administrador
CREATE TABLE administrador (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);

-- Tabla: cliente
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    dni VARCHAR(20),
    telefono VARCHAR(20),
    numero_tarjeta VARCHAR(20),
    nacionalidad VARCHAR(50)
);

-- Tabla: encargado
CREATE TABLE encargado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);

-- Tabla: propiedad
CREATE TABLE propiedad (
    id SERIAL PRIMARY KEY,
    dpto VARCHAR(10),
    piso INTEGER,
    numero INTEGER,
    calle VARCHAR(100),
    cantidad_ambientes INTEGER,
    petfriendly BOOLEAN,
    listada BOOLEAN,
    encargado_id INTEGER REFERENCES encargado(id)
);

-- Tabla: imagen
CREATE TABLE imagen (
    id SERIAL PRIMARY KEY,
    url TEXT,
    propiedad_id INTEGER REFERENCES propiedad(id)
);

-- Tabla: opinion
CREATE TABLE opinion (
    id SERIAL PRIMARY KEY,
    comentario TEXT,
    cantidad_estrellas INTEGER,
    cliente_id INTEGER REFERENCES cliente(id),
    propiedad_id INTEGER REFERENCES propiedad(id)
);

-- Tabla: reserva
CREATE TABLE reserva (
    id SERIAL PRIMARY KEY,
    fecha_in DATE,
    fecha_out DATE,
    cliente_id INTEGER REFERENCES cliente(id),
    propiedad_id INTEGER REFERENCES propiedad(id)
);

-- Tabla: pago
CREATE TABLE pago (
    id SERIAL PRIMARY KEY,
    reserva_id INTEGER REFERENCES reserva(id),
    monto DECIMAL(10, 2),
    completado BOOLEAN
);
