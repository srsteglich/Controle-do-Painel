import streamlit as st
from Controller.GrupoAcessoController import GrupoAcessoController

def Listar():                           # Mostra o título da página no topo: "Grupos de Acesso"
    st.title("Grupos de Acesso")    
    if 'grupo_page' not in st.session_state:    # Se a chave 'grupo_page' ainda não estiver definida no estado da sessão (st.session_state), ela é criada com valor 'list', primeira exibição da página será a lista de grupos
        st.session_state.grupo_page = 'list'
    if 'edit_id' not in st.session_state:       # Define uma chave para armazenar o ID do grupo a ser editado
        st.session_state.edit_id = None   

    if st.session_state.grupo_page == 'list':   # Se o estado atual for "list", chama a função show_list(), que exibe a lista de grupos cadastrados.
        show_list()
    elif st.session_state.grupo_page == 'form': # Se o estado for "form", chama a função show_form(), passando o edit_id (se houver), para exibir o formulário de criação ou edição.
        show_form(st.session_state.edit_id)
    elif st.session_state.grupo_page == 'delete':   # Se o estado for "delete", chama a função show_delete_confirm() para exibir a tela de confirmação de exclusão.
        show_delete_confirm(st.session_state.edit_id)

def show_list():
    if st.button("➕ Novo Grupo"):
        st.session_state.grupo_page = 'form'
        st.session_state.edit_id = None
        st.rerun()    
    try:
        grupos = GrupoAcessoController.get_all_grupos()        
        if not grupos:
            st.info("Nenhum grupo cadastrado ainda.")
            return        
        # Cabeçalho da tabela
        cols = st.columns([2, 6, 4, 2])
        #cols[0].write("**ID**")
        cols[0].write("**Nome**")
        cols[1].write("**Painéis Associados**")
        cols[2].write("**Itens de Faturamento**")        
        cols[3].write("**Ações**")        
        # Linhas da tabela
        for grupo in grupos:
            col1, col2, col3, col4 = st.columns([ 2, 6, 4, 2])
            #col1.write(grupo[0])  # ID
            col1.write(grupo[1])  # Nome
            col2.write(grupo[2] if grupo[2] else "Nenhum")  # Painéis            
            col3.write(grupo[3] if grupo[3] else "Nenhum")  # Itens            
            # Botões de ação
            btn1, btn2 = col4.columns(2)
            if btn1.button("✏️", key=f"edit_{grupo[0]}"):
                st.session_state.grupo_page = 'form'
                st.session_state.edit_id = grupo[0]
                st.rerun()            
            if btn2.button("🗑️", key=f"del_{grupo[0]}"):
                st.session_state.grupo_page = 'delete'
                st.session_state.edit_id = grupo[0]
                st.rerun()    
    except Exception as e:
        st.error(f"Erro ao carregar grupos: {str(e)}")

