from conexionBD import *
import tkinter as tk
from tkinter import messagebox

class Empleado:
    def __init__(self, id_usuario=None, RFC=None):
        self.id_usuario = id_usuario
        self.RFC = RFC

    def AgregarEmpleado(self, conexion):
        cursor = conexion.cursor()
        query = "INSERT INTO empleado (id_usuario, RFC) VALUES (%s, %s)"
        valores = (self.id_usuario, self.RFC)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Empleado", "Empleado agregado correctamente")

    @staticmethod
    def Consultar(conexion):
        cursor = conexion.cursor()
        query = "SELECT * FROM revisiones"
        cursor.execute(query)
        resultados = cursor.fetchall()

        if resultados:
            registros = ""
            for fila in resultados:
                registros += (f"no_revision: {fila[0]}, cambiofiltro: {fila[1]}, cambioaceite: {fila[2]}, "
                              f"cambiofrenos: {fila[3]}, otros: {fila[4]}, matricula: {fila[5]}\n")
            messagebox.showinfo("Registros de Revisiones", registros)
        else:
            messagebox.showinfo("Registros de Revisiones", "No se encontraron registros.")

    @staticmethod
    def EliminarEmpleado(conexion, id_usuario):
        cursor = conexion.cursor()
        query = "DELETE FROM empleado WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        conexion.commit()
        messagebox.showinfo("Empleado", "Empleado eliminado correctamente")
