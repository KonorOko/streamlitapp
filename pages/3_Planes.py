import streamlit as st
import pandas as pd
import sqlite3

# Conecction with database
conexion = sqlite3.connect('mi_base_de_datos.db')

cursor = conexion.cursor()

# Crear la tabla Ahorro con columnas de tipo REAL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Plan (
        ID_Plan INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Budget REAL NOT NULL
    )
''')

conexion.commit()

def main():
    st.header('Planes por hacer')
    st.markdown('''
Salidas o citas que tenemos pendientes por hacer💕''')
    try:
        cita = st.text_input('Agregar planes:', placeholder='Cita<3')
        budget = st.text_input('Budget', placeholder= 'Dinero necesario')
        if st.button('Agregar', type= 'primary'):
            nuevo_registro = (cita, budget)
            queryadd = 'INSERT INTO Plan (Nombre, Budget) VALUES (?, ?, ?)'
            cursor.execute(queryadd, nuevo_registro)
            conexion.commit()
            
    except:
        pass


    try:
        consulta_sql = "SELECT * FROM Ahorro"
        df = pd.read_sql_query(consulta_sql, conexion)
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
        df['Fecha'] = df['Fecha'].dt.date
        df['Ingresos'] = pd.to_numeric(df['Ingreso'], errors='coerce')
        df['Gastos'] = pd.to_numeric(df['Gasto'], errors='coerce')

        tabla = df.groupby('Fecha').agg({'Ingreso': 'sum', 'Gasto': 'sum'}).reset_index()

        tabla['Balance diario'] = tabla['Ingreso'] - tabla['Gasto']
        tabla['Balance total'] = tabla['Balance diario'].cumsum()
        idmax = tabla['Balance total'].idxmax()
        balance_total = tabla['Balance total'].iloc[idmax]

        query = 'SELECT * FROM Plan'
        df1 = pd.read_sql_query(query, conexion)

        df1['Dinero'] = df1.apply(lambda row: row['Budget'] <= balance_total, axis=1)


        st.data_editor(
            df1,
            column_config={
                "Dinero": st.column_config.CheckboxColumn(
                    "Dinero?",
                    help="Se marcan cuando tenemos el dinero suficiente",
                    default=False,
            )
        },
        disabled=["widgets"],
        hide_index=True,
        )
    except:
        pass

st.set_page_config(page_title='Citas', page_icon='📆')  
st.sidebar.header("Citas bonitas")
st.sidebar.caption('Quiero que estemos juntos.')

main()