import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
from Asistencias.asistencias import *
from Empleados.empleados import *
from Eventos.eventos import *
from Usuarios.usuarios import *
from Libros.libros import *
from Prestamos.prestamos import *


usuario_id_global = None

def conexion_BD():
    try:
        conexion = mysql.connector.connect(
            host='127.0.0.1',
            database='biblioteca',
            user='root',
            password='',
            port='3307'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return None

def limpiar_pantalla(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def mostrar_imagen_libreria(ventana, frame):
    img = Image.open("libro amarillo.png")
    img = img.resize((200, 150))  # Ajusta el tamaño según necesites
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame, image=img_tk)
    label_img.image = img_tk
    label_img.pack()

def centrar_widgets(frame, widgets):
    for widget in widgets:
        widget.pack(pady=5)

def menu_usuarios(conexion):
    global usuario_id_global
    ventana_inicio = tk.Tk()
    ventana_inicio.title("Libreria")
    ventana_inicio.geometry("800x600")
    ventana_inicio.configure(bg='#F5DEB3')  # Fondo color arena

    frame = tk.Frame(ventana_inicio, bg='#F5DEB3')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def registrar_usuario():
        limpiar_pantalla(frame)
        tk.Label(frame, text="Nombre:").pack()
        entry_nombre = tk.Entry(frame)
        entry_nombre.pack()
        tk.Label(frame, text="Apellido:").pack()
        entry_apellido = tk.Entry(frame)
        entry_apellido.pack()
        tk.Label(frame, text="Correo:").pack()
        entry_correo = tk.Entry(frame)
        entry_correo.pack()
        tk.Label(frame, text="Contraseña:").pack()
        entry_contrasena = tk.Entry(frame, show="*")
        entry_contrasena.pack()
        tk.Button(frame, text="Registrar", command=lambda: confirmar_registro(entry_nombre.get(), entry_apellido.get(), entry_correo.get(), entry_contrasena.get())).pack()

    def confirmar_registro(nombre, apellido, correo, contrasena):
        usuario = Usuario(nombre, apellido, correo, contrasena)
        usuario.RegistrarUsuario(conexion)
        messagebox.showinfo("Registro", "Usuario registrado exitosamente")
        limpiar_pantalla(frame)
        mostrar_imagen_libreria(ventana_inicio, frame)
        mostrar_botones_inicio_sesion()  # Vuelve a mostrar los botones

    def iniciar_sesion():
        limpiar_pantalla(frame)
        tk.Label(frame, text="Correo:").pack()
        entry_correo = tk.Entry(frame)
        entry_correo.pack()
        tk.Label(frame, text="Contraseña:").pack()
        entry_contrasena = tk.Entry(frame, show="*")
        entry_contrasena.pack()
        tk.Button(frame, text="Iniciar Sesión", command=lambda: confirmar_sesion(entry_correo.get(), entry_contrasena.get())).pack()

    def confirmar_sesion(correo, contrasena):
        usuario_id = Usuario.iniciar_sesion(conexion, correo, contrasena)
        if usuario_id:
            ventana_inicio.destroy()
            menu_principal(conexion, usuario_id)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def mostrar_botones_inicio_sesion():
        btn_login = tk.Button(frame, text="Iniciar Sesión", command=iniciar_sesion, width=20, height=2)
        btn_register = tk.Button(frame, text="Registrar", command=registrar_usuario, width=20, height=2)
        centrar_widgets(frame, [btn_login, btn_register])

    # Mostrar imagen de librería
    mostrar_imagen_libreria(ventana_inicio, frame)
    # Mostrar los botones de inicio de sesión y registro
    mostrar_botones_inicio_sesion()

    ventana_inicio.mainloop()


def menu_principal(conexion, usuario_id):
    ventana_principal = tk.Tk()
    ventana_principal.title("Menú Principal")
    ventana_principal.geometry("800x600")
    ventana_principal.configure(bg='#F5DEB3')

    frame = tk.Frame(ventana_principal, bg='#F5DEB3')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def abrir_menu_libros():
        ventana_principal.destroy()
        menu_libros(conexion, usuario_id)

    def abrir_menu_eventos():
        ventana_principal.destroy()
        menu_eventos(conexion, usuario_id)

    def abrir_menu_empleados():
        ventana_principal.destroy()
        menuempleado(conexion)

    btn_libros = tk.Button(frame, text="Libros", command=abrir_menu_libros)
    btn_eventos = tk.Button(frame, text="Eventos y Asistencias", command=abrir_menu_eventos)
    btn_empleados = tk.Button(frame, text="Menú de Empleados", command=abrir_menu_empleados)
    btn_salir = tk.Button(frame, text="Salir", command=lambda: cerrar_conexion(conexion))

    centrar_widgets(frame, [btn_libros, btn_eventos, btn_empleados, btn_salir])

    ventana_principal.mainloop()

def menu_libros(conexion, usuario_id):
    ventana_libros = tk.Tk()
    ventana_libros.title("Libros")
    ventana_libros.geometry("800x600")
    ventana_libros.configure(bg='#F5DEB3')

    frame = tk.Frame(ventana_libros, bg='#F5DEB3')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def solicitar_prestamo():
        ISBN = entry_ISBN.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion = entry_fecha_devolucion.get()
        prestamo = Prestamo(usuario_id, ISBN, fecha_prestamo, fecha_devolucion)
        prestamo.RealizarPrestamo(conexion)
        messagebox.showinfo("Préstamo", "Préstamo realizado con éxito")

    def consultar_libros():
        libro = Libros()
        libro.ConsultarLibros(conexion)


    label_ISBN = tk.Label(frame, text="ISBN del Libro:")
    entry_ISBN = tk.Entry(frame)
    label_fecha_prestamo = tk.Label(frame, text="Fecha de Préstamo (AAAA-MM-DD):")
    entry_fecha_prestamo = tk.Entry(frame)
    label_fecha_devolucion = tk.Label(frame, text="Fecha de Devolución (AAAA-MM-DD):")
    entry_fecha_devolucion = tk.Entry(frame)

    btn_solicitar_prestamo = tk.Button(frame, text="Solicitar Préstamo", command=solicitar_prestamo)
    btn_consultar_libros = tk.Button(frame, text="Consultar Libros Disponibles", command=consultar_libros)
    btn_volver = tk.Button(frame, text="Volver al Menú Principal", command=lambda: [ventana_libros.destroy(), menu_principal(conexion, usuario_id)])

    centrar_widgets(frame, [label_ISBN, entry_ISBN, label_fecha_prestamo, entry_fecha_prestamo, label_fecha_devolucion, entry_fecha_devolucion, btn_solicitar_prestamo, btn_consultar_libros, btn_volver])

    ventana_libros.mainloop()

def menu_eventos(conexion, usuario_id):
    ventana_eventos = tk.Tk()
    ventana_eventos.title("Eventos y Asistencias")
    ventana_eventos.geometry("800x600")
    ventana_eventos.configure(bg='#F5DEB3')

    frame = tk.Frame(ventana_eventos, bg='#F5DEB3')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # def consultar_eventos():
    #     evento = Eventos()
    #     evento.ConsultarEventos(conexion)

    def consultar_eventos():
        evento = Eventos()
        evento.ConsultarEventos(conexion, ventana_eventos)  # Pasar la ventana actual como argumento


    def registrar_asistencia():
        id_evento = entry_id_evento.get()
        fecha_asistencia = entry_fecha_asistencia.get()
        asistio = entry_asistio.get().lower() == 'sí'
        asistencia = Asistencia(usuario_id, id_evento, fecha_asistencia, asistio)
        asistencia.RegistrarAsistencia(conexion)
        messagebox.showinfo("Asistencia", "Asistencia registrada exitosamente")

    label_id_evento = tk.Label(frame, text="ID del Evento:")
    entry_id_evento = tk.Entry(frame)
    label_fecha_asistencia = tk.Label(frame, text="Fecha de Asistencia (AAAA-MM-DD):")
    entry_fecha_asistencia = tk.Entry(frame)
    label_asistio = tk.Label(frame, text="¿Asistió al evento? (Sí/No):")
    entry_asistio = tk.Entry(frame)

    btn_registrar_asistencia = tk.Button(frame, text="Registrar Asistencia", command=registrar_asistencia)
    btn_consultar_eventos = tk.Button(frame, text="Consultar Eventos Disponibles", command=consultar_eventos)
    btn_volver = tk.Button(frame, text="Volver al Menú Principal", command=lambda: [ventana_eventos.destroy(), menu_principal(conexion, usuario_id)])

    centrar_widgets(frame, [label_id_evento, entry_id_evento, label_fecha_asistencia, entry_fecha_asistencia, label_asistio, entry_asistio, btn_registrar_asistencia, btn_consultar_eventos, btn_volver])

    ventana_eventos.mainloop()

import tkinter as tk
from tkinter import messagebox

def menuempleado(conexion):
    ventana_empleados = tk.Tk()
    ventana_empleados.title("Menú de Empleados")
    ventana_empleados.geometry("800x600")
    ventana_empleados.configure(bg='#F5DEB3')

    frame = tk.Frame(ventana_empleados, bg='#F5DEB3')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def agregar_empleado():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ID de Usuario:").pack()
        entry_id_usuario = tk.Entry(frame)
        entry_id_usuario.pack()
        tk.Label(frame, text="RFC:").pack()
        entry_RFC = tk.Entry(frame)
        entry_RFC.pack()
        tk.Button(frame, text="Agregar Empleado", command=lambda: confirmar_agregar_empleado(entry_id_usuario.get(), entry_RFC.get())).pack()

    def confirmar_agregar_empleado(id_usuario, RFC):
        empleado = Empleado(id_usuario, RFC)
        empleado.AgregarEmpleado(conexion)
        messagebox.showinfo("Empleado", "Empleado agregado exitosamente")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def eliminar_empleado():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ID de Empleado a Eliminar:").pack()
        entry_id_usuario = tk.Entry(frame)
        entry_id_usuario.pack()
        tk.Button(frame, text="Eliminar Empleado", command=lambda: confirmar_eliminar_empleado(entry_id_usuario.get())).pack()

    def confirmar_eliminar_empleado(id_usuario):
        empleado = Empleado(id_usuario)
        empleado.EliminarEmpleado(conexion)
        messagebox.showinfo("Empleado", "Empleado eliminado exitosamente")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def eliminar_usuario():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ID de Usuario a Eliminar:").pack()
        entry_id_usuario = tk.Entry(frame)
        entry_id_usuario.pack()
        tk.Button(frame, text="Eliminar Usuario", command=lambda: confirmar_eliminar_usuario(entry_id_usuario.get())).pack()

    def confirmar_eliminar_usuario(id_usuario):
        usuario = Usuario(id_usuario=id_usuario)
        usuario.EliminarUsuario(conexion)
        messagebox.showinfo("Usuario", "Usuario eliminado exitosamente")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def agregar_prestamo():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ID de Usuario:").pack()
        entry_id_usuario = tk.Entry(frame)
        entry_id_usuario.pack()
        tk.Label(frame, text="ISBN del Libro:").pack()
        entry_ISBN = tk.Entry(frame)
        entry_ISBN.pack()
        tk.Label(frame, text="Fecha de Préstamo (AAAA-MM-DD):").pack()
        entry_fecha_prestamo = tk.Entry(frame)
        entry_fecha_prestamo.pack()
        tk.Label(frame, text="Fecha de Devolución (AAAA-MM-DD):").pack()
        entry_fecha_devolucion = tk.Entry(frame)
        entry_fecha_devolucion.pack()
        tk.Button(frame, text="Agregar Préstamo", command=lambda: confirmar_agregar_prestamo(entry_id_usuario.get(), entry_ISBN.get(), entry_fecha_prestamo.get(), entry_fecha_devolucion.get())).pack()

    def confirmar_agregar_prestamo(id_usuario, ISBN, fecha_prestamo, fecha_devolucion):
        prestamo = Prestamo(id_usuario, ISBN, fecha_prestamo, fecha_devolucion)
        prestamo.RealizarPrestamo(conexion)
        messagebox.showinfo("Préstamo", "Préstamo realizado con éxito")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def eliminar_prestamo():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ISBN del Préstamo a Eliminar:").pack()
        entry_ISBN = tk.Entry(frame)
        entry_ISBN.pack()
        tk.Button(frame, text="Eliminar Préstamo", command=lambda: confirmar_eliminar_prestamo(entry_ISBN.get())).pack()

    def confirmar_eliminar_prestamo(ISBN):
        prestamo = Prestamo(ISBN=ISBN)
        prestamo.EliminarPrestamo(conexion)
        messagebox.showinfo("Préstamo", "Préstamo eliminado con éxito")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def agregar_evento():
        limpiar_pantalla(frame)
        tk.Label(frame, text="Título del Evento:").pack()
        entry_titulo = tk.Entry(frame)
        entry_titulo.pack()
        tk.Label(frame, text="Fecha del Evento (AAAA-MM-DD):").pack()
        entry_fecha = tk.Entry(frame)
        entry_fecha.pack()
        tk.Label(frame, text="Descripción del Evento:").pack()
        entry_descripcion = tk.Entry(frame)
        entry_descripcion.pack()
        tk.Button(frame, text="Agregar Evento", command=lambda: confirmar_agregar_evento(entry_titulo.get(), entry_fecha.get(), entry_descripcion.get())).pack()

    def confirmar_agregar_evento(titulo, fecha, descripcion):
        evento = Eventos(titulo=titulo, fecha=fecha, descripcion=descripcion)
        evento.AgregarEvento(conexion)
        messagebox.showinfo("Evento", "Evento agregado exitosamente")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def modificar_evento():
        limpiar_pantalla(frame)
        tk.Label(frame, text="ID del Evento a Modificar:").pack()
        entry_id_evento = tk.Entry(frame)
        entry_id_evento.pack()
        tk.Label(frame, text="Nuevo Título del Evento:").pack()
        entry_titulo = tk.Entry(frame)
        entry_titulo.pack()
        tk.Label(frame, text="Nueva Fecha del Evento (AAAA-MM-DD):").pack()
        entry_fecha = tk.Entry(frame)
        entry_fecha.pack()
        tk.Label(frame, text="Nueva Descripción del Evento:").pack()
        entry_descripcion = tk.Entry(frame)
        entry_descripcion.pack()
        tk.Button(frame, text="Modificar Evento", command=lambda: confirmar_modificar_evento(entry_id_evento.get(), entry_titulo.get(), entry_fecha.get(), entry_descripcion.get())).pack()

    def confirmar_modificar_evento(id_evento, titulo, fecha, descripcion):
        evento = Eventos(id_evento=id_evento, titulo=titulo, fecha=fecha, descripcion=descripcion)
        evento.ModificarEvento(conexion, id_evento, titulo, fecha, descripcion)
        messagebox.showinfo("Evento", "Evento modificado exitosamente")
        limpiar_pantalla(frame)
        menuempleado(conexion)  # Volver al menú de empleados

    def volver_menu_principal():
        ventana_empleados.destroy()
        menu_principal(conexion, usuario_id_global)  # Redirige al menú principal

    # Botones del menú de empleados
    btn_agregar_empleado = tk.Button(frame, text="Agregar Empleado", command=agregar_empleado)
    btn_eliminar_empleado = tk.Button(frame, text="Eliminar Empleado", command=eliminar_empleado)
    btn_eliminar_usuario = tk.Button(frame, text="Eliminar Usuario", command=eliminar_usuario)
    btn_agregar_prestamo = tk.Button(frame, text="Agregar Préstamo", command=agregar_prestamo)
    btn_eliminar_prestamo = tk.Button(frame, text="Eliminar Préstamo", command=eliminar_prestamo)
    btn_agregar_evento = tk.Button(frame, text="Agregar Evento", command=agregar_evento)
    btn_modificar_evento = tk.Button(frame, text="Modificar Evento", command=modificar_evento)
    btn_volver = tk.Button(frame, text="Volver", command=volver_menu_principal)

    centrar_widgets(frame, [btn_agregar_empleado, btn_eliminar_empleado, btn_eliminar_usuario, btn_agregar_prestamo, btn_eliminar_prestamo, btn_agregar_evento, btn_modificar_evento, btn_volver])

    ventana_empleados.mainloop()

def limpiar_pantalla(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def centrar_widgets(frame, widgets):
    for widget in widgets:
        widget.pack(pady=5)




def cerrar_conexion(conexion):
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")
    exit()

if __name__ == "__main__":
    conexion = conexion_BD()
    if conexion:
        menu_usuarios(conexion)
