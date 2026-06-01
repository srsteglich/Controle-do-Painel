import streamlit as st

pages = {
    "Grupos de Acesso": [
        st.Page("Pages/grupos_acesso.py", title="Cadastro de Grupos de Acesso"),
    ],
    "Permissão": [
        st.Page("Pages/permissao.py", title="Cadastro de Permissão com o Usuário"),
    ],
    "Permissão de Acesso": [
        st.Page("Pages/listar_permissaoacesso.py", title="Listagem Grupo de Acesso por Usuário"),
    ],
}
navigation = st.navigation(pages)
navigation.run()