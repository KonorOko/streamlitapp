import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
import pytz
from sqlalchemy import create_engine
from models import Ahorro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import mysql.connector
'''
database: project
username: syq92swxj7nksylcqlwd
host: aws.connect.psdb.cloud
password: pscale_pw_hCI6wiQa0xO0grGYGDfI0pNwyQLf549NxspFFKvHMdq

'''
config = {
    'user': ' evhflwkt1vhsd9l1rioe',
    'password': 'pscale_pw_Mf9tyVbBH4c6UHg0vYyX1SasMDXNarO9wNIPj5CLdOp',
    'host': 'aws.connect.psdb.cloud',
    'database': 'project',
    'ssl_verify_identity': True,
    'ssl_ca': '/workspaces/streamlitapp/cacert.pem',
}

cnx = mysql.connector.connect(**config)
cnx.close()

print("Successfully connected to PlanetScale!")

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
                nuevo_registro = Ahorro(Fecha = fecha_actual, Ingreso = ingresos, Gasto = gastos)
                session.add(nuevo_registro)
                session.commit()

            elif ingresos.isnumeric():
                ingresos = float(ingresos)
                gastos = float(0)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                print(fecha_actual)
                # Insertar datos en la base de datos
                nuevo_registro = Ahorro(Fecha = fecha_actual, Ingreso = ingresos, Gasto = gastos)
                session.add(nuevo_registro)
                session.commit()

            elif gastos.isnumeric():
                ingresos = float(0)
                gastos = float(gastos)
                fecha_actual = datetime.now(tz).strftime("%Y-%m-%d")
                # Insertar datos en la base de datos
                nuevo_registro = Ahorro(Fecha = fecha_actual, Ingreso = ingresos, Gasto = gastos)
                session.add(nuevo_registro)
                session.commit()
                
                 
            else:
                 pass

        if col3.button("Borrar último registro", type="primary"):
            ultimo_id = session.query(func.max(Ahorro.ID_Ahorro)).scalar()
            elemento_a_eliminar = session.query(Ahorro).filter_by(ID_Ahorro=ultimo_id).one()

            session.delete(elemento_a_eliminar)
            session.commit()


    except Exception as e:
        st.error(f'Error: {e}')

    finally:
         pass
         

    # Leer datos de la base de datos y crear un DataFrame
    consulta_sql = "SELECT * FROM Ahorro"
    df = pd.read_sql_query(consulta_sql, cnx)
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
