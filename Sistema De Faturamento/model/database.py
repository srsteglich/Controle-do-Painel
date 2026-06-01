import streamlit as st
import os
import pg8000
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco de dados
def fetch_postgres_connection():
    try:
        conn =  pg8000.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except pg8000.OperationalError as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def get_user_permissions(id_grupoacesso):
    conn = fetch_postgres_connection()
    cursor = conn.cursor()
    try:
        # Consulta para obter os painéis permitidos
        cursor.execute("""SELECT id_painel 
                            FROM ADV_GrupoAcesso_Painel 
                            WHERE id_grupoacesso = %s""", (id_grupoacesso,))
        paineis_permitidos = [row[0] for row in cursor.fetchall()]

        cursor.execute("""SELECT a.id_itens_grupo_receita, b.nm_itens_grupo_receita  
                          FROM ADV_ItensFaturamentoBruto a
                          JOIN ADV_ItensGrupoReceita b 
                            ON a.id_itens_grupo_receita = b.id_itens_grupo_receita 
                          WHERE a.id_grupoacesso = %s""", (id_grupoacesso,))

        resultados = cursor.fetchall()
        itens_permitidos = [row[0] for row in resultados]
        nomes_itens = {row[0]: row[1] for row in resultados}

        return {
            'paineis': paineis_permitidos,
            'itens_receita': itens_permitidos,
            'nomes_itens': nomes_itens
        }
    except Exception as e:
        st.error(f"Erro ao buscar permissões: {e}")
        return {
            'paineis': paineis_permitidos,
            'itens_receita': [],
            'nomes_itens': {}}
    finally:
        cursor.close()
        conn.close()

def get_group_name(id_grupoacesso):
    conn = fetch_postgres_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT nm_grupoacesso FROM ADV_GrupoAcesso 
                            WHERE id_grupoacesso = %s""", (id_grupoacesso,))
        result = cursor.fetchone()
        return result[0] if result else "Grupo Desconhecido"
    finally:
        cursor.close()
        conn.close()
