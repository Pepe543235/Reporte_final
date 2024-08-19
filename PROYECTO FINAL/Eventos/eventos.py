from conexionBD import *
import tkinter as tk
from tkinter import messagebox

class Eventos:
    def __init__(self, id_evento=None, titulo=None, fecha=None, descripcion=None):
        self.id_evento = id_evento
        self.titulo = titulo
        self.fecha = fecha
        self.descripcion = descripcion

    def AgregarEvento(self, conexion):
        cursor = conexion.cursor()
        query = "INSERT INTO evento (titulo, fecha, descripcion) VALUES (%s, %s, %s)"
        valores = (self.titulo, self.fecha, self.descripcion)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Evento", "Evento agregado correctamente")

    @staticmethod
    def ModificarEvento(conexion, id_evento, titulo, fecha, descripcion):
        cursor = conexion.cursor()
        query = "UPDATE evento SET titulo = %s, fecha = %s, descripcion = %s WHERE id_evento = %s"
        valores = (titulo, fecha, descripcion, id_evento)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Evento", "Modificación hecha correctamente")

    @staticmethod
    def ConsultarEventos(conexion, ventana_padre):
        cursor = conexion.cursor()
        query = "SELECT * FROM evento"
        cursor.execute(query)
        resultados = cursor.fetchall()

        ventana_eventos = tk.Toplevel(ventana_padre)
        ventana_eventos.title("Consulta de Eventos")
        ventana_eventos.geometry("1000x400")
        ventana_eventos.configure(bg='#ADD8E6')

        frame = tk.Frame(ventana_eventos, bg='#ADD8E6')
        frame.pack(expand=True, fill=tk.BOTH)

        if resultados:
            for fila in resultados:
                evento_info = f"id_evento: {fila[0]}, título: {fila[1]}, fecha: {fila[2]}, descripción: {fila[3]}"
                label_evento = tk.Label(frame, text=evento_info, bg='#ADD8E6')
                label_evento.pack(anchor="w", pady=5)
        else:
            label_sin_eventos = tk.Label(frame, text="No se encontraron eventos.", bg='#ADD8E6')
            label_sin_eventos.pack(anchor="w", pady=5)

        btn_volver = tk.Button(frame, text="Cerrar", command=ventana_eventos.destroy)
        btn_volver.pack(pady=20)

        cursor.close()
