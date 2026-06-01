import streamlit as st
from Controller.GrupoAcessoUsuarioController import GrupoAcessoUsuarioController

def Listar():
    st.header("Gerenciamento de Usuários por Grupo de Acesso")
    if 'usuario_page' not in st.session_state:
        st.session_state.usuario_page = 'list'

    if 'edit_id' not in st.session_state:
        st.session_state.edit_id = None

    if st.session_state.usuario_page == 'list':
        show_list()
    elif st.session_state.usuario_page == 'form':
        show_form(st.session_state.edit_id)
    elif st.session_state.usuario_page == 'delete':
        show_delete_confirm(st.session_state.edit_id)

def show_list():
    if st.button("➕ Novo Usuário"):
        st.session_state.usuario_page = 'form'
        st.session_state.edit_id = None
        st.rerun()

    try:
        usuarios = GrupoAcessoUsuarioController.get_all_usuarios()
        if not usuarios:
            st.info("Nenhum usuário cadastrado ainda.")
            return

        # Cabeçalho
        cols = st.columns([4, 3, 2])
        cols[0].write("**E-mail**")
        cols[1].write("**Grupo de Acesso**")
        #cols[2].write("**ID**")
        cols[2].write("**Ações**")

        # Linhas
        for usuario in usuarios:
            cols = st.columns([4, 3, 2])
            #cols[0].text(usuario[1])          
            cols[0].write(usuario[1])  # E-mail                      
            cols[1].write(usuario[3])  # Nome do Grupo
            #cols[2].write(usuario[0])  # ID

            # Botões
            btn_col1, btn_col2 = cols[2].columns(2)
            if btn_col1.button("✏️", key=f"edit_{usuario[0]}"):
                st.session_state.usuario_page = 'form'
                st.session_state.edit_id = usuario[0]
                st.rerun()

            if btn_col2.button("🗑️", key=f"del_{usuario[0]}"):
                st.session_state.usuario_page = 'delete'
                st.session_state.edit_id = usuario[0]
                st.rerun()

    except Exception as e:
        st.error(f"Erro ao carregar usuários: {str(e)}")

def show_form(edit_id=None):
    st.subheader("Editar Usuário" if edit_id else "Novo Usuário")
    # Dados existentes para edição
    usuario_data = {'email': '', 'id_grupoacesso': None}
    if edit_id:
        usuario_db = GrupoAcessoUsuarioController.get_usuario_by_id(edit_id)
        if usuario_db:
            usuario_data = {
                # Remove o domínio para exibir apenas a parte do e-mail antes do @"NOME do DOMÍNIO".com
                'email': usuario_db[1].replace("@******.com", ""), 
                'id_grupoacesso': usuario_db[2]
            }
        else:
            st.error("Usuário não encontrado")
            st.session_state.usuario_page = 'list'
            st.rerun()
            return

    # Formulário
    with st.form(key='usuario_form'):
        col1, col2 = st.columns([3, 1])
        with col1:
            username = st.text_input(
                "Nome do E-mail (sem @******.com)*",
                value=usuario_data['email'],
                placeholder="nome.usuario",
                help="Digite apenas a parte antes do @******.com"
            )
        with col2:
            st.markdown("""
            <style>
            .domain-display {
                font-size: 1rem;
                margin-top: 1.5rem;
                padding: 0.5rem;
                background-color: #f0f2f6;
                border-radius: 0.5rem;
            }
            </style>
            <div class="domain-display">@******.com</div>
            """, unsafe_allow_html=True)

        # Dropdown de grupos
        grupos = GrupoAcessoUsuarioController.get_all_grupos()
        grupo_options = {g[0]: g[1] for g in grupos}
        id_grupoacesso = st.selectbox(
            "Grupo de Acesso*",
            options=list(grupo_options.keys()),
            format_func=lambda x: grupo_options[x],
            index=next((i for i, g in enumerate(grupo_options.keys())
                        if g == usuario_data['id_grupoacesso']), 0)
        )

        # Botões
        #col1, col2 = st.columns(2)
        col1, col2 = st.columns([1, 12])
        submitted = col1.form_submit_button("💾 Salvar")
        cancel = col2.form_submit_button("❌ Cancelar")

        if submitted:
            try:
                if not username:
                    st.error("O e-mail é obrigatório")
                    return

                if not id_grupoacesso:
                    st.error("Selecione um grupo de acesso")
                    return

                # Adiciona o domínio automaticamente
                email_completo = f"{username}@******.com"
                if edit_id:
                    success = GrupoAcessoUsuarioController.update_usuario(
                        edit_id, email_completo, id_grupoacesso
                    )
                    if success:
                        st.success("Usuário atualizado com sucesso!")
                else:
                    usuario_id = GrupoAcessoUsuarioController.create_usuario(
                        email_completo , id_grupoacesso
                    )
                    st.success(f"Usuário criado com sucesso! ID: {usuario_id}")

                st.session_state.usuario_page = 'list'
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao salvar usuário: {str(e)}")

        if cancel:
            st.session_state.usuario_page = 'list'
            st.rerun()


def show_delete_confirm(usuario_id):
    st.warning("Confirmar Exclusão")

    usuario = GrupoAcessoUsuarioController.get_usuario_by_id(usuario_id)
    if not usuario:
        st.error("Usuário não encontrado")
        st.session_state.usuario_page = 'list'
        st.rerun()
        return

    st.markdown(f"""**E-mail:** {usuario[1]}  
                    **ID:** {usuario[0]} """)

    #col1, col2 = st.columns(2)
    col1, col2 = st.columns([1, 6])
    if col1.button("✅ Confirmar Exclusão", type="primary"):
        try:
            success = GrupoAcessoUsuarioController.delete_usuario(usuario_id)
            if success:
                st.success("Usuário excluído com sucesso!")
            else:
                st.error("Falha ao excluir usuário")

            st.session_state.usuario_page = 'list'
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao excluir usuário: {str(e)}")

    if col2.button("❌ Cancelar"):
        st.session_state.usuario_page = 'list'
        st.rerun()
