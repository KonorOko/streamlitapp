import streamlit as st
import random
import time

# Lista de opciones en la ruleta
if 'opciones' not in st.session_state:
    st.session_state.opciones = []


try:
	opcion = st.text_input('Ingresa opciones a escoger:')
	if st.button('Agregar'):
		st.session_state.opciones.append(opcion)
except Exception as e:
	pass
st.write(st.session_state.opciones)
# Botón para girar la ruleta
if st.button("¡Girar la ruleta!"):
    # Animación de giro
    with st.spinner("Girando la ruleta..."):
        time.sleep(2)  # Simula un giro de 2 segundos
        opcion_seleccionada = random.choice(st.session_state.opciones)
    st.success(f"¡La opción seleccionada es: {opcion_seleccionada}")
