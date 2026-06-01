import streamlit as st
import pandas as pd
import time
import plotly.express as px
from model.sql_conn import create_connection, fetch_clientereceita_data  #, fetch_clienteAtualAnter_data
from model.database import get_group_name, get_user_permissions 

st.set_page_config(
    page_title="Cliente e Grupo da Receita",  
    page_icon=":📋", 
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

# Mostra a sidebar antes do conteúdo principal
show_sidebar()

if 'permissions' not in st.session_state:
    st.session_state.permissions = get_user_permissions(st.session_state['id_grupoacesso'])

itens_permitidos = st.session_state.permissions.get('itens_receita', [])


# Configurar o CSS
with open('estilos.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

conn = create_connection()
if conn:
    ano_selecionado  = st.session_state['ano']        
    df_display = fetch_clientereceita_data(conn, ano_selecionado, itens_permitidos)
    # Renomeiar as colunas
    df_display = df_display.rename(columns={
        'nm_itens_grupo_receita': 'Grupo de Receita',
        'nm_Cliente': 'Nome do Cliente',        
        'total_vl_total_nf': 'Total Faturamento'
    }) 

    df_display['Total de Faturamento'] = df_display['Total Faturamento'].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) 
    st.subheader(" Clientes e Grupos de Receita")
    st.divider()
    # Filtro de Grupos (MultiSelect)   
    st.subheader("📦 Filtrar os Grupos de Receita")     
    grupos = st.multiselect(
        "Selecione o(s) Grupo(s):",
        options=df_display["Grupo de Receita"].unique(), 
        default=df_display["Grupo de Receita"].unique())
    if grupos:
        df_display = df_display[df_display["Grupo de Receita"].isin(grupos)] 
# Configurar as guias        
    guia_tabela, guia_grafico, guia_graficopie = st.tabs(["📊 Tabela", "📈 Gráfico de Barra", "🥧 Gráfico da Pizza" ])
    with guia_tabela:        
        st.subheader(f" 📋 Listagem de Clientes com Grupo de Receita - {ano_selecionado}")
        st.dataframe(df_display[['Grupo de Receita', 'Nome do Cliente', 'Total de Faturamento']])
    with guia_grafico:  
        st.subheader(f"📈  Gráfico de Barras - Cliente e Grupo - {ano_selecionado}")
        fig_bar = px.bar(
            df_display,
            x="Total Faturamento", y="Nome do Cliente",
            title=" Total de Receita por Cliente e Grupo",
            labels={"Nome do Cliente": "Cliente", "Total Faturamento": "Faturamento"},
            color="Grupo de Receita",
            height=400,   
            orientation="h")
        # Mostrar Graficos
        st.plotly_chart(fig_bar, use_container_width=True)      
    with guia_graficopie:  
        # Gráfico de Pizza
        st.subheader(f"🥧 Gráfico de Pizza em {ano_selecionado}")
        fig_pizza = px.pie(
            df_display,
            names='Grupo de Receita',
            values='Total Faturamento',
            title="Grupos de Receita em Porcentagem",
            hole=0.3,
        )
        st.plotly_chart(fig_pizza)

    conn.close()

else:
    st.error("Não foi possivel conectar ao banco de dados.")
