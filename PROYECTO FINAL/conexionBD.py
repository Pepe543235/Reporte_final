import mysql.connector
from tkinter import messagebox


conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='biblioteca',
        port='3307'
    )


