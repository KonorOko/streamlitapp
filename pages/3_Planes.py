import streamlit as st
from sqlalchemy import create_engine
from models import Plan
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Conecction with database
ssl_args = {'ssl_ca': 'cacert.pem'}
connection_string = "mysql+mysqlconnector://p52vdv0zokfr4l81yw6y:pscale_pw_tu40dgYizB7VgXbJNSFkRxQ5k7KIVVaaG2tvYhL9kbs@aws.connect.psdb.cloud:3306/project"
engine = create_engine(connection_string, echo=False, connect_args=ssl_args)
Session = sessionmaker(bind=engine)
session = Session()

def main():
    st.header('Planes por hacer')
    st.markdown('''
Salidas o citas que tenemos pendientes por hacer💕''')
    try:
        cita = st.text_input('Agregar planes:', placeholder='Cita<3')
        budget = st.text_input('Budget', placeholder= 'Dinero necesario')
        if st.button('Agregar', type= 'primary'):
            nuevo_registro = Plan(Nombre = cita, Budget = budget)
            session.add(nuevo_registro)
            session.commit()
            
    except:
        pass

    finally:
        session.close()

    try:
        consulta_sql = "SELECT * FROM Ahorro"
        df = pd.read_sql_query(consulta_sql, engine)
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
        df1 = pd.read_sql_query(query, engine)

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
    finally:
        session.close()

st.set_page_config(page_title='Citas', page_icon='📆')  
st.sidebar.header("Citas bonitas")
st.sidebar.caption('Quiero que estemos juntos.')

main()