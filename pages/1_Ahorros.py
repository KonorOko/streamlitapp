import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
import pytz
from sqlalchemy import func
import streamlit as st

import sqlite3

# Conectar a la base de datos (si no existe, se creará)
conexion = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear la tabla Ahorro solo si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ahorro (
        ID_Ahorro INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha TEXT NOT NULL,
        Ingreso REAL NOT NULL,
        Gasto REAL NOT NULL
    )
''')

conexion.commit()
# Guardar los cambios y cerrar la conexión

query = "INSERT INTO Ahorro (Fecha, Ingreso, Gasto) VALUES (?, ?, ?)"

# Adjust the time zone
tz = pytz.timezone('America/Mexico_City')


def main_window():
    st.markdown("""
                # Alcancia
                ### Dinero ahorrado con la más preciosa del mundo ☀️❤️
                """)

    # Obtener los valores actuales de los widgets (si existen)
    ingresos = st.text_input('Ingresos', key= 1, placeholder= 'Ingresar dinero<3')
    gastos = st.text_input('Gastos', key=2, placeholder= 'Ingresar dinero gastado unu')

    try:
        col1, col2, col3 = st.columns(3)
        if col1.button("Agregar registro", type="primary"):
            if ingresos.isnumeric() and gastos.isnumeric():
                ingresos = float(ingresos)
                gastos = float(gastos)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                nuevo_registro = (fecha_actual, ingresos, gastos)
                cursor.execute(query, nuevo_registro)
                conexion.commit()

            elif ingresos.isnumeric():
                ingresos = float(ingresos)
                gastos = float(0)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                print(fecha_actual)
                # Insertar datos en la base de datos
                nuevo_registro = (fecha_actual, ingresos, gastos)
                cursor.execute(query, nuevo_registro)
                conexion.commit()

            elif gastos.isnumeric():
                ingresos = float(0)
                gastos = float(gastos)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                # Insertar datos en la base de datos
                nuevo_registro = (fecha_actual, ingresos, gastos)
                cursor.execute(query, nuevo_registro)
                conexion.commit()
                
                 
            else:
                 pass

        if col3.button("Borrar último registro", type="primary"):
            cursor.execute("DELETE FROM Ahorro WHERE ID_Ahorro = (SELECT MAX(ID_Ahorro) FROM Ahorro)")
            conexion.commit()


    except Exception as e:
        st.error(f'Error: {e}')

    finally:
        pass
         

    # Leer datos de la base de datos y crear un DataFrame
    consulta_sql = "SELECT * FROM Ahorro"
    df = pd.read_sql_query(consulta_sql, conexion)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
    df['Fecha'] = df['Fecha'].dt.date
    df['Ingresos'] = pd.to_numeric(df['Ingreso'], errors='coerce')
    df['Gastos'] = pd.to_numeric(df['Gasto'], errors='coerce')

    tabla = df.groupby('Fecha').agg({'Ingreso': 'sum', 'Gasto': 'sum'}).reset_index()

    tabla['Balance diario'] = tabla['Ingreso'] - tabla['Gasto']
    tabla['Balance total'] = tabla['Balance diario'].cumsum()

    st.dataframe(tabla, height=200, width=800)
    chart = (
        alt.Chart(tabla)
        .mark_line()
        .encode(
        alt.X('utcyearmonthdate(Fecha):O').title('Fecha'),
        y="Balance total:Q")
        )
    st.altair_chart(chart, use_container_width=True)



    
st.set_page_config(page_title="Ahorros", page_icon="📊")
st.sidebar.header("Para el futuro")
st.sidebar.caption('Vivir momentos a tu lado es lo mejor que hay.')

main_window()
