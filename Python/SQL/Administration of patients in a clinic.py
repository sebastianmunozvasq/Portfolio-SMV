import psycopg2

# Conexión a PostgreSQL
def conectar():
    try:
        conexion = psycopg2.connect(
            dbname="clinica",
            user="postgres",
            password="modulo4",
            host="localhost",
            port="5432"
        )
        return conexion
    except Exception as error:
        print("Error al conectar con la base de datos:", error)
        return None


# Submenú para información
def submenu_informacion():
    while True:
        print("\n--- Submenú: Información ---")
        print("1. Ver todos los pacientes")
        print("2. Ver detalle de paciente por RUT")
        print("3. Ver camas disponibles")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": mostrar_pacientes()
        elif opcion == "2": consultar_paciente()
        elif opcion == "3": ver_camas_disponibles()
        elif opcion == "0": break
        else: print("Opción inválida.")

# Submenú para administración médica
def submenu_administracion():
    while True:
        print("\n--- Submenú: Administración Médica ---")
        print("1. Cambiar cama de paciente")
        print("2. Cambiar médico de paciente")
        print("3. Crear camas")
        print("4. Crear habitaciones")
        print("5. Agregar diagnóstico y examen")
        print("6. Agregar paciente")
        print("7. Eliminar paciente")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": cambiar_cama()
        elif opcion == "2": cambiar_medico()
        elif opcion == "3": crear_cama()
        elif opcion == "4": crear_habitacion()
        elif opcion == "5": agregar_examen_diagnostico()
        elif opcion == "6": agregar_paciente()
        elif opcion == "7": eliminar_paciente()
        elif opcion == "0": break
        else: print("Opción inválida.")

# Menú principal
def menu_principal():
    while True:
        print("\n===== SISTEMA DE GESTIÓN CLÍNICA =====")
        print("1. Información")
        print("2. Administración Médica")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": submenu_informacion()  # Llama al submenú de información
        elif opcion == "2": submenu_administracion()  # Llama al submenú de administración médica
        elif opcion == "0":
            print("Sistema desconectado.")
            break
        else:
            print("Opción inválida.")


# Función para mostrar todos los pacientes
def mostrar_pacientes():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            cursor.execute("""
            SELECT p.paciente_rut, p.paciente_name, e.enfermedad_name,
                   m.medico_name, h.habitacion_name
            FROM Paciente p
            JOIN Medico m ON p.medico_id = m.medico_id
            JOIN Cama c ON p.cama_id = c.cama_id
            JOIN Habitacion h ON c.habitacion_id = h.habitacion_id
            LEFT JOIN Diagnostico d ON p.paciente_rut = d.paciente_rut
            LEFT JOIN Enfermedad e ON d.enfermedad_id = e.enfermedad_id;
            """)
            pacientes = cursor.fetchall()

            if not pacientes:
                print("No hay pacientes registrados.")
            else:
                for p in pacientes:
                    print(f"\nRUT: {p[0]} | Nombre: {p[1]} | Enfermedad: {p[2]} | Médico: {p[3]} | Habitación: {p[4]}")
        except Exception as error:
            print("Error al consultar pacientes:", error)
        finally:
            cursor.close()
            conexiondb.close()

# Función para consultar detalle de un paciente por RUT
def consultar_paciente():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            rut = input("Ingrese el RUT del paciente sin puntos y con guión: ")
            # Verificar si el paciente existe
            cursor.execute("SELECT 1 FROM Paciente WHERE paciente_rut = %s", (rut,))
            existe = cursor.fetchone()
            if not existe:
                print(f"No existe un paciente con RUT {rut}")
                return

            cursor.execute("""
                SELECT p.paciente_rut, p.paciente_name, e.enfermedad_name,
                       m.medico_name, h.habitacion_name, c.cama_id,
                       ex.examen_name
                FROM Paciente p
                JOIN Medico m ON p.medico_id = m.medico_id
                JOIN Cama c ON p.cama_id = c.cama_id
                JOIN Habitacion h ON c.habitacion_id = h.habitacion_id
                LEFT JOIN Diagnostico d ON p.paciente_rut = d.paciente_rut
                LEFT JOIN Enfermedad e ON d.enfermedad_id = e.enfermedad_id
                LEFT JOIN Orden_examen oe ON p.paciente_rut = oe.paciente_rut
                LEFT JOIN Examen ex ON oe.examen_id = ex.examen_id
                WHERE p.paciente_rut = %s
                ORDER BY oe.fecha DESC
                LIMIT 1;
            """, (rut,))
            p = cursor.fetchone()

            if p:
                print(f"\nRUT: {p[0]}\nNombre: {p[1]}\nEnfermedad: {p[2]}")
                print(f"Médico tratante: {p[3]}\nHabitación: {p[4]}\nCama: {p[5]}\nÚltimo examen: {p[6]}")
        except Exception as error:
            print("Error al consultar el paciente:", error)
        finally:
            cursor.close()
            conexiondb.close()


