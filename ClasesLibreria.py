import mysql.connector
from mysql.connector import Error
from funciones import *
import getpass

def conexion_BD():
    try:
        conexion = mysql.connector.connect(
            host='127.0.0.1',
            database='biblioteca',
            user='root',
            password='',
            port='3306'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def menu_inicio_sesion():
    conexion = conexion_BD()
    while True:
        borrarPantalla()
        print("\n--- Menú de Inicio ---")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            borrarPantalla()
            correo = input("Correo: ")
            contrasena = getpass.getpass("Contraseña: ")
            privilegio = input("¿Es estudiante, profesor o empleado? ")

            if iniciar_sesion(conexion, correo, contrasena, privilegio):
                if privilegio:
                    if privilegio == "Empleado":
                        menuempleado()
                    elif privilegio in ["Estudiante", "Profesor"]:
                        menu()
                    else:
                        print("Privilegio desconocido. Por favor, contacte al administrador.")
            else:
                print("Usuario, contraseña o privilegio incorrectos. Inténtalo de nuevo.")
        elif opcion == '2':
            borrarPantalla()
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            contrasena = input("Contraseña: ")
            privilegio = input("¿Es profesor o estudiante? ")
            CrearUsuario(nombre, correo, contrasena, privilegio)
        elif opcion == '3':
            esperarTecla(   )
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def iniciar_sesion(conexion, correo, contrasena, privilegio):
    cursor = conexion.cursor()
    query = "SELECT * FROM usuario WHERE correo = %s AND contrasena = %s AND privilegio = %s"
    valores = ( correo, contrasena, privilegio)
    cursor.execute(query, valores)
    resultado = cursor.fetchone()
    return resultado is not None
    
def CrearUsuario(conexion, id_usuario, nombre, correo, contrasena, privilegio):
    cursor = conexion.cursor()
    query = "INSERT INTO usuario (id_usuario, nombre, correo, contrasena, privilegio) VALUES (NULL, %s, %s, %s, %s)"
    valores = (id_usuario, nombre, correo, contrasena, privilegio)
    cursor.execute(query, valores)
    conexion.commit()
    print(f"Usuario creado correctamente")  

def menu():
    conexion = conexion_BD()
    if conexion:
        while True:
            borrarPantalla()
            print("\n....::::BIENVENIDO::::....")
            print("\n--- Menú de Opciones ---")
            print("1- Libros Disponibles")
            print("2. Préstamo de Libro")
            print("3. Eventos Disponibles")
            print("4. Asistir Evento")
            print("5. Salir")
            opcion = input("Elige una opción: ")

            if opcion == '1':
                borrarPantalla()
                verLibros(conexion)
            elif opcion == '2':
                borrarPantalla()
                ISBN = input("Escribe el ISBN del libro que quieres pedir: ")
                estado = "Prestado"
                Pedir(conexion, ISBN, estado)
            elif opcion == '3':
                borrarPantalla()
                verEventos(conexion)
            elif opcion == '4':
                borrarPantalla()
                id_usuario = input("'Ingrese su ID: ")
                id_evento = input("'Ingrese el ID del evento al que desea asistir: ")
                asistio = "Si"
                Asistio(conexion, id_usuario, id_evento, asistio)
            elif opcion == '5':
                esperarTecla()
                cerrar_conexion(conexion)
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

def menuempleado():
    conexion = conexion_BD()
    if conexion:
        while True:
            borrarPantalla()
            print("\n....::::EMPLEADOS::::....")
            print("\n--- Menú de Opciones ---")
            print("1. Manejar Empleados")
            print("2. Manejar Usuarios")
            print("3. Manejar Prestamos")
            print("4. Manejar Eventos")
            print("5. Salir")
            opcion = input("Elige una opción: ")

            if opcion == '1':
                borrarPantalla()
                print("\n--- Menú de Empleados ---")
                print("1. Agregar Empleado")
                print("2- ELiminar Empleado")
                print("3- Salir")
                opcion1 = input("Elige una opción: ")
                if opcion1 == '1':
                    borrarPantalla()
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    contrasena = input("Contraseña: ")
                    privilegio = "Empleado"
                    RFC = input("Escriba su RFC: ")
                    AgregarEmpleado(conexion, id_usuario, nombre, correo, contrasena, privilegio,RFC)
                elif opcion1 == '2':
                    borrarPantalla()
                    id_usuario = input("Escriba el id del empleado a eliminar: ")
                    eliminarEmpleado(conexion, id_usuario)
                elif opcion == '3':
                    esperarTecla()
                    break

            elif opcion == '2':
                borrarPantalla()
                print("\n--- Menú de Usuarios ---")
                print("1. Agregar Usuario")
                print("2- ELiminar Usuario")
                print("3- Salir")
                opcion1 = input("Elige una opción: ")
                if opcion1 == '1':
                    borrarPantalla()
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    contrasena = input("Contraseña: ")
                    privilegio = input("¿Es estudiante o profesor? ")
                    AgregarUsuario(conexion, id_usuario, nombre, correo, contrasena, privilegio)
                elif opcion1 == '2':
                    borrarPantalla()
                    id_usuario = input("Escriba el id del usuario a eliminar ")
                    eliminarUsuario(conexion, id_usuario)
                elif opcion == '3':
                    esperarTecla()
                    break

            elif opcion == '3':
                borrarPantalla()
                print("\n--- Menú de Prestamos ---")
                print("1. Agregar Prestamo")
                print("2- ELiminar Prestamo")
                print("3- Modificar Prestamo")
                print("4- Salir")
                opcion1 = input("Elige una opción: ")
                if opcion1 == '1':
                    borrarPantalla()
                    ISBN = input("Ingresar el ISBN del libro prestado: ")
                    fecha_prestamo = input("¿En qué fecha se realizo el préstamo?: ")
                    fecha_devolucion = input("¿Cual es la fecha limite? (Dos semanas maximo) ")
                    prestar()
                    PrestamoLibro(conexion, ISBN, fecha_prestamo, fecha_devolucion)
                elif opcion1 == '2':
                    borrarPantalla()
                    ISBN = input("Ingresar el ISBN del libro devuelto: ")
                    devolver()
                    eliminarPrestamo(conexion, ISBN)
                elif opcion1 == '3':
                    borrarPantalla()
                    ISBN = input("Ingresar el ISBN del libro a modificar: ")
                    fecha_prestamo = input("¿En qué fecha se realizo el préstamo?: ")
                    fecha_devolucion = input("¿Cual es la fecha limite? (Dos semanas maximo) ")
                    ModificarPrestamo(conexion, ISBN, fecha_prestamo, fecha_devolucion)
                elif opcion == '4':
                    esperarTecla()
                    break

            elif opcion == '4':
                borrarPantalla()
                print("\n--- Menú de Eventos ---")
                print("1. Agregar Evento")
                print("2- Modificar Evento")
                print("3- Salir")
                opcion1 = input("Elige una opción: ")
                if opcion1 == '1':
                    borrarPantalla()
                    titulo = input("Ingrese el titulo del evento: ")
                    fecha = input("Ingresar la fecha del evento: ")
                    descripcion = input("Escribe la descripcion del evento: ")
                    Evento(conexion, titulo, fecha, descripcion)
                elif opcion1 == '2':
                    borrarPantalla()
                    id_evento = input("Escribe el id del evento a modificar: ")
                    titulo = input("Ingrese el titulo del evento: ")
                    fecha = input("Ingresar la fecha del evento: ")
                    descripcion = input("Escribe la descripcion del evento: ")
                    Evento(conexion, id_evento, titulo, fecha, descripcion)
                elif opcion == '3':
                    esperarTecla()
                    break

            elif opcion == '5':
                esperarTecla()
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "_main_":
    menu()

def verLibros(conexion):
    cursor = conexion.cursor()
    query = "SELECT * FROM libro"
    cursor.execute(query)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(f"ISBN: {fila[0]}, Titulo: {fila[1]}, Autor: {fila[2]}, Estado: {fila[3]}")

def Pedir(conexion, ISBN, estado):
    cursor = conexion.cursor()
    query = "UPDATE libro SET estado = %s WHERE ISBN = %s"
    valores = (estado, ISBN)
    cursor.execute(query, valores)
    conexion.commit()

def verEventos(conexion):
    cursor = conexion.cursor()
    query = "SELECT * FROM evento"
    cursor.execute(query)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(f"ID: {fila[0]}, Titulo: {fila[1]}, Fecha: {fila[2]}, Descripcion: {fila[3]}")

def AgregarEmpleado(conexion, RFC, nombre, id_usuario, correo, contraseña, privilegio):
    cursor = conexion.cursor()
    query = "INSERT INTO usuario (id_usuario, nombre, correo, contraseña, privilegio) VALUES (NULL, %s, %s, %s, %s)"
    valores = (id_usuario, nombre, correo, contraseña, privilegio)
    cursor.execute(query, valores)
    conexion.commit()
    query = "INSERT INTO empleado (id_usuario, RFC) VALUES (NULL, %s)"
    valores1 = (id_usuario, RFC)
    cursor.execute(query, valores1)
    conexion.commit()
    print("Empleado creado exitosamente")

def eliminarEmpleado(conexion, id_usuario):
    cursor = conexion.cursor()
    query = "DELETE FROM empleados WHERE id_usuario = %s"
    valores = (id_usuario)
    cursor.execute(query, valores)
    conexion.commit()
    print("Empleado eliminado exitosamente")

def AgregarUsuario(conexion, id_usuario, nombre, correo, contrasena, privilegio):
    cursor = conexion.cursor()
    query = "INSERT INTO usuario (id_usuario, nombre, correo, contrasena, privilegio) VALUES (NULL, %s, %s, %s, %s)"
    valores = (id_usuario, nombre, correo, contrasena, privilegio)
    cursor.execute(query, valores)
    conexion.commit()
    print(f"Usuario creado correctamente")

def eliminarUsuario(conexion, id_usuario):
    cursor = conexion.cursor()
    query = "DELETE FROM usuario WHERE id_usuario = %s"
    valores = (id_usuario)
    cursor.execute(query, valores)
    conexion.commit()
    print("Usuario eliminado exitosamente")

def PrestamoLibro(conexion, id_usuario, ISBN, fecha_prestamo, fecha_devolucion):
    cursor = conexion.cursor()
    query = "INSERT INTO prestamo (id_usuario, ISBN, fecha_prestamo, fecha_devolucion) VALUES (NULL, %s, %s, %s)"
    valores = (id_usuario, ISBN, fecha_prestamo, fecha_devolucion)
    cursor.execute(query, valores)
    conexion.commit()
    print("Préstamo realizado exitosamente")

def eliminarPrestamo(conexion, ISBN):
    cursor = conexion.cursor()
    query = "DELETE FROM prestamo WHERE ISBN = %s"
    valores = (ISBN)
    cursor.execute(query, valores)
    conexion.commit()
    print("Préstamo eliminado exitosamente")

def ModificarPrestamo(conexion, id_usuario, ISBN, fecha_prestamo, fecha_devolucion):
    cursor = conexion.cursor()
    query = "UPDATE prestamo SET ISBN = %s, fecha_prestamo = %s, fecha_devolucion = %s WHERE id_usuario = %s"
    valores = (ISBN, fecha_prestamo, fecha_devolucion, id_usuario)
    cursor.execute(query, valores)
    conexion.commit()
    print("Préstamo modificado exitosamente")

def Evento(conexion, id_evento, titulo, fecha, descripcion):
    cursor = conexion.cursor()
    query = "INSERT INTO evento (id_evento, titulo, fecha, descripcion) VALUES (NULL, %s, %s, %s)"
    valores = (id_evento, titulo, fecha, descripcion)
    cursor.execute(query, valores)
    conexion.commit()
    print("Evento creado exitosamente")   

def ModificarEvento(conexion, id_evento, titulo, fecha, descripcion):
    cursor = conexion.cursor()
    query = "UPDATE evento SET titulo = %s, fecha = %s, descripcion = %s WHERE id_evento = %s"
    valores = (titulo, fecha, descripcion, id_evento)
    cursor.execute(query, valores)
    conexion.commit()
    print("Evento modificado exitosamente")   

def Asistio(conexion, id_usuario, id_evento, asistio):
    cursor = conexion.cursor()
    query = "INSERT INTO asistencia (id_usuario, id_evento, asistio) VALUES (%s, %s, %s)"
    valores = (id_usuario, id_evento,  asistio)
    cursor.execute(query, valores)
    conexion.commit()
    print("Asistio al evento")   

def prestar(self):
        if self.estado == "disponible": 
            self.estado = "prestado"
            print("El libro  ha sido prestado.")
        else:
            print(f"El libro  no está disponible.")
def devolver(self):
        if self.estado =="prestado":
            self.estado = "disponible"
            print(f"El libro ha sido devuelto.")
        else:
            print(f"El libro no está prestado.")


def cerrar_conexion(conexion):
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")   

class Libro:
    def __init__(self, titulo, autor, isbn, estado):
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn
        self.__estado = estado
    
    def getTitulo(self):
        return self.__titulo
    
    def setTitulo(self, titulo):
        self.__titulo=titulo

    def getAutor(self):
        return self.__autor
    
    def setAutor(self,autor):
        self.__autor=autor

    def getISBN(self):
        return self.__isbn
    
    def setISBN(self,isbn):
        self.__isbn=isbn

    def getEstado(self):
        return self.__estado
    
    def setEstado(self, estado):
        self.__estado=estado

    def prestar(self):
        if self.estado == "disponible": 
            self.estado = "prestado"
            print(f"El libro {self.getTitulo()} ha sido prestado.")
        else:
            print(f"El libro {self.getTitulo()}no está disponible.")
    def devolver(self):
        if self.estado =="prestado":
            self.estado = "disponible"
            print(f"El libro {self.getTitulo()} ha sido devuelto.")
        else:
            print(f"El libro {self.getTitulo()} no está prestado.")

class Usuario:
    def __init__(self, nombre, id_usuario, correo, contraseña, privilegio):
        self.__nombre = nombre
        self.__id_usuario=id_usuario
        self.__correo=correo
        self.__contraseña=contraseña
        self.__privilegio=privilegio

    def getNombre(self):
        return self.__nombre
    
    def setNombre(self, nombre):
        self.__nombre=nombre

    def getCorreo(self):
        return self.__correo
    
    def setCorreo(self,correo):
        self.__correo=correo

    def getId_usuario(self): 
        return self.__id_usuario
    
    def setId_usuario(self, id_usuario):
        self.__id_usuario=id_usuario

    def getContraseña(self):
        return self.__contraseña
    
    def setContraseña(self, contraseña):
        self.__contraseña=contraseña

    def getPrivilegio(self):
        return self.__privilegio
    
    def setPrivilegio(self, privilegio):
        self.__privilegio=privilegio

    def solicitarPrestamo (self, libro): 
        libro.prestar()

    def devolverLibro(self, libro): 
        libro.devolver()

    def __str__(self):
        return f"Nombre: {self.__nombre}, ID: {self.__id_usuario}"
    
class Estudiante(Usuario):
    def __init__(self, nombre, id_usuario, grado, seccion, correo, contraseña, privilegio):
        super().__init__(nombre, id_usuario, correo, contraseña, privilegio)
        self.__grado = grado
        self.__seccion = seccion

    def getGrado(self):
        return self.__grado
    
    def setGrado(self,grado):
        self.__grado=grado

    def getSeccion(self):
        return self.__seccion
    
    def setSeccion(self, seccion):
        self.__seccion=seccion

    def __str__(self):
        return super().__str__()+ f", Grado: {self.__grado}, Sección: {self.__seccion}"
    
class Profesor(Usuario):
    def _Init(self, nombre, id_usuario, departamento, correo, contraseña, privilegio):
        super().__init__(nombre, id_usuario, correo, contraseña, privilegio)
        self.__departamento=departamento

    def getDepartamento(self):
        return self.__departamento
    
    def setDepartamento(self, departamento):
        self.__departamento-departamento

    def _str_(self):
        return super().__str__()+f", Departamento: {self.__departamento}"
    
class Empleado(Usuario):
    def __init__(self, RFC,nombre, id_usuario, correo, contraseña, privilegio):
        super().__init__(nombre, id_usuario, correo, contraseña, privilegio)
        self.__RFC=RFC
        self.__id_usuario=id_usuario

    def getRFC(self):
        return self.__RFC
    
    def setRFC(self, RFC):
        self.__RFC=RFC

    def getld_empleado(self):
        return self.__id_usuario
    
    def setId_empleado(self,id_usuario):
        self.__id_usuario=id_usuario

    def registrarPrestamo(self, usuario, libro):
        usuario.solicitarPrestamo(libro)
        print(f"Empleado {self.getRFC()} ha registrado el préstamo del libro {libro} para {usuario}")

    def registrarDevolucion(self, usuario, libro):
        usuario.devolverLibro(libro) 
        print(f"Empleado {self.getRFC()} ha registrado la devolución del libro {libro} para {usuario}.")
    
    def __str__(self):
        return f"Nombre: {self.__nombre}, ID: {self.__id_usuario}"
    
class Eventos:
    def __init__(self, titulo, fecha, descripcion, id_evento):
        self.__titulo = titulo
        self.__fecha = fecha
        self.__descripcion = descripcion
        self.__id_evento=id_evento

    def getTitulo(self):
        return self.__titulo
    
    def setTitulo(self, titulo):
        self.__titulo=titulo

    def getFecha(self):
        return self.__fecha
    
    def setFecha(self, fecha):
        self.__fecha=fecha

    def getDescricpion(self):
        return self.__descripcion
    
    def setDescripcion(self, descripcion):
        self.__descripcion=descripcion

    def getID_evento(self):
        return self.__id_evento
    
    def setID_evento(self, id_evento):
        self.__id_evento=id_evento

    def registrarAsistencia(self, usuario):
        print(f"Usuario {usuario} ha registrado su asistencia al evento (self._titulo)'.")

    def __str__(self):
        return f"Titulo: {self.__titulo}, Fecha: {self.__fecha}, Descripción: {self.__descripcion}"
    
class Prestamo:
    def __inti__(self, id_usuario, ISBN, fecha_prestamo, fecha_devolucion):
        self.__id_usuario=id_usuario
        self.__ISBN=ISBN
        self.__fecha_prestamo=fecha_prestamo
        self.__fecha_devolucion=fecha_devolucion
    
    def getID_usuario(self):
        return self.__id_usuario
    
    def setID_usuario(self, id_usuario):
        self.__id_usuario=id_usuario

    def getISBN(self):
        return self.__ISBN
    
    def setISBN(self, ISBN):
        self.__ISBN=ISBN

    def getFecha_prestamo(self):
        return self.__fecha_prestamo
    
    def setFecha_prestamo(self, fecha_prestamo):
        self.__fecha_prestamo=fecha_prestamo

    def getFecha_devolucion(self):
        return self.__fecha_devolucion
    
    def setFecha_devolucion(self, fecha_devolucion):
        self.__fecha_devolucion=fecha_devolucion

    def VerificarEstado(self):
        print(f"El libro aun sigue en prestamo hasta la fecha: {self.getFecha_devolucion}")

    def CalcularMulta(self):
        print(f"La multa es un total de: 200")

class Asistencia: 
    def __init__(self,id_usuario, id_evento, fecha_asistencia, asistio):
        super()._init_(id_usuario)
        self.__id_usuario=id_usuario
        self.__id_evento=id_evento
        self.__fecha_asistencia=fecha_asistencia
        self.__asistio=asistio
    
    def setID_usuario(self, id_usuario):
        self.__id_usuario=id_usuario
    def getID_usuario(self):
        return self.__id_usuario
    
    def setID_evento(self, id_evento):
        self.__id_evento=id_evento

    def getID_evento(self):
        return self.__id_evento
    
    def setFecha_asistencia(self, fecha_asistencia):
        self.__fecha_asistencia=fecha_asistencia

    def getFecha_asistencia(self):
        return self.__fecha_asistencia
    
    def setAsistio(self, asistio):
        self.__asistio=asistio

    def getAsistio(self):
        return self.__asistio
    
    def VerificarAsistencia(self):
        print(f"El usuario{self.getID_usuario} asistió al evento {self.getID_evento}el dia{self.getFecha_asistencia}")

if __name__ == "__main__":
    menu_inicio_sesion()