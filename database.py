"""
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
fecha_actual1 = '2023-10-14'
ingresos1 = '30'
gastos1 = '0'


c.execute("INSERT INTO registros (fecha, ingresos, gastos) VALUES (?, ?, ?)",
                          (fecha_actual1, ingresos1, gastos1))

c.execute("Delete FROM registros")
conn.commit()

c.execute("SELECT * FROM registros")
data = c.fetchall()
print(data)
"""