import streamlit as st
import pandas as pd
import model.database as database

st.set_page_config(
    page_title="Acesso Restrito",  
    page_icon=":🎯", 
)

st.header("Lista de Usuários")
def consultar_usuarios():
    try:
        conn = database.fetch_postgres_connection()
        cursor = conn.cursor()   
        cursor.execute("""SELECT id_usuario, id_grupoacesso, nm_email 
                            FROM ADV_GrupoAcesso_Usuario
                            ORDER BY nm_email""")
        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

df = consultar_usuarios()
if df is not None:
    # Mostrar a lista de e-mails    
    email_selecionado = st.selectbox("Selecione um e-mail:", df['nm_email'].tolist())
    
    if st.button("Entrar"):
        usuario = df[df['nm_email'] == email_selecionado].iloc[0]
        st.session_state['id_usuario'] = usuario['id_usuario']
        st.session_state['id_grupoacesso'] = usuario['id_grupoacesso']
        st.session_state['nm_email'] = usuario['nm_email']
        
        st.switch_page("pages/login.py")