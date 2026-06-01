import streamlit as st
import pandas as pd
import plotly.express as px 
import time
from datetime import timedelta
from model.sql_conn import create_connection, fetch_diariofaturamento_data
from model.database import get_group_name, get_user_permissions

st.set_page_config(
    page_title="Faturamento Diario",  
    page_icon=":📊", 
)

def show_sidebar():
    with st.sidebar:
        if 'id_grupoacesso' in st.session_state:
            st.title("🔒 Controle de Acesso")
            st.subheader(f"Usuário: {st.session_state['nm_email']}")
            st.subheader(f"Grupo: {get_group_name(st.session_state['id_grupoacesso'])}")
            st.divider()  
            
            if 'ano' in st.session_state:
                st.write(f"Ano selecionado: {st.session_state['ano']}")

            st.divider()
            if st.button("🔓 Voltar ao Menu"):
                st.switch_page("pages/menu.py")

def show_faturamento_data(conn, df_display, ano_selecionado):
    df = df_display.copy()        
    df["dt_lancamento"] = pd.to_datetime(df["dt_lancamento"])
    df["dt_lancamento"] = df["dt_lancamento"].dt.date
    df = df.sort_values("dt_lancamento")
    df = df.set_index("dt_lancamento")
    
    df_display = df_display.rename(columns={
        'dt_lancamento': 'Data',
        'nm_itens_grupo_receita': 'Grupo de Receita',
        'total_vl_total_nf': 'Total Faturamento'
    })
    
    df_display['Total de Faturamento'] = df_display['Total Faturamento'].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.header("Faturamento Diário")
    st.divider()

    st.subheader("📦 Filtrar Grupo da Receita")
    nomes_permitidos = list(st.session_state.permissions.get('nomes_itens', {}).values())  

    filtros_ativos = st.multiselect(
        "Selecione os grupos da receita:",
        options=nomes_permitidos,
        default=nomes_permitidos
    )
 
    if filtros_ativos:
        df_display = df_display[df_display["Grupo de Receita"].isin(filtros_ativos)]
    else:
        st.warning("Nenhum grupo de receita selecionado.")
        return

    st.subheader("📅 Filtrar por Datas")
    data_min = df.index.min()
    data_max = df.index.max()
    
    intervalo = st.slider(
        "Selecione o período:",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
        step=timedelta(days=1),
        format="DD/MM/YYYY"
    )
    
    df_display["Data"] = pd.to_datetime(df_display["Data"])
    df_display = df_display[
        (df_display["Data"].dt.date >= intervalo[0]) & 
        (df_display["Data"].dt.date <= intervalo[1])
    ]

    if df_display.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return
    st.caption(" ")
    #if filtros_ativos:
    st.subheader("📊 Tabelas e Gráficos do Banco de Dados")
    #df_display = df_display[df_display["Grupo de Receita"].isin(filtros_ativos)]
    guia_tabela, guia_graficoline,  guia_graficoarea= st.tabs(["📊 Tabela", "📈 Gráfico de Linhas", " Gráfico de Area" ])  
    with guia_tabela:
        st.subheader(f"📋 Listagem Diário de Faturamento - {ano_selecionado}")
        df_display["Data"] = df_display["Data"].dt.strftime("%d/%m/%Y")
        st.dataframe(df_display[['Data', 'Grupo de Receita', 'Total de Faturamento']])

    with guia_graficoline:            
        if not df_display.empty:
            st.subheader(f"Gráfico de Linhas - Faturamento Diário - {ano_selecionado}")

            df_plot = df_display.copy()
            df_plot['Data'] = pd.to_datetime(df_plot['Data'], format='%d/%m/%Y')
            df_plot = df_plot.sort_values('Data')
            #Converter para string apenas para exibição (opcional)
            df_plot['Data_str'] = df_plot['Data'].dt.strftime('%d/%m/%Y')

            fig = px.line(
                df_plot, 
                x='Data', 
                y='Total Faturamento',
                color='Grupo de Receita',
                markers=True,
                title='Total de Faturamento por Data'
            )

            # Configurar o eixo X para mostrar as datas formatadas
            fig.update_xaxes(
                tickformat='%d/%m/%Y',
                tickangle=45
            )
            st.plotly_chart(fig)
        else:
            st.warning("Nenhum dado disponível para os filtros selecionados.")

    with guia_graficoarea:
        if not df_display.empty:                        
            st.subheader("Faturamento Diário - Gráfico de Áreas Empilhadas")
            fig = px.area(
                df_display,
                x='Data',
                y='Total Faturamento',
                color='Grupo de Receita',
                title='Total de Faturamento por Data'
            )
            st.plotly_chart(fig)
        else:
            st.warning("Nenhum dado disponível para os filtros selecionados.")

# Inicialização correta da session_state
if 'id_grupoacesso' not in st.session_state:
    st.error("Usuário não autenticado. Por favor, faça login.")
    if st.button("Ir para página principal"):
        st.switch_page("main.py")
    st.stop()

if 'permissions' not in st.session_state:
    st.session_state.permissions = get_user_permissions(st.session_state['id_grupoacesso'])

show_sidebar()

conn = create_connection()
if conn:   
    #if 'ano' not in st.session_state:
    #    st.error("Por favor, selecione o ano antes de continuar.")
    #    time.sleep(3)       
    #    st.rerun()

    ano_selecionado  = int(st.session_state['ano']) 
    itens_permitidos = st.session_state.permissions.get('itens_receita', [])
    df_display = fetch_diariofaturamento_data(conn, ano_selecionado, itens_permitidos)
    
    if not itens_permitidos:
        st.warning("Nenhum item permitido foi encontrado para o usuário.")
    elif df_display.empty:
        st.warning("Nenhum dado encontrado para os filtros aplicados.")
    else:
        show_faturamento_data(conn, df_display, ano_selecionado)    

    conn.close()
else:
    st.error("Não foi possível conectar ao banco de dados.")
