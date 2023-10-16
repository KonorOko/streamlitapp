import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import altair as alt
import pytz

tz = pytz.timezone('America/Mexico_City')
# Crear una conexión a la base de datos SQLite (o crear el archivo de la base de datos si no existe)
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Crear una tabla si no existe
c.execute('''
          CREATE TABLE IF NOT EXISTS registros (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              fecha TEXT,
              ingresos REAL,
              gastos REAL
          )
          ''')


def main_window():
    st.markdown("""
                # Alcancia
                ### Ahorros para comprar cosas con la más preciosa
                """)

    # Obtener los valores actuales de los widgets (si existen)
    ingresos = st.text_input('Ingresos', key= 1)
    gastos = st.text_input('Gastos', key=2)

    try:
        col1, col2, col3 = st.columns(3)
        if col1.button("Agregar"):
            if ingresos.isnumeric() and gastos.isnumeric():
                ingresos = float(ingresos)
                gastos = float(gastos)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                # Insertar datos en la base de datos
                c.execute("INSERT INTO registros (fecha, ingresos, gastos) VALUES (?, ?, ?)",
                          (fecha_actual, ingresos, gastos))
                conn.commit()  # Guardar cambios en la base de datos

            elif ingresos.isnumeric():
                ingresos = float(ingresos)
                gastos = float(0)
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                # Insertar datos en la base de datos
                c.execute("INSERT INTO registros (fecha, ingresos, gastos) VALUES (?, ?, ?)",
                          (fecha_actual, ingresos, gastos))
                conn.commit()  # Guardar cambios en la base de datos

            elif gastos.isnumeric():
                ingresos = float(0)
                gastos = float(gastos)
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                # Insertar datos en la base de datos
                c.execute("INSERT INTO registros (fecha, ingresos, gastos) VALUES (?, ?, ?)",
                          (fecha_actual, ingresos, gastos))
                conn.commit()  # Guardar cambios en la base de datos
                 
            else:
                 pass

        if col2.button("Borrar ultimo registro"):
                c.execute("DELETE FROM registros WHERE id = (SELECT MAX(id) FROM registros)")
                conn.commit()  # Guardar cambios en la base de datos

        if col3.button("Borrar Registros"):
            c.execute("DELETE FROM registros")  # Borrar todos los registros de la base de datos
            conn.commit()  # Guardar cambios en la base de datos

    except Exception as e:
        st.error(f'Error: {e}')

    # Leer datos de la base de datos y crear un DataFrame
    c.execute("SELECT * FROM registros")
    db_data = c.fetchall()
    df = pd.DataFrame(db_data, columns=['id', 'Fecha', 'Ingresos', 'Gastos'])
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
    df['Fecha'] = df['Fecha'].dt.date
    df['Ingresos'] = pd.to_numeric(df['Ingresos'], errors='coerce')
    df['Gastos'] = pd.to_numeric(df['Gastos'], errors='coerce')

    tabla = df.groupby('Fecha').agg({'Ingresos': 'sum', 'Gastos': 'sum'}).reset_index()

    tabla['Balance diario'] = tabla['Ingresos'] - tabla['Gastos']
    tabla['Balance total'] = tabla['Balance diario'].cumsum()

    st.dataframe(tabla, height=200, width=800)
    chart = (
        alt.Chart(tabla)
        .mark_line()
        .encode(
        x="Fecha:T",
        y="Balance total:Q")
        )
    st.altair_chart(chart, use_container_width=True)



    
st.set_page_config(page_title="Ahorros", page_icon="📊")
st.sidebar.header("Dinero")

main_window()
