import streamlit as st
from model.database import get_user_permissions, get_group_name
from model.sql_conn import create_connection, fetch_ano

st.set_page_config(
    page_title="Menu Pricipal",  
    page_icon=":💻", 
)
# Função para armazenar o ano selecionado na sessão
def store_value():
    if '_ano' in st.session_state:
        st.session_state['ano'] = st.session_state['_ano']

def show_menu():
    if 'id_grupoacesso' not in st.session_state:
        st.error("Usuário não autenticado. Por favor, seleciona o teu e-mail.")
        if st.button("Ir para página principal"):
            st.switch_page("main.py")
        return
    
    # Configuração da barra lateral
    with st.sidebar:
        # Exibe informações do usuário
        st.title("🔒 Controle de Acesso")
        st.subheader(f"Usuário: {st.session_state['nm_email']}")
        
        # Obtém o nome do grupo
        group_name = get_group_name(st.session_state['id_grupoacesso'])
        st.subheader(f"Grupo: {group_name}")
        st.divider()
        
        # Obtém permissões
        try:
            permissions = get_user_permissions(st.session_state['id_grupoacesso'])
        except Exception as e:
            st.error(f"Erro ao carregar permissões: {str(e)}")
            permissions = {'paineis': [], 'itens_receita': [], 'nomes_itens': {}}
        
        conn = create_connection()
        df_anos = fetch_ano(conn)
        anos_disponiveis = df_anos['ano'].astype(str).tolist()
        
        if 'ano' not in st.session_state:
            st.session_state['ano'] = anos_disponiveis[-1]
        
        ano_selecionado = st.selectbox(
            "Selecione o Ano", 
            anos_disponiveis, 
            index=anos_disponiveis.index(st.session_state['ano']),           
            key="_ano", 
            on_change=store_value
        )

        # Mapeamento de IDs de painel para os links correspondentes
        paineis = {
            1: ("clientes.py", "🏅 Tops 10 Clientes"),
            2: ("clientesreceitas.py", "📈 Clientes e Receitas"),
            3: ("faturamento.py", "💰 Faturamentos Brutos"),
            4: ("mensalfaturamento.py", "📅 Faturamentos Mensal"),
            5: ("receitaliquida.py", "💵 Receita Líquida"),
            6: ("diariofaturamento.py", "📆  Faturamento Diário")
        }
        
        # Menu de Clientes
        if any(p in permissions['paineis'] for p in [1, 2]):
            st.header("Clientes")
            for pid in [1, 2]:
                if pid in permissions['paineis']:
                    link, label = paineis[pid]
                    st.page_link(f"pages/{link}", label=label)
        
        # Menu de Faturamento
        if any(p in permissions['paineis'] for p in range(3, 7)):
            st.header("Faturamentos")
            for pid in range(3, 7):
                if pid in permissions['paineis']:
                    link, label = paineis[pid]
                    st.page_link(f"pages/{link}", label=label)
        
        st.divider()
        
        if st.button("🔓  Sair"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("main.py")

    # Área principal da página
    st.title("Painel de Controle")
    st.write("Selecione o ano e após selecione uma opção no menu lateral para acessar os painéis disponíveis.")

show_menu()