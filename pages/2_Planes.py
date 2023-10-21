import streamlit as st
import pandas as pd
import mysql.connector

connection = mysql.connector.connect(
  host= st.secrets.db_credentials.host,
  user= st.secrets.db_credentials.username,
  password = st.secrets.db_credentials.password,
  database = st.secrets.db_credentials.database,
  ssl_ca = "/workspaces/streamlitapp/cacert.pem")

# Crea un cursor para ejecutar consultas SQL
cursor = connection.cursor()

def main():
    st.header('Planes por hacer')
    st.markdown('''
Salidas o citas que tenemos pendientes por hacer💕''')
    try:
        col1, col2 = st.columns(2)
        cita = col1.text_input('Agregar planes:', placeholder='Cita<3')

        budget = col2.text_input('Budget', placeholder= 'Dinero necesario')
        if st.button('Agregar', type= 'primary', use_container_width=True):
            nuevo_registro = (cita, budget)
            queryadd = "INSERT INTO Plan (Nombre, Budget) VALUES (%s, %s)"
            cursor.execute(queryadd, nuevo_registro)
            connection.commit()

        delete = st.text_input('Eliminar', placeholder='Ingrese el nombre del plan que quiera borrar')
        if st.button('DELETE', type= 'primary'):

            consulta_eliminar = "DELETE FROM Plan WHERE Nombre = %s"
            cursor.execute(consulta_eliminar, (delete,))

            # Hacer commit para confirmar los cambios en la base de datos
            connection.commit()
            
    except:
        pass


    try:
        consulta_sql = "SELECT * FROM Ahorro"
        df = pd.read_sql_query(consulta_sql, connection)
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
        df1 = pd.read_sql_query(query, connection)

        df1['Dinero'] = df1.apply(lambda row: row['Budget'] <= balance_total, axis=1)
        df2 = df1[['Nombre', 'Budget', 'Dinero']]



        st.data_editor(
            df2,
            column_config={
                "Dinero": st.column_config.CheckboxColumn(
                    "Dinero?",
                    help="Se marcan cuando tenemos el dinero suficiente",
                    default=False,
                    disabled=True
            )
        },
        disabled=["widgets"],
        hide_index=True
        )

        





    except:
        pass

st.set_page_config(page_title='Citas', page_icon='📆')  
st.sidebar.header("Citas bonitas")
st.sidebar.caption('Quiero que estemos juntos.')

main()