import streamlit as st

def main():
    if 'citas' not in st.session_state:
        st.session_state.citas = []

    st.header('Planes por hacer')
    st.markdown('''
Salidas o citas que tenemos pendientes por hacer💕''')
    try:
        cita = st.text_input('Agregar planes:')
        if st.button('Agregar'):
            st.session_state.citas.append(cita)

        for i in st.session_state.citas:
            st.checkbox(i)
    except:
        pass

st.set_page_config(page_title='Citas', page_icon='📆')  
st.sidebar.header("Citas bonitas")
st.sidebar.caption('Quiero que estemos juntos.')

main()