# Función para cambiar de cama
def cambiar_cama():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            rut = input("Ingrese el RUT del paciente sin puntos y con guión: ")

            # Verificar si el paciente existe
            cursor.execute("SELECT 1 FROM Paciente WHERE paciente_rut = %s", (rut,))
            existe = cursor.fetchone()
            if not existe:
                print(f"No existe un paciente con RUT {rut}")
                return

            nueva_cama_id = input("Ingrese el ID de la nueva cama: ")

            # Verificar que la cama nueva existe y está libre
            cursor.execute("SELECT estado FROM Cama WHERE cama_id = %s", (nueva_cama_id,))
            cama = cursor.fetchone()

            if not cama:
                print(f"La cama con ID {nueva_cama_id} no existe.")
            elif cama[0] != 'libre':
                print(f"La cama con ID {nueva_cama_id} no está disponible.")
            else:
                # Obtener la cama actual del paciente
                cursor.execute("SELECT cama_id FROM Paciente WHERE paciente_rut = %s", (rut,))
                cama_actual = cursor.fetchone()
                cama_anterior_id = cama_actual[0]

                # Actualizar la cama anterior a libre
                cursor.execute("UPDATE Cama SET estado = 'libre' WHERE cama_id = %s", (cama_anterior_id,))

                # Asignar nueva cama al paciente
                cursor.execute("UPDATE Paciente SET cama_id = %s WHERE paciente_rut = %s", (nueva_cama_id, rut))

                # Marcar nueva cama como ocupada
                cursor.execute("UPDATE Cama SET estado = 'ocupada' WHERE cama_id = %s", (nueva_cama_id,))

                conexiondb.commit()
                print("Cama cambiada correctamente.")
        except Exception as error:
            print("Error al cambiar de cama:", error)
        finally:
            cursor.close()
            conexiondb.close()


# Función para cambiar médico
def cambiar_medico():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            rut = input("Ingrese el RUT del paciente sin puntos y con guión: ")
            # Verificar si existe rut
            cursor.execute("SELECT 1 FROM Paciente WHERE paciente_rut = %s", (rut,))
            existe = cursor.fetchone()
            if not existe:
                print(f"No existe un paciente con RUT {rut}")
                return

            nuevo_medico_id = input("Ingrese el ID del nuevo médico: ")
            # Verificar si existe médico
            cursor.execute("SELECT 1 FROM Medico WHERE medico_id = %s", (nuevo_medico_id,))
            existe = cursor.fetchone()
            if not existe:
                print(f"No existe un médico con ID {nuevo_medico_id}")
                return

            cursor.execute("UPDATE Paciente SET medico_id = %s WHERE paciente_rut = %s", (nuevo_medico_id, rut))
            conexiondb.commit()
            print("Médico actualizado correctamente.")
        except Exception as error:
            print("Error al cambiar de médico:", error)
        finally:
            cursor.close()
            conexiondb.close()


