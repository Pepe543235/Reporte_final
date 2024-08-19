from tkinter import messagebox
from conexionBD import *
import tkinter as tk

class Prestamo:
    def __init__(self, id_usuario, ISBN, fecha_prestamo, fecha_devolucion):
        self.id_usuario = id_usuario
        self.ISBN = ISBN
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def RealizarPrestamo(self, conexion):
        cursor = conexion.cursor()
        query = "INSERT INTO prestamo (id_usuario, ISBN, fecha_prestamo, fecha_devolucion) VALUES (%s, %s, %s, %s)"
        valores = (self.id_usuario, self.ISBN, self.fecha_prestamo, self.fecha_devolucion)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Préstamo", "Préstamo creado correctamente")

    @staticmethod
    def EstadoPrestamo(conexion, ventana_padre):
        cursor = conexion.cursor()
        query = "SELECT * FROM prestamo"
        cursor.execute(query)
        resultados = cursor.fetchall()

        ventana_estado = tk.Toplevel(ventana_padre)
        ventana_estado.title("Estado de Préstamos")
        ventana_estado.geometry("600x400")
        ventana_estado.configure(bg='#F5DEB3')

        frame = tk.Frame(ventana_estado, bg='#F5DEB3')
        frame.pack(expand=True, fill=tk.BOTH)

        if resultados:
            for fila in resultados:
                prestamo_info = f"id_prestamo: {fila[0]}, id_usuario: {fila[1]}, ISBN: {fila[2]}, fecha_prestamo: {fila[3]}, fecha_devolucion: {fila[4]}"
                label_prestamo = tk.Label(frame, text=prestamo_info, bg='#F5DEB3')
                label_prestamo.pack(anchor="w", pady=5)
        else:
            label_sin_prestamos = tk.Label(frame, text="No se encontraron préstamos.", bg='#F5DEB3')
            label_sin_prestamos.pack(anchor="w", pady=5)

        btn_volver = tk.Button(frame, text="Cerrar", command=ventana_estado.destroy)
        btn_volver.pack(pady=20)

    @staticmethod
    def EliminarPrestamo(conexion, ISBN):
        cursor = conexion.cursor()
        query = "DELETE FROM prestamo WHERE ISBN = %s"
        cursor.execute(query, (ISBN,))
        conexion.commit()
        messagebox.showinfo("Préstamo", "Préstamo eliminado correctamente")
