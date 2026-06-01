import streamlit as st
import locale
import time
import plotly.express as px
from model.sql_conn import create_connection, fetch_receitaliquidaAtual_data
from model.database import get_group_name, get_user_permissions     

st.set_page_config(
    page_title="Receita Líquida Bruta",  
    page_icon=":📊", 
)

# Adicione esta função para mostrar a sidebar
def show_sidebar():
    with st.sidebar:
        if 'id_grupoacesso' in st.session_state:
            st.title("🔒 Controle de Acesso")
            st.subheader(f"Usuário: {st.session_state['nm_email']}")
            st.subheader(f"Grupo: {get_group_name(st.session_state['id_grupoacesso'])}")
            st.divider()            
            # Mostrar ano selecionado (se existir na sessão)
            if 'ano' in st.session_state:
                st.write(f"Ano selecionado: {st.session_state['ano']}")            
            st.divider()
            if st.button("🔓 Voltar ao Menu"):
                st.switch_page("pages/menu.py")

show_sidebar()
# Configurar locale para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if 'permissions' not in st.session_state:
    st.session_state.permissions = get_user_permissions(st.session_state['id_grupoacesso'])

itens_permitidos = st.session_state.permissions.get('itens_receita', [])

conn = create_connection()
if conn:           
    ano_selecionado  = st.session_state['ano']
    df_display = fetch_receitaliquidaAtual_data(conn, ano_selecionado, itens_permitidos)

    if df_display.empty:
        st.warning("Nenhum dado encontrado para os grupos permitidos.")
        st.stop()

    df_display = df_display.rename(columns={
        'nm_itens_grupo_receita': 'Nome do Grupo',
        'total_vl_liquido': 'Faturamento Bruto Líquido',
        'total_vl_devolucoesvendas': 'Devolucoes Vendas',
        'total_vl_devolucoesservicos': 'Devolucoes Servicos',
        'receita_liquida': 'Receita Líquida'
    })

    st.header("Receita Líquida")
    st.divider()

    st.subheader("📦 Filtrar os Grupos")
    df = df_display.sort_values("Nome do Grupo")
    grupos = st.multiselect(
        "Selecione o(s) Grupo(s):",
            #options=df["Nome do Grupo"].unique())
            options=df_display["Nome do Grupo"].unique(), 
            default=df_display["Nome do Grupo"].unique())


    # Configurar as guias
    guia_tabela, guia_grafico = st.tabs(["📊 Tabela", "📈 Gráfico"])
    # Guia de tabela
    with guia_tabela:
        st.subheader("Tabelas e Gráficos do Banco de Dados")
        # Formatar valores como moeda apenas para exibição na tabela
        df_tabela = df_display.copy()
        for col in ['Faturamento Bruto Líquido', 'Devolucoes Vendas', 'Devolucoes Servicos', 'Receita Líquida']:
            df_tabela[col] = df_tabela[col].apply(lambda x: locale.currency(x, grouping=True))       
        if st.checkbox("Mostrar a Tabela da Receita Líquida Bruta"):
            st.subheader(f" 📋 Listagem da Receita Líquida Bruta - {ano_selecionado}")
            if grupos:
                df_tabela = df_tabela[df_tabela["Nome do Grupo"].isin(grupos)]
            st.dataframe(df_tabela[['Nome do Grupo', 'Faturamento Bruto Líquido',
                        'Devolucoes Vendas', 'Devolucoes Servicos', 'Receita Líquida']])            
        if grupos:
            df = df[df["Nome do Grupo"].isin(grupos)]
        df = df.groupby("Nome do Grupo")["Receita Líquida"].sum().reset_index()
        df = df.sort_values(by="Receita Líquida", ascending=True)

    with guia_grafico:
        # Criar Grafico
        st.subheader(f"Gráfico de Receita Líquida em {ano_selecionado}")
        fig = px.bar(
            df, x= "Receita Líquida", y= "Nome do Grupo",           
            labels={"Nome do Grupo": "Grupo",
                    "Receita Líquida": "Total da Receita Líquida"},
            color="Nome do Grupo",
            orientation="h")
        st.plotly_chart(fig)

    conn.close()
else:
    st.error("Não foi possivel conectar ao banco de dados.")
