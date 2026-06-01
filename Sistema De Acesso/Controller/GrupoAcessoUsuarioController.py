from Model.Database import execute_query

class GrupoAcessoUsuarioController:
    
    @staticmethod
    def create_usuario(email, id_grupoacesso):
        query = """INSERT INTO ADV_GrupoAcesso_Usuario (nm_email, id_grupoacesso) VALUES (%s, %s)
                    RETURNING id_usuario"""
        try:
            result = execute_query(query, (email, id_grupoacesso))
            return result[0][0] if result else None
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            raise

    @staticmethod
    def get_all_usuarios():
        query = """SELECT u.id_usuario, u.nm_email, g.id_grupoacesso, g.nm_grupoacesso
                    FROM ADV_GrupoAcesso_Usuario u
                    JOIN ADV_GrupoAcesso g ON u.id_grupoacesso = g.id_grupoacesso
                    ORDER BY u.nm_email"""
        return execute_query(query)

    @staticmethod
    def get_usuario_by_id(usuario_id):
        query = """SELECT id_usuario, nm_email, id_grupoacesso
                    FROM ADV_GrupoAcesso_Usuario
                    WHERE id_usuario = %s"""
        result = execute_query(query, (usuario_id,))
        return result[0] if result else None

    @staticmethod
    def update_usuario(usuario_id, email, id_grupoacesso):
        query = """UPDATE ADV_GrupoAcesso_Usuario SET nm_email = %s, id_grupoacesso = %s
                    WHERE id_usuario = %s"""
        try:
            execute_query(query, (email, id_grupoacesso, usuario_id))
            return True
        except Exception as e:
            print(f"Erro ao atualizar usuário: {str(e)}")
            return False

    @staticmethod
    def delete_usuario(usuario_id):
        query = """DELETE FROM ADV_GrupoAcesso_Usuario 
                    WHERE id_usuario = %s"""
        try:
            execute_query(query, (usuario_id,))
            return True
        except Exception as e:
            print(f"Erro ao excluir usuário: {str(e)}")
            return False

    @staticmethod
    def get_all_grupos():
        query = """SELECT id_grupoacesso, nm_grupoacesso 
                    FROM ADV_GrupoAcesso 
                    ORDER BY nm_grupoacesso"""
        return execute_query(query)
    
    @staticmethod
    def get_permissoes_completas():
        query = """WITH grupos_paineis AS 
                    (SELECT g.id_grupoacesso, g.nm_grupoacesso,
                        STRING_AGG(DISTINCT p.nm_painel, ', ' 
                        ORDER BY p.nm_painel) AS paineis,
                        BOOL_OR(p.id_painel BETWEEN 2 AND 6) AS tem_painel
                      FROM ADV_GrupoAcesso g
                      LEFT JOIN ADV_GrupoAcesso_Painel gp ON g.id_grupoacesso = gp.id_grupoacesso
                      LEFT JOIN ADV_Painel p ON gp.id_painel = p.id_painel
                      GROUP BY g.id_grupoacesso, g.nm_grupoacesso), itens_faturamento AS 
                    (SELECT ifb.id_grupoacesso, STRING_AGG(DISTINCT d.nm_itens_grupo_receita, ', ' 
                      ORDER BY d.nm_itens_grupo_receita) AS itens
                      FROM ADV_ItensFaturamentoBruto ifb
                      JOIN ADV_ItensGrupoReceita d ON ifb.id_itens_grupo_receita = d.id_itens_grupo_receita
                      GROUP BY ifb.id_grupoacesso), usuarios_grupo AS 
                    (SELECT id_grupoacesso, STRING_AGG(nm_email, ', ' 
                      ORDER BY nm_email) AS usuarios
                      FROM ADV_GrupoAcesso_Usuario
                      GROUP BY id_grupoacesso)
                    SELECT gp.id_grupoacesso, gp.nm_grupoacesso, gp.paineis,
                        CASE 
                        WHEN gp.tem_painel THEN COALESCE(if.itens, 'Nenhum item selecionado')
                        ELSE 'Não aplicável'
                        END AS itens_faturamento,
                        COALESCE(ug.usuarios, 'Nenhum usuário') AS usuarios
                      FROM grupos_paineis gp
                      LEFT JOIN itens_faturamento if ON gp.id_grupoacesso = if.id_grupoacesso
                      LEFT JOIN usuarios_grupo ug ON gp.id_grupoacesso = ug.id_grupoacesso
                      ORDER BY gp.nm_grupoacesso"""
        return execute_query(query)    