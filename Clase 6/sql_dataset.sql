DROP TABLE IF EXISTS empleados;
CREATE TABLE empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    edad INT,
    departamento VARCHAR(50),
    salario INT,
    fecha_ingreso DATE
);
INSERT INTO empleados (id, nombre, apellido, edad, departamento, salario, fecha_ingreso) VALUES
(1, 'Ana', 'Gómez', 28, 'Administración', 4500000, '2021-03-15'),
(2, 'Luis', 'Martínez', 35, 'Sistemas', 7200000, '2019-07-01'),
(3, 'María', 'López', 24, 'Marketing', 3800000, '2022-11-20'),
(4, 'Carlos', 'Pérez', 41, 'Finanzas', 8500000, '2018-02-10'),
(5, 'Sofía', 'Rodríguez', 30, 'Recursos Humanos', 5000000, '2020-05-05'),
(6, 'Jorge', 'Benítez', 29, 'Sistemas', 6800000, '2021-09-12'),
(7, 'Lucía', 'Fernández', 33, 'Administración', 4700000, '2019-01-25'),
(8, 'Diego', 'Ramírez', 26, 'Marketing', 3900000, '2023-04-18'),
(9, 'Paula', 'Acosta', 38, 'Finanzas', 8200000, '2017-12-03'),
(10, 'Raúl', 'Vera', 45, 'Gerencia', 12000000, '2016-06-30'),
(11, 'Elena', 'Cabrera', 32, 'Sistemas', 7000000, '2020-08-14'),
(12, 'Tomás', 'Rivas', 27, 'Marketing', 3600000, '2022-02-11'),
(13, 'Valeria', 'Ortiz', 34, 'Finanzas', 8100000, '2018-10-22'),
(14, 'Miguel', 'García', 31, 'Sistemas', 6900000, '2021-01-19'),
(15, 'Rocío', 'Mendoza', 29, 'Recursos Humanos', 5200000, '2020-06-07'),
(16, 'Hernán', 'Silva', 40, 'Gerencia', 11500000, '2016-09-12'),
(17, 'Camila', 'Torres', 25, 'Administración', 4300000, '2023-01-03'),
(18, 'Nicolás', 'Franco', 37, 'Sistemas', 7500000, '2019-11-29'),
(19, 'Patricia', 'Ayala', 42, 'Finanzas', 8800000, '2017-04-16'),
(20, 'Gabriel', 'Sosa', 28, 'Marketing', 4000000, '2022-07-21');
