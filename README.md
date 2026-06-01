# Controle-do-Painel
O Projeto possuiem dois sistemas para controlar o acesso e permissao para utilizar o sistema de faturamento.

Sistema de Permissão e Autorização de Acesso
Este projeto é uma aplicação web desenvolvida em Python com a biblioteca Streamlit para gerenciar permissões e autorizações de usuários de forma granular e centralizada. A interface permite a criação de grupos de acesso, a associação de usuários a esses grupos e a definição de quais recursos (chamados de "Painéis" e "Itens de Faturamento") cada grupo pode acessar.

✨ Principais Funcionalidades

  •	Gerenciamento de Grupos de Acesso: Crie, edite e exclua grupos de acesso de forma intuitiva.
  
  •	Associação de Recursos: Associe múltiplos "Painéis" a cada grupo. Para painéis específicos, defina permissões detalhadas para "Itens de Faturamento".
  
  •	Gerenciamento de Usuários: Cadastre, atualize e remova usuários, atribuindo-os a um grupo de acesso específico.
  
  •	Visualização Completa: Uma tela consolidada que exibe todos os grupos, seus painéis, itens de faturamento associados e a lista de usuários com permissão.
  
  •	Interface Reativa: Interface web limpa e funcional construída com Streamlit.
  
  •	Segurança: O e-mail do usuário é validado para pertencer ao domínio @nome_empresa.com de forma automática.

📸 Screenshots
1. Gerenciamento de Grupos de Acesso
Visão geral de todos os grupos, seus painéis, itens de faturamento e ações de edição/exclusão.
2. Criação e Edição de um Grupo
Formulário para criar ou editar um grupo, com seleção de múltiplos painéis e itens.
3. Gerenciamento de Usuários
Tela para cadastrar, editar e remover usuários, associando cada um a um grupo de acesso.
4. Edição de Usuário
Formulário simples para editar o e-mail (parcial) e o grupo de um usuário.
5. Listagem Completa de Permissões
Visão consolidada e expansível de todas as permissões, ideal para auditoria e consulta rápida.
6. Filtrando a Listagem de Permissões
A mesma tela de listagem, agora filtrada por um grupo específico.

🛠️ Tecnologias Utilizadas

  •	Linguagem: Python 3
  
  •	Framework Web: Streamlit
  
  •	Banco de Dados: PostgreSQL
  
  •	Driver de Conexão: pg8000
  
  •	Gerenciamento de Variáveis de Ambiente: python-dotenv

🗂️ Estrutura do Projeto
O projeto está organizado da seguinte forma para separar responsabilidades (Model-View-Controller):

├── Controller/

│   ├── GrupoAcessoController.py        # Lógica para gerenciar grupos e seus recursos

│   └── GrupoAcessoUsuarioController.py   # Lógica para gerenciar usuários e suas associações

├── Model/

│   └── Database.py                     # Lida com a conexão e execução de queries no banco de dados

├── Pages/

│   ├── grupos_acesso.py                # Página para o CRUD de Grupos

│   ├── permissao.py                    # Página para o CRUD de Usuários

│   └── listar_permissaoacesso.py       # Página para a listagem completa de permissões

├── View/

│   ├── AcessoPermitido/

│   │   ├── Listagem.py                 # UI da listagem completa de permissões

│   │   └── Listar.py                   # UI do CRUD de usuários

│   └── GrupoAcesso/

│       └── Listar.py                   # UI do CRUD de grupos (arquivo não fornecido, mas inferido)

├── .env                                # Arquivo para as credenciais do banco (deve ser criado localmente)

├── main.py                             # Ponto de entrada da aplicação Streamlit

└── requirements.txt                    # Dependências do projeto



Sistema de Faturamento 

Apos utilizar o Sistema de Acesso e Permissao, utiliza o Sistema de Faturamento para mostrar os dados do SQLServer que mostrar os graficos( Dashboard ).
