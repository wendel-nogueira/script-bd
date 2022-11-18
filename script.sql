-- criação do schema
CREATE SCHEMA private;

-- criação de um usuario a nivel de schema
CREATE ROLE dba_banco_de_dados;
GRANT ALL ON SCHEMA private TO dba_banco_de_dados;
CREATE USER programador_bd1 WITH PASSWORD 'trabalhovanessa1';
GRANT dba_banco_de_dados TO programador_bd1;

-- criação de um usuario a nivel de schema, entretanto, apenas com permissão de inserção
CREATE ROLE aplicacao_popular;
GRANT INSERT ON ALL TABLES IN SCHEMA private TO aplicacao_popular;
CREATE USER aplicacacao_popular_usuario1 WITH PASSWORD 'trabalhovanessa1';
GRANT aplicacao_popular TO aplicacacao_popular_usuario1;

-- criação de um usuario a nivel de schema, apenas com permissão de leitura
CREATE ROLE aplicacao_relatorio;
GRANT SELECT ON ALL TABLES IN SCHEMA private TO aplicacao_relatorio;
CREATE USER aplicacao_relatorio_usuario1 WITH PASSWORD 'trabalhovanessa1';
GRANT aplicacao_relatorio TO aplicacao_relatorio_usuario1;

-- a partir daqui, conecte-se ao usuario programador_bd1 e crie as tabelas

CREATE TABLE private.Bundle(
	id text PRIMARY KEY,
	name varchar(100),
	description varchar(100),
	icon varchar(100)
);

CREATE TABLE private.Spray(
    id text PRIMARY KEY,
    id_bundle text,
    name varchar(100),
    category varchar(100),
    theme varchar(100),
	icon varchar(100),
    animation varchar(100),
    FOREIGN KEY (id_bundle) REFERENCES private.Bundle(id) ON DELETE RESTRICT
);

CREATE TABLE private.Title(
    id text PRIMARY KEY,
    id_bundle text,
    name varchar(100),
    txt text,
    FOREIGN KEY (id_bundle) REFERENCES private.Bundle(id) ON DELETE RESTRICT
);

CREATE TABLE private.Buddies(
    id text PRIMARY KEY,
    id_bundle text,
    theme varchar(100),
    icon varchar(100),
    name varchar(100),
    FOREIGN KEY (id_bundle) REFERENCES private.Bundle(id) ON DELETE RESTRICT
);

CREATE TABLE private.Cards(
    id text PRIMARY KEY,
    id_bundle text,
    theme varchar(100),
    name varchar(100),
    icon varchar(100),
    FOREIGN KEY (id_bundle) REFERENCES private.Bundle(id) ON DELETE RESTRICT
);

CREATE TABLE private.Weapons(
    id text PRIMARY KEY,
    name varchar(100), 
    category varchar(100), 
    icon varchar(100)
);

CREATE TABLE private.WeaponsInfo(
    id_weapon text,
    info varchar(200),
    FOREIGN KEY (id_weapon) REFERENCES private.Weapons(id) ON DELETE RESTRICT
);

CREATE TABLE private.Skins(
    id text PRIMARY KEY,
    id_bundle text,
    id_weapon text,
    name varchar(100),
    tier varchar(100),
    theme varchar(100),
    icon varchar(100),
    price float,
    FOREIGN KEY (id_bundle) REFERENCES private.Bundle(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_weapon) REFERENCES private.Weapons(id) ON DELETE RESTRICT
);

CREATE TABLE private.Level(
    id_skin text,
    name varchar(200),
    icon varchar(200),
    FOREIGN KEY (id_skin) REFERENCES private.Skins(id) ON DELETE RESTRICT
);

CREATE TABLE private.Chroma(
    id_skin text,
    name varchar(200),
    icon varchar(200),
    FOREIGN KEY (id_skin) REFERENCES private.Skins(id) ON DELETE RESTRICT
);