#Función para crear habitación
def crear_habitacion():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            nombre = input("Ingrese el nombre de la habitación: ")
            # Verificar si ya existe una habitación con ese nombre
            cursor.execute("SELECT 1 FROM Habitacion WHERE habitacion_name = %s", (nombre,))
            existe = cursor.fetchone()

            if existe:
                print(f"Ya existe una habitación con el nombre '{nombre}'. Intente con otro nombre.")
                return None

            capacidad = int(input("Capacidad de camas de la habitación: "))
            cursor.execute("""
                INSERT INTO Habitacion (habitacion_name, habitacion_capacidad)
                VALUES (%s, %s)
                RETURNING habitacion_id
            """, (nombre, capacidad))

            habitacion_id = cursor.fetchone()[0]
            conexiondb.commit()
            print(f"Habitación '{nombre}' creada correctamente con ID {habitacion_id}.")


        except Exception as error:
            print("Error al crear habitación:", error)

        finally:
            cursor.close()
            conexiondb.close()

#Función para ver camas disponibles
def ver_camas_disponibles():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            cursor.execute("""
                           SELECT c.cama_id, h.habitacion_id
                           FROM Cama c
                           LEFT JOIN Habitacion h ON c.habitacion_id = h.habitacion_id
                           LEFT JOIN Paciente p ON c.cama_id = p.cama_id
                           WHERE p.paciente_rut IS NULL;
                           """)
            print("Camas disponibles:")
            for row in cursor.fetchall():
                print(f"Cama {row[0]} en habitación {row[1]}")
        except Exception as error:
            print("Error al ver camas disponibles:", error)

        finally:
            cursor.close()
            conexiondb.close()
#Función para crear cama
def crear_cama():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            habitacion_id = int(input("ID de la habitación para asignar camas: "))
            # Verificar si la habitación existe
            cursor.execute("SELECT 1 FROM Habitacion WHERE habitacion_id = %s", (habitacion_id,))
            existe = cursor.fetchone()
            if not existe:
                print(f"No existe una habitación con ID {habitacion_id}.")
                return
            cantidad = int(input("Cantidad de camas a crear: "))

            for _ in range(cantidad):
                cursor.execute("INSERT INTO Cama (habitacion_id, estado) VALUES (%s, 'libre')", (habitacion_id,))
            conexiondb.commit()
            print(f"Se crearon {cantidad} camas para la habitación ID {habitacion_id} correctamente.")

        except Exception as error:
            print("Error al crear camas:", error)

        finally:
            cursor.close()
            conexiondb.close()

#Función para añadir examen a paciente
def agregar_examen_diagnostico():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            paciente_rut = input("Ingrese el RUT del paciente sin puntos y con guión: ")
            # Validar rut
            cursor.execute("SELECT 1 FROM paciente WHERE paciente_rut = %s", (paciente_rut,))
            if not cursor.fetchone():
                print(f"No se encontró al paciente con RUT {paciente_rut}.")
                return
            medico_id = input("Ingrese el ID del médico: ")
            # Validar médico
            cursor.execute("SELECT 1 FROM medico WHERE medico_id = %s", (medico_id,))
            if not cursor.fetchone():
                print(f"No se encontró al médico con ID {medico_id}.")
                return

            # Mostrar enfermedades
            cursor.execute("SELECT enfermedad_id, enfermedad_name FROM enfermedad")
            enfermedades = cursor.fetchall()
            print("\nEnfermedades disponibles:")
            for e in enfermedades:
                print(f"{e[0]}: {e[1]}")

            enfermedad_id = input("\nSeleccione el ID de la enfermedad: ")
            #Validar ID
            cursor.execute("SELECT 1 FROM enfermedad WHERE enfermedad_id = %s", (enfermedad_id,))
            if not cursor.fetchone():
              print("ID de enfermedad inválido.")
              return

            # Sincronizar secuencia
            cursor.execute("""
                SELECT setval('diagnostico_diagnostico_id_seq',
                              (SELECT COALESCE(MAX(diagnostico_id), 1) FROM diagnostico));
            """)

            # Insertar diagnóstico
            cursor.execute("""
                INSERT INTO diagnostico (paciente_rut, medico_id, enfermedad_id, fecha)
                VALUES (%s, %s, %s, CURRENT_DATE)
                RETURNING diagnostico_id
            """, (paciente_rut, medico_id, enfermedad_id))
            diagnostico_id = cursor.fetchone()[0]

            # Mostrar exámenes
            cursor.execute("SELECT examen_id, examen_name FROM examen")
            examenes = cursor.fetchall()
            print("\nExámenes disponibles:")
            for e in examenes:
                print(f"{e[0]}: {e[1]}")

            examen_ids_input = input("\nSeleccione los IDs de los exámenes (separados por coma): ").split(",")

            for examen_id in examen_ids_input:
                examen_id = examen_id.strip()

                # Validar examen
                while True:
                    cursor.execute("SELECT 1 FROM examen WHERE examen_id = %s", (examen_id,))
                    if cursor.fetchone():  # Si el examen es válido
                        cursor.execute(
                            "INSERT INTO diagnostico_examen (diagnostico_id, examen_id) VALUES (%s, %s)",
                            (diagnostico_id, examen_id)
                        )
                        print(f"Examen ID {examen_id} agregado exitosamente.")
                        break  # Salir del ciclo cuando el examen es válido
                    else:
                        print(f"Examen ID inválido: {examen_id} — por favor, ingrese un ID válido.")
                        examen_id = input("Ingrese nuevamente el ID del examen: ").strip()  # Solicitar nuevo examen_id


            conexiondb.commit()

        except Exception as error:
            print("Error al agregar diagnóstico:", error)
        finally:
            cursor.close()
            conexiondb.close()



