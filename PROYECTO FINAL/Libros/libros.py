from conexionBD import *
from tkinter import messagebox

class Libros:

    def __init__(self, ISBN=None, titulo=None, autor=None, estado=None):
        self.ISBN = ISBN
        self.titulo = titulo
        self.autor = autor
        self.estado = estado

    @staticmethod
    def ConsultarLibros(conexion):
        cursor = conexion.cursor()
        query = "SELECT * FROM libro"
        cursor.execute(query)
        resultados = cursor.fetchall()

        if resultados:
            libros_info = "\n".join([f"ISBN: {fila[0]}, Título: {fila[1]}, Autor: {fila[2]}, Estado: {fila[3]}" for fila in resultados])
            messagebox.showinfo("Libros Disponibles", libros_info)
        else:
            messagebox.showinfo("Libros Disponibles", "No se encontraron libros.")

        cursor.close()


