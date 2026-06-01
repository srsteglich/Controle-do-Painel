import streamlit as st

st.set_page_config(
    page_title="Login",  
    page_icon=":🔑", 
)

if 'nm_email' in st.session_state and 'id_grupoacesso' in st.session_state:
    st.title("Informações do Usuário")
    st.write(f"E-mail: {st.session_state['nm_email']}")
    st.write(f"ID do Grupo de Acesso: {st.session_state['id_grupoacesso']}")

    st.switch_page("pages/menu.py")

    if st.button("Voltar"):
        st.switch_page("main.py")
else:
    st.error("Usuário não autenticado. Por favor, volte à página principal.")
    if st.button("Ir para página principal"):
        st.switch_page("main.py")