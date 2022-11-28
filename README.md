# Script de coleta de dados

Este é um script criado com o objetivo de extrair, tratar e armazenar dados presentes em ``https://valorant-api.com/v1/`` e ``https://valorant.fandom.com/wiki/Weapon_Skins``.

# Aplicação complementar

É responsável por consumir os dados gerados a partir deste script, por meio da utilização de filtros contidos na aplicação.

## Front-end 

https://github.com/lavyoliveira/banco-de-dados/

## Back-end 

https://github.com/wendel-nogueira/back-end/tree/dev

### Tecnologias utilizadas:

- [python](https://www.python.org)
- [ORM peewee](http://docs.peewee-orm.com/en/latest/)

### Como executar:


- Etapa 01 - Restaurar o banco de dados:

    Utilizando o arquivo ``script.sql``, você consegue criar as tabelas e roles 
    necessárias para a execução do script.

- Etapa 02 - Variáveis de ambiente:

    Utilizando o arquivo ``.env.example``, você consegue definir os parâmetros de conexão com o banco (host, user, database ...), com isso basta realizar uma cópia do arquivo, modificar a cópia com os parâmetros de conexão e renomear a cópia para ``.env``.

- Etapa 03 - Instalação de bibliotecas

    Bibliotecas utilizadas:

    ````
    requests
    json
    bs4
    re
    peewee
    psycopg2
    os
    dotenv
    ````

    Para realizar a instalação das bibliotecas necessárias basta utilizar o comando ``pip install {nome_da_biblioteca}``.

- Etapa 04 - Execução do projeto

    E por fim caso sejam feitas corretamente as etapas anteriores, basta executar o arquivo ``index.py`` presente na pasta src para inicializar o script :relaxed:.