def show_form(edit_id=None):
    st.subheader("Cadastramento do Grupo de Acesso" if edit_id is None else "Editar Grupo de Acesso")    
    paineis_disponiveis = GrupoAcessoController.get_all_paineis()
    painel_options = {p[0]: p[1] for p in paineis_disponiveis}        

    grupo_data = {'id_grupo': None, 'nm_grupo': ''}
    selected_paineis = []
    painel_itens = {}     
    if edit_id:
        grupo_data_db = GrupoAcessoController.get_grupo_by_id(edit_id)
        if grupo_data_db:  
            grupo_data = {
                'id_grupo': grupo_data_db[0],
                'nm_grupo': grupo_data_db[1]
            }
            selected_paineis = [p[0] for p in GrupoAcessoController.get_paineis_do_grupo(edit_id)]        
            for pid in [2, 3, 4, 5, 6]:
                if pid in selected_paineis:
                    painel_itens[pid] = GrupoAcessoController.get_itens_faturamento_by_grupo_painel(edit_id, pid)

        else:
            st.error("Grupo não encontrado no banco de dados")
            st.session_state.grupo_page = 'list'
            st.rerun()
            return

    with st.form(key='grupo_form'):
        nome = st.text_input(
            "Nome do Grupo*",
            value=grupo_data['nm_grupo'], 
            max_chars=100
        )        

        selected_paineis = st.multiselect(
            "Painéis Associados*",
            options=list(painel_options.keys()),
            format_func=lambda x: painel_options[x],
            default=selected_paineis,
            key="paineis_selecionados"
        )       

        show_itens_faturamento = any(p in selected_paineis for p in [2, 3, 4, 5, 6])        
        selected_itens = []

        if show_itens_faturamento:
            itens_receita = GrupoAcessoController.get_itens_grupo_receita()
            if not itens_receita:
                st.warning("Não foi possível carregar os itens de receita.")
            else:
                item_options = {i['id_itens_grupo_receita']: i['nm_itens_grupo_receita'] for i in itens_receita}
                painel_ids_itens = [pid for pid in [2, 3, 4, 5, 6] if pid in selected_paineis]
                
                # ✅ Coleta todos os itens já salvos (de todos os painéis 2-6) ao editar
                default_itens = []
                if edit_id:
                    delayed_itens = []
                    for pid in painel_ids_itens:
                        delayed_itens += painel_itens.get(pid, [])
                    default_itens = list(set(delayed_itens)) # Remove duplicatas

                selected_itens = st.multiselect(
                    "Itens de Faturamento Bruto* (para todos os painéis selecionados de 2 a 6)",
                    options=list(item_options.keys()),
                    format_func=lambda x: item_options[x],
                    #default=painel_itens.get(painel_ids_itens[0], []) if painel_ids_itens else []
                    default=default_itens
                )
                # Atribui os mesmos itens a todos os painéis selecionados entre 2 a 6
                for painel_id in painel_ids_itens:
                    painel_itens[painel_id] = selected_itens
                # Remove dos demais
                for painel_id in [2, 3, 4, 5, 6]:
                    if painel_id not in painel_ids_itens:
                        painel_itens.pop(painel_id, None)
        else:
            for pid in [2, 3, 4, 5, 6]:
                painel_itens.pop(pid, None)
            
        # Botões do formulário
        # Estar mais proximo da coluna do botão de salvar        
        col1, col2 = st.columns([1, 12])
        submitted = col1.form_submit_button("💾 Salvar")
        cancel = col2.form_submit_button("❌ Cancelar")

        #col1, col2 = st.columns(2)       
        #submitted = col1.form_submit_button("💾 Salvar")
        #cancel = col2.form_submit_button("❌ Cancelar")

        if submitted:
            try:
                if not nome:
                    st.error("O nome do grupo é obrigatório")
                    return                
                if not selected_paineis:
                    st.error("Selecione pelo menos um painel")
                    return                
                if show_itens_faturamento and not selected_itens:
                    st.error("É necessário selecionar pelo menos um item de faturamento,")
                    return           
                if edit_id:
                    success = GrupoAcessoController.update_grupo(
                        edit_id, nome, selected_paineis, painel_itens
                    )
                    if success:
                        st.success("Grupo atualizado com sucesso!")
                else:
                    grupo_id = GrupoAcessoController.create_grupo(
                        nome, selected_paineis, painel_itens
                    )
                    st.success(f"Grupo criado com sucesso! ID: {grupo_id}")                
                st.session_state.grupo_page = 'list'
                st.rerun()            
            except Exception as e:
                st.error(f"Erro ao salvar grupo: {str(e)}")
        
        if cancel:
            st.session_state.grupo_page = 'list'
            st.rerun()

def show_delete_confirm(grupo_id):
    st.title("Confirmar Exclusão")    
    grupo = GrupoAcessoController.get_grupo_by_id(grupo_id)
    if not grupo:
        st.error("Grupo não encontrado")
        st.session_state.grupo_page = 'list'
        st.rerun()
        return    
    #st.toast(f"Ver se tem dados no cadastro de permissão com o usuário?",  icon="⚠️")   
    st.warning(f"Você está prestes a excluir o grupo: **{grupo[1]}**")

    #col1, col2 = st.columns(2)
    col1, col2 = st.columns([1, 6])
    if col1.button("✅ Confirmar Exclusão", type="primary"):
        try:
            success = GrupoAcessoController.delete_grupo(grupo_id)
            if success:
                st.success("Grupo excluído com sucesso!")
            else:
                st.error("Nenhum grupo foi excluído. Verifique o ID.")
            
            st.session_state.grupo_page = 'list'
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao excluir grupo: {str(e)}")    
    if col2.button("❌ Cancelar"):
        st.session_state.grupo_page = 'list'
        st.rerun()