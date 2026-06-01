from Model.Database import execute_query

class GrupoAcessoController:    
    @staticmethod
    def get_all_paineis():
        query = """SELECT id_painel, nm_painel 
                    FROM ADV_Painel"""
        return execute_query(query)
    
    @staticmethod
    def get_grupo_by_id(grupo_id):
        query = """SELECT id_grupoacesso, nm_grupoacesso 
                    FROM ADV_GrupoAcesso 
                    WHERE id_grupoacesso = %s"""
        result = execute_query(query, (grupo_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_paineis_do_grupo(grupo_id):
        query = """SELECT p.id_painel, p.nm_painel 
                    FROM ADV_GrupoAcesso_Painel gp
                    JOIN ADV_Painel p ON gp.id_painel = p.id_painel
                    WHERE gp.id_grupoacesso = %s"""
        return execute_query(query, (grupo_id,))
    
    @staticmethod
    def get_itens_faturamento_by_grupo_painel(grupo_id, id_painel):
        query = """SELECT id_itens_grupo_receita 
                    FROM ADV_ItensFaturamentoBruto 
                    WHERE id_grupoacesso = %s AND id_painel = %s"""
        result = execute_query(query, (grupo_id, id_painel))
        return [item[0] for item in result]
    
    @staticmethod
    def create_grupo(nome, id_paineis, painel_itens=None):       
        try:
            query = """INSERT INTO ADV_GrupoAcesso (nm_grupoacesso)
                        VALUES (%s) RETURNING id_grupoacesso"""
            grupo_id = execute_query(query, (nome,))[0][0]
       
            for id_painel in id_paineis:
                execute_query("""INSERT INTO ADV_GrupoAcesso_Painel (id_grupoacesso, id_painel)
                                    VALUES (%s, %s)""", (grupo_id, id_painel))            

            if painel_itens:
                # Usa um set para garantir que não insere item_id duplicado por painel
                ja_inseridos = set()
                for id_painel, itens in painel_itens.items():
                    for item_id in itens:
                        chave = (id_painel, item_id)
                        if chave not in ja_inseridos:
                            execute_query("""INSERT INTO ADV_ItensFaturamentoBruto 
                                            (id_grupoacesso, id_painel, id_itens_grupo_receita)
                                            VALUES (%s, %s, %s)""", (grupo_id, id_painel, item_id))
                            ja_inseridos.add(chave)
            return grupo_id
        except Exception as e:
            print(f"Erro ao criar grupo: {str(e)}")
            raise            

    @staticmethod
    def update_grupo(grupo_id, nome, id_paineis, painel_itens=None):
        try:
            execute_query("UPDATE ADV_GrupoAcesso SET nm_grupoacesso = %s WHERE id_grupoacesso = %s", (nome, grupo_id))           
            current_paineis = [p[0] for p in GrupoAcessoController.get_paineis_do_grupo(grupo_id)]           
            for id_painel in set(current_paineis) - set(id_paineis):
                execute_query("""DELETE FROM ADV_GrupoAcesso_Painel 
                                    WHERE id_grupoacesso = %s AND id_painel = %s""", (grupo_id, id_painel))            
            for id_painel in set(id_paineis) - set(current_paineis):
                execute_query("""INSERT INTO ADV_GrupoAcesso_Painel (id_grupoacesso, id_painel) VALUES (%s, %s)""",
                    (grupo_id, id_painel))   

            if painel_itens:
                for id_painel in painel_itens.keys():
                    execute_query("""DELETE FROM ADV_ItensFaturamentoBruto 
                                     WHERE id_grupoacesso = %s AND id_painel = %s""", (grupo_id, id_painel))
                    for item_id in painel_itens[id_painel]:
                        execute_query("""INSERT INTO ADV_ItensFaturamentoBruto 
                                         (id_grupoacesso, id_painel, id_itens_grupo_receita)
                                         VALUES (%s, %s, %s)""", (grupo_id, id_painel, item_id))
            return True
        
        except Exception as e:
            print(f"Erro detalhado ao atualizar grupo: {str(e)}")
            raise    

    @staticmethod
    def delete_grupo(grupo_id):
        try:
            execute_query("DELETE FROM ADV_ItensFaturamentoBruto WHERE id_grupoacesso = %s", (grupo_id,))        
            execute_query("DELETE FROM ADV_GrupoAcesso_Painel WHERE id_grupoacesso = %s", (grupo_id,))           
            execute_query("DELETE FROM ADV_GrupoAcesso WHERE id_grupoacesso = %s", (grupo_id,))            
            return True
        except Exception as e:
            print(f"Erro ao excluir grupo: {str(e)}")
            return False    

    @staticmethod
    def get_all_grupos():
        query = """SELECT g.id_grupoacesso, g.nm_grupoacesso,
                    COALESCE(STRING_AGG(DISTINCT p.nm_painel, ', 
                    ' ORDER BY p.nm_painel), 'Nenhum') AS paineis,
                    COALESCE((SELECT STRING_AGG(DISTINCT d.nm_itens_grupo_receita, ', 
                    ' ORDER BY d.nm_itens_grupo_receita)
                    FROM ADV_ItensFaturamentoBruto ifb
                    JOIN ADV_ItensGrupoReceita d ON ifb.id_itens_grupo_receita = d.id_itens_grupo_receita
                    WHERE ifb.id_grupoacesso = g.id_grupoacesso), 'Nenhum') AS itens_faturamento
                    FROM ADV_GrupoAcesso g
                    LEFT JOIN ADV_GrupoAcesso_Painel gp ON g.id_grupoacesso = gp.id_grupoacesso
                    LEFT JOIN ADV_Painel p ON gp.id_painel = p.id_painel
                    GROUP BY g.id_grupoacesso
                    ORDER BY g.nm_grupoacesso"""  
        return execute_query(query)
    
    @staticmethod
    def get_itens_grupo_receita():
        query = """SELECT id_itens_grupo_receita, nm_itens_grupo_receita 
                    FROM ADV_ItensGrupoReceita     
                    ORDER BY nm_itens_grupo_receita"""
        return [{'id_itens_grupo_receita': row[0], 'nm_itens_grupo_receita': row[1]} for row in execute_query(query)]
    
    @staticmethod
    def get_itens_faturamento_formatados(grupo_id):
        try:
            query = """SELECT id_itens_receita 
                        FROM ADV_ItensFaturamentoBruto 
                        WHERE id_grupoacesso = %s"""
            itens_ids = [item[0] for item in execute_query(query, (grupo_id,))]            
            if not itens_ids:
                return "Nenhum"
                               
        except Exception as e:
            print(f"Erro ao obter itens: {str(e)}")        
        return "Nenhum"    