# Función para agregar pacientes
def agregar_paciente():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            # Pedir los datos al usuario
            rut = input("Ingrese el RUT del paciente sin puntos y con guión: ")
            # Validar si el RUT ya está registrado
            cursor.execute("SELECT paciente_rut FROM Paciente WHERE paciente_rut = %s", (rut,))
            if cursor.fetchone():
                print(f"El paciente con RUT {rut} ya está registrado.")
                return

            nombre = input("Ingrese nombre del paciente: ")
            cama_id = input("Ingrese ID de la cama asignada: ")
            # Validar que la cama esté disponible (estado 'libre')
            cursor.execute("SELECT estado FROM Cama WHERE cama_id = %s", (cama_id,))
            cama = cursor.fetchone()
            if not cama:
                print(f"No existe una cama con ID {cama_id}.")
                return
            if cama[0] != 'libre':
                print(f"La cama con ID {cama_id} no está libre.")
                return

            medico_id = input("Ingrese ID del médico tratante: ")

            # Validar si el médico existe
            cursor.execute("SELECT medico_id FROM Medico WHERE medico_id = %s", (medico_id,))
            if not cursor.fetchone():
                print(f"No existe un médico con ID {medico_id}.")
                return

            # Insertar el paciente en la base de datos
            cursor.execute("""
                           INSERT INTO Paciente (paciente_rut, paciente_name, cama_id, medico_id)
                           VALUES (%s, %s, %s, %s);
                           """, (rut, nombre, cama_id, medico_id))

            # Cambiar el estado de la cama a 'ocupada'
            cursor.execute("UPDATE Cama SET estado = 'ocupada' WHERE cama_id = %s", (cama_id,))

            # Confirmar los cambios
            conexiondb.commit()
            print("Paciente agregado exitosamente.")

        except Exception as error:
            print("Error al agregar paciente:", error)

        finally:
            cursor.close()
            conexiondb.close()

#Función para eliminar paciente
def eliminar_paciente():
    conexiondb = conectar()
    if conexiondb:
        cursor = conexiondb.cursor()
        try:
            rut = input("Ingrese el RUT del paciente a eliminar sin puntos y con guión: ")
            # Validar si el RUT ya está registrado
            cursor.execute("SELECT paciente_rut FROM Paciente WHERE paciente_rut = %s", (rut,))
            if not cursor.fetchone():
                print(f"El paciente con RUT {rut} no está registrado.")
                return
            cursor.execute("DELETE FROM Paciente WHERE paciente_rut = %s", (rut,))
            conexiondb.commit()
            print(f"Paciente con rut {rut} eliminado.")
        except Exception as error:
            print("Error al eliminar paciente:", error)

        finally:
            cursor.close()
            conexiondb.close()



# Ejecución principal
if __name__ == "__main__":
    menu_principal()
