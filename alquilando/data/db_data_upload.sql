-- Datos: administrador
INSERT INTO administrador (id, nombre, apellido, email, password) VALUES
(1, 'Lucía', 'Gómez', 'lucia@admin.com', 'admin123'),
(2, 'Carlos', 'Pérez', 'carlos@admin.com', 'admin456');

-- Datos: cliente
INSERT INTO cliente (id, nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad) VALUES
(1, 'María', 'López', 'maria@cliente.com', 'clave1', NULL, NULL, NULL, NULL),
(2, 'Juan', 'Martínez', 'juan@cliente.com', 'clave2', NULL, NULL, NULL, NULL),
(3, 'Adrian alejandro', 'Sambido', 'adriinform2021@gmail.com', 'clave3', NULL, NULL, NULL, NULL),
(4, 'Mariel', 'Ajala', 'mariela@cliente.com', 'clave4', NULL, NULL, NULL, NULL),
(5, 'Nicolás', 'Viviers', 'nicolas@cliente.com', 'clave5', NULL, NULL, NULL, NULL),
(6, 'Alejandro', 'Pozati', 'alejandro@cliente.com', 'clave6', '18222555', '-1', '3333555566667776', 'Argentino'),
(7, 'Pato', 'Verón', 'pato@cliente.com', 'clave', '6666666', '2222222', '55451215', 'Paraguayo');

-- Datos: encargado
INSERT INTO encargado (id, nombre, apellido, email, password) VALUES
(1, 'Ana', 'Ramírez', 'ana@encargado.com', 'enc123'),
(2, 'Pedro', 'Sosa', 'pedro@encargado.com', 'enc456');

-- Datos: propiedad
INSERT INTO propiedad (id, dpto, piso, numero, calle, cantidad_ambientes, petfriendly, listada, encargado_id) VALUES
(1, 'A', 3, 101, 'Calle Falsa', 2, TRUE, TRUE, 1),
(2, 'B', 1, 202, 'Av. Siempre Viva', 3, FALSE, TRUE, 2);

-- Datos: imagen
INSERT INTO imagen (id, url, propiedad_id) VALUES
(1, 'https://ejemplo.com/imagen1.jpg', 1),
(2, 'https://ejemplo.com/imagen2.jpg', 1),
(3, 'https://ejemplo.com/imagen3.jpg', 2);

-- Datos: opinion
INSERT INTO opinion (id, comentario, cantidad_estrellas, cliente_id, propiedad_id) VALUES
(1, 'Muy linda propiedad, todo limpio.', 5, 1, 1),
(2, 'Buena ubicación pero algo ruidosa.', 3, 2, 2);

-- Datos: reserva
INSERT INTO reserva (id, fecha_in, fecha_out, cliente_id, propiedad_id) VALUES
(1, '2025-06-01', '2025-06-07', 1, 1),
(2, '2025-07-10', '2025-07-15', 2, 2);

-- Datos: pago
INSERT INTO pago (id, reserva_id, monto, completado) VALUES
(1, 1, 50000.00, TRUE),
(2, 2, 45000.00, FALSE);
