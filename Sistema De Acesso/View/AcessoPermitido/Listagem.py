import streamlit as st
from Controller.GrupoAcessoUsuarioController import GrupoAcessoUsuarioController

def Listagem():
    st.title("Listagem Completa de Permissões")   
    todos_grupos = GrupoAcessoUsuarioController.get_all_grupos()
    grupo_options = {g[0]: g[1] for g in todos_grupos}
    grupo_selecionado = st.selectbox(    
        "Filtrar por Grupo:",
        options=["Todos"] + list(grupo_options.keys()),
        format_func=lambda x: "Todos" if x == "Todos" else grupo_options[x]
    )

    try:
        permissoes = GrupoAcessoUsuarioController.get_permissoes_completas()       
        if grupo_selecionado != "Todos":
            permissoes = [p for p in permissoes if p[0] == grupo_selecionado]        
        if not permissoes:
            st.info("Nenhuma permissão encontrada para os critérios selecionados.")
            return
        
        for permissao in permissoes:            
            with st.expander(f"{permissao[1]}", expanded=True):
                col1, col2 = st.columns([1, 1])              
                with col1:
                    st.subheader("Painéis Associados")
                    st.write(permissao[2] or "Nenhum painel associado")

                    # Se não tem dados no Itens de Faturamento, não exibe o itens de receita.
                    if permissao[3] != "Não aplicável":
                        st.subheader("Itens de Faturamento")
                        st.write(permissao[3])

                with col2:
                    st.subheader("Usuários com Acesso")
                    usuarios = permissao[4].split(', ')
                    for usuario in usuarios:
                        st.write(f"- {usuario}")                

    except Exception as e:
        st.error(f"Erro ao carregar permissões: {str(e)}")
