import streamlit as st   
import pg8000 
import os
from dotenv import load_dotenv
 
st.set_page_config(page_title="CRUD", page_icon=":computer:",layout="wide") 
load_dotenv()

db_config = {
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }

def get_connection():
    return pg8000.connect(**db_config)

def get_cursor():
    conn = get_connection()
    return conn.cursor(), conn

def execute_query(query, params=None):
    cursor, conn = None, None
    try:
        cursor, conn = get_cursor()        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)  

        if query.strip().upper().startswith(('SELECT', 'WITH')) or 'RETURNING' in query.upper():
            result = cursor.fetchall()
            conn.commit()  
            return result
        else:
            conn.commit()  
            return []  
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao executar query: {query}\nParams: {params}\nErro: {str(e)}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

