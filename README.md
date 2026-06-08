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


________________________________________________________________________________________________________________________________________________________

As Telas do Sistemas de Acesso:

<img width="886" height="382" alt="image" src="https://github.com/user-attachments/assets/915f6dc7-5691-4630-b0ac-fa6c470feae5" />

Figura 1: Tela de Grupos de Acesso, exibindo a listagem dos grupos cadastrados, seus painéis associados e os respectivos itens de faturamento.


<img width="886" height="383" alt="image" src="https://github.com/user-attachments/assets/0fdcfce8-0e7c-4664-b7a8-aaa4d03ba1cb" />

Figura 2: Tela de Grupos de Acesso, exibindo a listagem dos grupos cadastrados, seus painéis associados e os respectivos itens de faturamento.


<img width="886" height="377" alt="image" src="https://github.com/user-attachments/assets/a4f51d23-7c80-4440-a7bf-75a737945227" />

Figura 3: Filtro de listagem completa de permissões por grupo selecionado.


<img width="886" height="379" alt="image" src="https://github.com/user-attachments/assets/1bab5c76-716a-4ae8-8aaa-c568d82d41c4" />

Figura 4: Visualização do grupo 'Dados' filtrado, exibindo os painéis associados, itens de faturamento e usuários vinculados.


<img width="886" height="380" alt="image" src="https://github.com/user-attachments/assets/5d561fea-8619-4820-bb6e-4193d559625a" />

Figura 5: Visualização do grupo 'Analista' filtrado, exibindo os painéis associados, itens de faturamento e usuários vinculados.

________________________________________________________________________________________________________________________________________________________

As Telas do Sistemas de Faturamentos (Graficos):

<img width="886" height="415" alt="image" src="https://github.com/user-attachments/assets/cae2bd59-2f47-4fa0-a58a-b8723192ae3e" />

Figura 1: Tela inicial do Painel de Faturamentos e Clientes. O sistema realiza a identificação automática do e-mail do usuário logado e carrega suas permissões e grupos de acesso correspondentes.


<img width="886" height="415" alt="image" src="https://github.com/user-attachments/assets/d23c2343-c3b9-494f-a0c4-9609732f5c69" />

Figura 2: Listagem e detalhamento do faturamento por cliente e grupo de receita, com dados consolidados do ano selecionado.


<img width="886" height="415" alt="image" src="https://github.com/user-attachments/assets/7d9f7c8a-222b-43df-addf-0cfd3009d276" />

Figura 3: Visualização em Gráfico de Barras do total de receita por cliente e por grupo de faturamento.


<img width="886" height="415" alt="image" src="https://github.com/user-attachments/assets/9a99a194-8acb-41ae-934d-30ec47ec98b6" />

Figura 4: Gráfico de Pizza exibindo a distribuição percentual de participação por Grupo de Receita.


<img width="886" height="416" alt="image" src="https://github.com/user-attachments/assets/0c560920-39d9-4ac3-b407-b5d573c66eb8" />

Figura 5: Na tela Faturamento Mensal, filtrei os Grupo de Receita apenas Plotter e Sala de Corte com os meses de Março à Julho de 2024, mostram a lista da Tabela ordenadas.


<img width="886" height="416" alt="image" src="https://github.com/user-attachments/assets/df88b28f-f0fa-4b1f-b226-94a6a7deae25" />

Figura 6: Na tela Faturamento Mensal, filtrei os Grupo de Receita apenas Plotter e Sala de Corte com os meses de Março à Julho de 2024, mostram Gráficos de Linha ordenadas por meses escolhidos.


<img width="886" height="417" alt="image" src="https://github.com/user-attachments/assets/bb4c0053-1105-4538-ab78-920ef42f2749" />

Figura 7: Na tela Faturamento Mensal, filtrei os Grupo de Receita apenas Plotter e Sala de Corte com os meses de Março à Julho de 2024, mostram Área ordenadas por meses escolhidos.

