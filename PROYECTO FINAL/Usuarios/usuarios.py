from tkinter import messagebox
from conexionBD import *

class Usuario:
    def __init__(self, nombre, correo, contrasena, privilegio):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.privilegio = privilegio

    def RegistrarUsuario(self, conexion):
        cursor = conexion.cursor()
        query = "INSERT INTO usuario (nombre, correo, contrasena, privilegio) VALUES (%s, %s, %s, %s)"
        valores = (self.nombre, self.correo, self.contrasena, self.privilegio)
        cursor.execute(query, valores)
        conexion.commit()
        id_usuario = cursor.lastrowid  # Obtiene el ID del usuario recién registrado
        messagebox.showinfo("Registro exitoso", f"Usuario agregado correctamente con ID: {id_usuario}")
        return id_usuario

    @staticmethod
    def iniciar_sesion(conexion, correo, contrasena):
        cursor = conexion.cursor()
        query = "SELECT id_usuario, nombre FROM usuario WHERE correo = %s AND contrasena = %s"
        cursor.execute(query, (correo, contrasena))
        usuario = cursor.fetchone()
        if usuario:
            messagebox.showinfo("Inicio de sesión", f"Bienvenido, {usuario[1]}! Tu ID de usuario es: {usuario[0]}")
            return usuario[0]  # Devuelve el ID de usuario
        else:
            messagebox.showwarning("Error de inicio de sesión", "Correo o contraseña incorrectos.")
            return None

    @staticmethod
    def EliminarUsuario(conexion, id_usuario):
        cursor = conexion.cursor()
        query = "DELETE FROM usuario WHERE id_usuario = %s"
        valores = (id_usuario,)
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Usuario eliminado", "Usuario eliminado exitosamente")
