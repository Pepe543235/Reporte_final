from conexionBD import *
import tkinter as tk
from tkinter import messagebox

class Asistencia:
    def __init__(self, id_usuario, id_evento, fecha_asistencia, asistio):
        self.id_usuario = id_usuario
        self.id_evento = id_evento
        self.fecha_asistencia = fecha_asistencia
        self.asistio = asistio

    def RegistrarAsistencia(self, conexion):
        cursor = conexion.cursor()
        query = "INSERT INTO asistencia (id_usuario, id_evento, fecha_asistencia, asistio) VALUES (%s, %s, %s, %s)"
        valores = (self.id_usuario, self.id_evento, self.fecha_asistencia, self.asistio)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Asistencia", "Asistencia registrada correctamente")
