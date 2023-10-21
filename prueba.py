
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()
'''
query = 'INSERT INTO Ahorro (Fecha, Ingreso, Gasto) VALUES (?, ?, ?)'


valores = [("2023-10-17", 10, 0),
           ("2023-10-19", 10, 0),
           ("2023-10-20", 10, 0)]

cursor.executemany(query, valores)
'''
conexion.commit()
cursor.close()
conexion.close()