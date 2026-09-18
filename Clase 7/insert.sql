-- Datos de prueba para MariaDB (base de datos "negocio")

-- ============ PRODUCTOS ============
INSERT INTO productos (id_producto, codigo, descripcion, precio_compra, precio_venta, stock, estado, fecha_creacion) VALUES
(1, 'P001', 'Teclado mecanico', 50000, 80000, 20, 1, '2026-01-05'),
(2, 'P002', 'Mouse inalambrico', 25000, 45000, 35, 1, '2026-01-05'),
(3, 'P003', 'Monitor 24 pulgadas', 350000, 520000, 10, 1, '2026-01-10'),
(4, 'P004', 'Diadema con microfono', 40000, 70000, 15, 1, '2026-01-10'),
(5, 'P005', 'Webcam full HD', 60000, 95000, 12, 1, '2026-01-15'),
(6, 'P006', 'Disco SSD 500GB', 120000, 180000, 25, 1, '2026-01-15'),
(7, 'P007', 'Memoria RAM 8GB', 90000, 130000, 30, 1, '2026-01-20'),
(8, 'P008', 'Mousepad grande', 10000, 20000, 50, 1, '2026-01-20'),
(9, 'P009', 'Cable HDMI 2m', 8000, 15000, 40, 1, '2026-01-25'),
(10, 'P010', 'Base refrigerante portatil', 45000, 75000, 18, 1, '2026-01-25');

-- ============ CLIENTES ============
INSERT INTO clientes (id_cliente, nombre_completo, documento, email, telefono, direccion, estado, fecha_registro) VALUES
(1, 'Juan Carlos Benitez', '2345678', 'juan.benitez@correo.com.py', '+595981234567', 'Av. Mariscal Lopez 1450, Asuncion', 1, '2026-01-06'),
(2, 'Maria Fernanda Gonzalez', '2876543', 'maria.gonzalez@correo.com.py', '+595982345678', 'Av. Eusebio Ayala 2380, Asuncion', 1, '2026-01-07'),
(3, 'Carlos Alberto Ramirez', '3124589', 'carlos.ramirez@correo.com.py', '+595983456789', 'Av. Espana 980, Asuncion', 1, '2026-01-08'),
(4, 'Ana Beatriz Torres', '3567890', 'ana.torres@correo.com.py', '+595984567890', 'Av. San Martin 720, Asuncion', 1, '2026-01-09'),
(5, 'Luis Alberto Martinez', '4012345', 'luis.martinez@correo.com.py', '+595985678901', 'Av. Irrazabal 1560, Encarnacion', 1, '2026-01-10'),
(6, 'Sofia Elizabeth Castro', '4234567', 'sofia.castro@correo.com.py', '+595986789012', 'Av. Bernardino Caballero 430, Ciudad del Este', 1, '2026-01-12'),
(7, 'Pedro Andres Hernandez', '4678901', 'pedro.hernandez@correo.com.py', '+595987890123', 'Av. Adrian Jara 1150, Ciudad del Este', 1, '2026-01-14'),
(8, 'Laura Daniela Diaz', '4987654', 'laura.diaz@correo.com.py', '+595988901234', 'Av. Jose Gaspar Rodriguez de Francia 610, Luque', 1, '2026-01-16');

-- ============ VENTAS ============
INSERT INTO ventas (id_venta, id_cliente, total, subtotal, descuento, iva, fecha_venta) VALUES
(1, 1, 190400, 160000, 0, 30400, '2026-02-01'),
(2, 2, 61750, 45000, 5000, 21750, '2026-02-02'),
(3, 3, 987700, 830000, 0, 157700, '2026-02-03'),
(4, 4, 83300, 70000, 0, 13300, '2026-02-04'),
(5, 5, 678300, 580000, 10000, 108300, '2026-02-05'),
(6, 6, 249900, 210000, 0, 39900, '2026-02-06'),
(7, 7, 196350, 165000, 0, 31350, '2026-02-07'),
(8, 8, 23800, 20000, 0, 3800, '2026-02-08'),
(9, 1, 33320, 30000, 2000, 5320, '2026-02-09'),
(10, 2, 89250, 75000, 0, 14250, '2026-02-10'),
(11, 3, 618800, 520000, 0, 98800, '2026-02-11'),
(12, 4, 154700, 130000, 0, 24700, '2026-02-12'),
(13, 5, 113050, 95000, 0, 18050, '2026-02-13'),
(14, 6, 232050, 195000, 0, 37050, '2026-02-14'),
(15, 7, 17850, 15000, 0, 2850, '2026-02-15');

-- ============ DETALLE_VENTAS ============
INSERT INTO detalle_ventas (id_detalle, id_venta, id_producto, cantidad, precio_unitario, subtotal, descuento, iva) VALUES
(1, 1, 1, 2, 80000, 160000, 0, 30400),
(2, 2, 2, 1, 45000, 45000, 5000, 21750),
(3, 3, 3, 1, 520000, 520000, 0, 98800),
(4, 3, 6, 1, 180000, 180000, 0, 34200),
(5, 3, 7, 1, 130000, 130000, 0, 24700),
(6, 4, 4, 1, 70000, 70000, 0, 13300),
(7, 5, 3, 1, 520000, 520000, 0, 98800),
(8, 5, 8, 3, 20000, 60000, 10000, 9500),
(9, 6, 6, 1, 180000, 180000, 0, 34200),
(10, 6, 9, 2, 15000, 30000, 0, 5700),
(11, 7, 4, 1, 70000, 70000, 0, 13300),
(12, 7, 5, 1, 95000, 95000, 0, 18050),
(13, 8, 8, 1, 20000, 20000, 0, 3800),
(14, 9, 9, 2, 15000, 30000, 2000, 5320),
(15, 10, 10, 1, 75000, 75000, 0, 14250),
(16, 11, 3, 1, 520000, 520000, 0, 98800),
(17, 12, 7, 1, 130000, 130000, 0, 24700),
(18, 13, 5, 1, 95000, 95000, 0, 18050),
(19, 14, 6, 1, 180000, 180000, 0, 34200),
(20, 14, 9, 1, 15000, 15000, 0, 2850),
(21, 15, 9, 1, 15000, 15000, 0, 2850);
