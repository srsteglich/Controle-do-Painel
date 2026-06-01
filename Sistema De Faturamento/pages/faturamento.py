import streamlit as st
import pandas as pd
import plotly.express as px
from model.sql_conn import create_connection, fetch_faturamento_data, fetch_faturamentoAtualAnter_data
from model.database import get_group_name, get_user_permissions  

st.set_page_config(
    page_title="Faturamento Bruto",  
    page_icon=":📈", 
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
    ano_selecionado  = int(st.session_state['ano'])
    df_dis = fetch_faturamentoAtualAnter_data(conn, ano_selecionado)
    # Transformar DataFrame em lista de dicionários
    df_dis = df_dis.to_dict('records')
    # Separar os dados por ano
    data_atual = [item for item in df_dis if item["ano"] == ano_selecionado]
    data_anter = [item for item in df_dis if item["ano"] == ano_selecionado-1]

    st.header("Faturamento Brutos & Comparação")
    st.divider()

    st.subheader("Comparação dos 4 melhores Itens de Receita")
    if len(data_atual) < 4:
        st.warning(f"Não há dados suficientes para exibir os 4 melhores itens de receita no ano {ano_selecionado}.")
    else:
        for i in range(4):
            item_atual = data_atual[i]
            if i < len(data_anter):
                item_anter = data_anter[i]
                delta = item_atual["total_vl_total_nf"] - item_anter["total_vl_total_nf"]
                delta_porcentual = (delta / item_anter['total_vl_total_nf']) * 100 if item_anter['total_vl_total_nf'] != 0 else 0
            else:
                # Se não houver dados para o ano anterior, definir delta como None
                item_anter = {'total_vl_total_nf': 0}
                delta = None
                delta_porcentual = None
            col1, col2 = st.columns(2)
            with col1:
                # Verificar se o ano anterior está vazio    
                if item_anter['total_vl_total_nf'] != 0 and delta is not None:
                    st.metric(
                        label=f"{item_atual['nm_itens_grupo_receita']}",
                        #value=f"{locale.format_string('%.2f', item_atual['total_vl_total_nf'], grouping=True)}",
                        #delta=f"{locale.format_string('%.2f', delta, grouping=True)}",                                  
                        value=f"{item_atual['total_vl_total_nf']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if item_atual is not None else "R$ 0",
                        delta=f"{delta:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                        delta_color="normal")
                else:
                    st.metric(
                        label=f"{item_atual['nm_itens_grupo_receita']}",
                        #value=f"{locale.format_string('%.2f', item_atual['total_vl_total_nf'], grouping=True)}",
                        value=f"{item_atual['total_vl_total_nf']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if item_atual is not None else "R$ 0",
                        delta=None,                                                              
                        delta_color="normal",
                        help="Não há dados disponíveis para o ano anterior.")
            with col2:
                if item_anter['total_vl_total_nf'] != 0 and delta_porcentual is not None:
                    st.metric(
                        label="Variação Percentual",
                        #value = f"{locale.format_string('%.2f', delta_porcentual, grouping=True)}%",   
                        value=f"{delta_porcentual:.2f}%".replace(".", ","),                
                        delta=None,        
                        delta_color="normal",
                        help="O Porcentual do ano anterior")
                else:
                    st.metric(
                        label="Variação Percentual",
                        value="0.00%", 
                        delta=None,
                        delta_color="normal",
                        help="Não há dados disponíveis para o ano anterior.")  

        st.subheader("📦 Filtrar os Grupos")
        df_display = fetch_faturamento_data(conn, ano_selecionado, itens_permitidos)   
        if df_display.empty:
            st.warning("Nenhum dado encontrado para os grupos permitidos.")
            st.stop()

        df_display['Total de Faturamento'] = df_display['total_vl_total_nf'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
        # Renomeiar as colunas
        df_display = df_display.rename(columns={
            'fb_id_itens_grupo_receita': 'Item do Grupo',
            'nm_itens_grupo_receita': 'Nome do Grupo',
            'total_vl_total_nf': 'Total Faturamento'})

        grupos_selecionados = st.multiselect(
            "📦 Selecione o(s) Grupo(s) de Receita:",
            options=df_display["Nome do Grupo"].unique(),
            default=df_display["Nome do Grupo"].unique())
        # Aplicar filtro
        df_filtrado = df_display[df_display["Nome do Grupo"].isin(grupos_selecionados)]
        # Configurar as guias
        st.subheader("Tabelas e Gráficos do Banco de Dados")
        guia_tabela, guia_grafico,  guia_graficopie= st.tabs(["📊 Tabela", "📈 Gráfico de Barra", "🥧 Gráfico da Pizza" ])       

        with guia_tabela: 
            st.subheader(f" 📋 Listagem de Faturamento Bruto - {ano_selecionado}")
            st.dataframe(df_filtrado[['Item do Grupo', 'Nome do Grupo', 'Total de Faturamento']])

        with guia_grafico:
            # Preparar dados para gráfico de barras
            st.subheader(f"Gráfico de Barra em {ano_selecionado}")
            pro_quant = df_filtrado.groupby("Nome do Grupo")["Total Faturamento"].sum().reset_index()
            pro_quant = pro_quant.sort_values(by="Total Faturamento", ascending=True)                
            fig = px.bar(
                pro_quant, 
                x="Total Faturamento", 
                y="Nome do Grupo",
                title="📈 Total por Grupo de Receita",
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)                    

        with guia_graficopie:
            st.subheader(f"Gráfico de Pizza em {ano_selecionado}")
            # Cálculo para gráfico de pizza
            df_filtrado['porcentagem'] = (df_filtrado["Total Faturamento"] / df_filtrado["Total Faturamento"].sum()) * 100
            threshold = 8
            outros = df_filtrado[df_filtrado['porcentagem'] < threshold].sum(numeric_only=True)
            outros_label = pd.DataFrame({
                'Nome do Grupo': ['Outros'],
                'Total Faturamento': [outros['Total Faturamento']],
                'porcentagem': [outros['porcentagem']]
            })
            df_maiores = df_filtrado[df_filtrado['porcentagem'] >= threshold]
            df_final = pd.concat([df_maiores, outros_label], ignore_index=True)                
            fig = px.pie(
                df_final,
                names='Nome do Grupo',
                values='Total Faturamento',
                title="🥧 Distribuição por Grupo",
                hole=0.3
            )
            st.plotly_chart(fig)

    conn.close()
else:
    st.error("Não foi possivel conectar ao banco de dados.")
