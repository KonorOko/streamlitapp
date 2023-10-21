from st_supabase_connection import SupabaseConnection
import streamlit as st
import pandas as pd

conn = st.experimental_connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="Ahorro", ttl="10m").execute()

# Print results.
Fecha = []
Ingreso = []
Gasto = []
for row in rows.data:
    Fecha = [row['Fecha']]
    Ingreso = [row['Ingreso']]
    Gasto = [row['Gasto']]

df = pd.DataFrame(data= {'Fecha': Fecha, 'Ingreso': Ingreso, 'Gasto': Gasto})
st.dataframe(df)
