/*  Ciar Banco de Dados  */
CREATE DATABASE Painel;

/*1) Criar tabela Painel para o Sistema Faturamento e o Permissão - O Painel fica dentro do Programa 'Faturamento'*/
CREATE TABLE ADV_Painel (
    id_painel SERIAL PRIMARY KEY,
    nm_painel VARCHAR(100) NOT NULL
);

/* Colocar os nomes dos Panieis nesta ordem    */ 
INSERT INTO adv_painel(nm_painel)
VALUES ('Painel Top 10 Clientes'), ('Painel dos Clientes e Grupos de Receitas'), ('Painel dos Faturamentos Brutos'), ('Painel Mensal dos Faturamentos Brutos'), 
       ('Painel Receita Bruta Líquida de Vendas'), ('Painel Diário dos Faturamentos Brutos')

SELECT * FROM adv_painel       



/*2) Criar tabela GrupoAcesso para Sistema Faturamento e o nome do Grupo de Acesso do Permissão* */
CREATE TABLE ADV_GrupoAcesso (
    id_grupoacesso SERIAL PRIMARY KEY,
    nm_grupoacesso VARCHAR(100) NOT NULL
);       

SELECT * FROM adv_grupoacesso



/*3) Criar tabela GrupoAcesso_Painel para Sistema Faturamento e o acesso ao grupo com painel */ 
CREATE TABLE ADV_GrupoAcesso_Painel (
    id_grupoacesso INTEGER REFERENCES ADV_GrupoAcesso(id_grupoacesso),
    id_painel INTEGER REFERENCES ADV_Painel(id_painel),
    PRIMARY KEY (id_grupoacesso, id_painel)
);

SELECT * FROM adv_grupoacesso_painel



/*4) Criar tabela GrupoAcesso_Painel para Sistema Faturamento e o acesso ao grupo com o usuario com e-mail */ 
CREATE TABLE ADV_GrupoAcesso_Usuario (
    id_usuario SERIAL PRIMARY KEY,
	id_grupoacesso INT REFERENCES ADV_GrupoAcesso(id_grupoacesso),
    nm_email VARCHAR(100)    
);

SELECT * FROM adv_grupoacesso_usuario


/*5) Criar ADV_ItensGrupoReceita no lugar DItensGrupoReceita   */ 
CREATE TABLE ADV_ItensGrupoReceita(
	id_itens_grupo_receita SERIAL PRIMARY KEY,
	nm_itens_grupo_receita VARCHAR(100) NOT null
);

INSERT INTO ADV_ItensGrupoReceita(nm_itens_grupo_receita)
VALUES ('Renovação'), ('USO E CONSUMO'), ('ADIANTAMENTOS'), ('Plotter'), ('Sala de Corte'), ('SERVIÇOS'),
	   ('SW Outros'), ('Academy'), ('Peças e Serviços'), ('ICF'), ('Digiflash'), ('Consultorias e Implantações'),
	   ('LICITACAO'), ('SW MRR'), ('Franquias'), ('SW ARR'), ('Royalties'), ('Trial'), ('NÃO APLICÁVEL')

SELECT * FROM adv_itensgruporeceita


/*6) Criar tabela ADV_ItensFaturamentoBruto para Sistema de Faturamento que é conposta do itens da receita  */ 
CREATE TABLE ADV_ItensFaturamentoBruto (
    id_itensfatura SERIAL PRIMARY KEY,
    id_grupoacesso INTEGER NOT NULL,
    id_painel INTEGER NOT NULL,
    id_itens_grupo_receita INTEGER NOT NULL,

    -- FK para tabela de itens de receita
    CONSTRAINT fk_id_itens_grupo_receita
        FOREIGN KEY (id_itens_grupo_receita)
        REFERENCES ADV_ItensGrupoReceita(id_itens_grupo_receita),  /* precisa modificar DItensGrupoReceita, pois tem no servidor Dw   */

    -- FK simples para ADV_GrupoAcesso (opcional, veja observação abaixo)
    CONSTRAINT fk_grupoacesso 
        FOREIGN KEY (id_grupoacesso)
        REFERENCES ADV_GrupoAcesso(id_grupoacesso),

    -- FK simples para ADV_Painel (opcional, veja observação abaixo)
    CONSTRAINT fk_painel 
        FOREIGN KEY (id_painel)
        REFERENCES ADV_Painel(id_painel),

    -- FK composta para tabela intermediária grupoacesso + painel
    CONSTRAINT fk_grupoacesso_painel
        FOREIGN KEY (id_grupoacesso, id_painel)
        REFERENCES ADV_GrupoAcesso_Painel(id_grupoacesso, id_painel)
);

ALTER TABLE ADV_ItensFaturamentoBruto
ADD CONSTRAINT uq_grupo_painel_item UNIQUE (id_grupoacesso, id_painel, id_itens_grupo_receita);
