import streamlit as st
import random
import time


def ruleta():
    # Header de pagina
    st.header('Ruleta')
    st.markdown('''
             Sirve para cuando la preciosa de Jacque no se decide que escoger 😵‍💫💕.
             ''')

    # Lista de opciones en la ruleta
    if 'opciones' not in st.session_state:
        st.session_state.opciones = []
    try:
        opciones = st.text_input('Ingresa opciones a escoger:')
        if st.button('Agregar'):
            opciones = opciones.split(', ')
            for opcion in opciones:
                st.session_state.opciones.append(opcion)
        with st.expander('!!!'):
            st.markdown('''Puedes agregar múltiples valores a la vez separandolos por una coma y un espacio.  
                        Example: Hoja, Letra, Musica''')
    except Exception as e:
        pass

    st.write(st.session_state.opciones)
    try:
        if st.button("¡Girar la ruleta!"):
            with st.spinner("Girando la ruleta..."):
                time.sleep(2)  # Simula un giro de 2 segundos
                opcion_seleccionada = random.choice(st.session_state.opciones)
            st.success(f"¡La opción seleccionada es: {opcion_seleccionada}")
    except:
        st.warning('Hubo un problema, intentalo de nuevo')

st.set_page_config(page_title="Ruleta", page_icon="🎰")
st.sidebar.header("Azar")
st.sidebar.caption('Alea iacta est.')

ruleta()