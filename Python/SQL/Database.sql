-- CREATE DATABASE clinica;
-- \c clinica

-- Eliminar las tablas si ya existen
DROP TABLE IF EXISTS Diagnostico_Examen CASCADE;
DROP TABLE IF EXISTS Diagnostico CASCADE;
DROP TABLE IF EXISTS Enfermedad CASCADE;
DROP TABLE IF EXISTS Orden_examen CASCADE;
DROP TABLE IF EXISTS Examen CASCADE;
DROP TABLE IF EXISTS Paciente CASCADE;
DROP TABLE IF EXISTS Cama CASCADE;
DROP TABLE IF EXISTS Habitacion CASCADE;
DROP TABLE IF EXISTS Medico CASCADE;


CREATE TABLE Medico(
    medico_id SERIAL PRIMARY KEY,
    medico_name VARCHAR(100) NOT NULL
);

CREATE TABLE Habitacion(
    habitacion_id SERIAL PRIMARY KEY,
    habitacion_name VARCHAR(50) NOT NULL,
    habitacion_capacidad INT CHECK (habitacion_capacidad > 0)
);

CREATE TABLE Examen(
    examen_id SERIAL PRIMARY KEY,
    examen_name VARCHAR(100) NOT NULL
);

CREATE TABLE Enfermedad(
    enfermedad_id SERIAL PRIMARY KEY,
    enfermedad_name VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE Cama(
    cama_id SERIAL PRIMARY KEY,
    habitacion_id INT NOT NULL REFERENCES habitacion(habitacion_id),
    estado VARCHAR(10) NOT NULL CHECK (estado IN ('libre', 'ocupada'))
);

CREATE TABLE Paciente(
    paciente_rut VARCHAR(12) PRIMARY KEY,
    paciente_name VARCHAR(100) NOT NULL,
    cama_id INT REFERENCES cama(cama_id),
    medico_id INT REFERENCES medico(medico_id),
    enfermedad_id INT REFERENCES enfermedad(enfermedad_id)
);

CREATE TABLE Orden_examen(
    orden_id SERIAL PRIMARY KEY,
    paciente_rut VARCHAR(12) NOT NULL REFERENCES paciente(paciente_rut) ON DELETE CASCADE,
    medico_id INT NOT NULL REFERENCES medico(medico_id),
    examen_id INT NOT NULL REFERENCES examen(examen_id),
    fecha DATE NOT NULL,
    enfermedad_id INT REFERENCES enfermedad(enfermedad_id)
);

CREATE TABLE Diagnostico(
    diagnostico_id SERIAL PRIMARY KEY,
    paciente_rut VARCHAR(12) NOT NULL REFERENCES paciente(paciente_rut) ON DELETE CASCADE,
    medico_id INT NOT NULL REFERENCES medico(medico_id),
    enfermedad_id INT NOT NULL REFERENCES enfermedad(enfermedad_id),
    fecha DATE NOT NULL
);

CREATE TABLE Diagnostico_Examen(
    diagnostico_id INT REFERENCES Diagnostico(diagnostico_id) ON DELETE CASCADE,
    examen_id INT REFERENCES Examen(examen_id),
    PRIMARY KEY (diagnostico_id, examen_id)
);


INSERT INTO Medico (medico_name) VALUES
('Dr. Gregory House'),
('Dr. Eric Foreman'),
('Dr. Allison Cameron'),
('Dr. Robert Chase'),
('Dr. Remy Hadley'),
('Dr. Chris Taub'),
('Dr. Lawrence Kutner'),
('Dr. Jeffrey Cole'),
('Dr. Jessica Adams'),
('Dr. James Wilson');  

INSERT INTO Habitacion (habitacion_name, habitacion_capacidad) VALUES
('Habitación 101', 2),
('Habitación 102', 2),
('Habitación 103', 2),
('Habitación 201', 2),
('Habitación 202', 2),
('Habitación 203', 2),
('Habitación 301', 2),
('Habitación 302', 2),
('Habitación 303', 2),
('Habitación 304', 2),
('Habitación 401', 2),
('Habitación 402', 2),
('Habitación 403', 2),
('Habitación 404', 2),
('Habitación 405', 2);

INSERT INTO Examen (examen_name) VALUES
('Examen de sangre'),
('Radiografía de tórax'),
('Ultrasonido abdominal'),
('Tomografía computarizada'),
('Prueba de COVID-19'),
('Electrocardiograma'),
('Examen de orina'),
('Prueba de función pulmonar'),
('Examen de colesterol'),
('Prueba de embarazo'),
('Colonoscopía'),
('Ecografía renal'),
('Resonancia magnética cerebral'),
('Angiografía'),
('Espirometría'),
('Radiografía de articulaciones');


INSERT INTO Enfermedad (enfermedad_name, descripcion) VALUES
('Alergia al polvo', 'Reacción alérgica a partículas de polvo'),
('Hipotensión', 'Baja presión arterial'),
('EPOC', 'Enfermedad pulmonar obstructiva crónica'),
('Artritis', 'Inflamación de las articulaciones'),
('Cáncer de colon', 'Cáncer que afecta el colon'),
('Asma', 'Trastorno respiratorio crónico'),
('Diabetes', 'Enfermedad metabólica caracterizada por niveles elevados de glucosa'),
('Trombosis', 'Formación de coágulos sanguíneos'),
('Migraña', 'Dolores de cabeza recurrentes y fuertes'),
('Hipertensión', 'Presión arterial alta'),
('Insuficiencia renal', 'Disminución de la función renal'),
('Covid-19', 'Enfermedad respiratoria causada por el virus SARS-CoV-2'),
('Neumonía', 'Inflamación de los pulmones'),
('Cáncer de pulmón', 'Cáncer que afecta los pulmones'),
('Infarto de miocardio', 'Daño al músculo cardíaco debido a la obstrucción de las arterias coronarias'),
('Accidente cerebrovascular (ACV)', 'Interrupción del flujo sanguíneo al cerebro, provocando daño cerebral'),
('Insuficiencia hepática', 'Disminución grave de la función hepática');

INSERT INTO Cama (habitacion_id, estado) VALUES
(1, 'ocupada'),
(2, 'ocupada'),
(3, 'ocupada'),
(4, 'ocupada'),
(5, 'ocupada'),
(6, 'ocupada'),
(7, 'ocupada'),
(8, 'ocupada'),
(9, 'ocupada'),
(10, 'ocupada'),
(11, 'libre'),
(12, 'libre'),
(13, 'libre'),
(14, 'libre'),
(15, 'libre');


INSERT INTO Paciente (paciente_rut, paciente_name, cama_id, medico_id, enfermedad_id) VALUES
('43827194-7', 'Italo Lazcano Castro', 1, 1, 1),
('10839275-2', 'Sebastián Andrés Muñoz Vásquez', 2, 2, 2),
('93284756-9', 'Reinero Jose Quiroz Escobar', 3, 3, 3),
('71628493-0', 'Patricio Orlando Romo Ovalle', 4, 4, 4),
('58291736-4', 'Luis Edwards Tapia Contreras', 5, 5, 5),
('29481637-5', 'Elizabeth Nunez Andrade', 6, 6, 6),
('37482910-3', 'Andrés Sebastián Vásquez Muñoz', 7, 7, 8),
('86529173-8', 'Jose Reinero Escobar Quiroz', 8, 8, 9),
('71593824-1', 'Orlando Patricio Ovalle Romo', 9, 1, 11),
('39182046-6', 'Edwards Luis Contreras Tapia', 10, 2, 12);




INSERT INTO Orden_examen (paciente_rut, medico_id, examen_id, fecha, enfermedad_id) VALUES
('43827194-7', 1, 1, '2025-04-10', 1),   
('10839275-2', 2, 1, '2025-04-11', 2),   
('93284756-9', 3, 3, '2025-04-12', 3),   
('71628493-0', 4, 2, '2025-04-13', 4),   
('58291736-4', 5, 4, '2025-04-14', 5),   
('29481637-5', 6, 5, '2025-04-15', 6),   
('37482910-3', 7, 6, '2025-04-16', 8),   
('86529173-8', 8, 7, '2025-04-17', 9),   
('71593824-1', 1, 9, '2025-04-18', 11), 
('39182046-6', 2, 1, '2025-04-19', 12);



INSERT INTO Diagnostico (diagnostico_id, paciente_rut, medico_id, enfermedad_id, fecha) VALUES
(1, '43827194-7', 1, 1, '2025-04-10'),
(2, '10839275-2', 2, 2, '2025-04-11'),
(3, '93284756-9', 3, 3, '2025-04-12'),
(4, '71628493-0', 4, 4, '2025-04-13'),
(5, '58291736-4', 5, 5, '2025-04-14'),
(6, '29481637-5', 6, 6, '2025-04-15'),
(7, '37482910-3', 7, 8, '2025-04-16'),
(8, '86529173-8', 8, 9, '2025-04-17'),
(9, '71593824-1', 1, 11, '2025-04-18'),
(10, '39182046-6', 2, 12, '2025-04-19');

INSERT INTO Diagnostico_Examen (diagnostico_id, examen_id) VALUES
(1, 1),
(1, 8),
(2, 6),
(2, 1),
(3, 15),
(3, 2),
(4, 16),
(4, 1),
(5, 11),
(5, 1),
(6, 15),
(6, 8),
(7, 1),
(7, 7),
(7, 9),
(8, 14),
(8, 1),
(9, 12),
(9, 7),
(10, 5),
(10, 2);
