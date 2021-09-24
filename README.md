# FastAPI FoodProducts CRUD MongoDB

Projeto para atendimento de desafio para a [coodesh](https://coodesh.com) que consiste na criação de uma REST API com CRUD para produtos do banco de dados aberto da [Open Food Facts](https://br.openfoodfacts.org). O banco de dados aberto é disponibilizado em arquivos zip, que contém documentos JSON com os dados de cada produto. O objetivo é realizar o download e extração diariamente de 100 documentos de cada arquivo e garantir que o mesmo arquivo não seja importado mais de uma vez.


## Estrutura do Projeto e Tecnologias utilizadas

### API
python3.7 + [FastAPI](https://fastapi.tiangolo.com/)

### Database
MongoDB hospedado em um shared cluster na AWS região US EAST.
Backend e CRON Utilizam [PyMongo](https://pymongo.readthedocs.io/en/stable/)

### CRON (Scraper)
python3.7 + [requests](https://docs.python-requests.org/en/latest/) com agendamento diário de scraping dos arquivos utilizando [schedule](https://schedule.readthedocs.io/en/stable/)


### Estratégia de Deploy
Serviços conteinirazados com Docker através de um docker-compose que expõe a API com o uvicorn na porta 5000.

## Instalando o projeto em ambiente local

### Criar e ativar o ambiente virtual (opcional)
Na plataforma windows:<br>
`python -m venv venv`<br>
`venv/scripts/activate.bin`

Na plataforma linux:<br>
`python3 -m venv venv`<br>
`venv/scripts/activate.bin`

### Instalar dependências do projeto

Na plataforma windows:<br>
`pip install -r app/requirements.txt`<br>

Na plataforma linux:<br>
`python3 -m pip install -r app/requirements.txt`<br>

### Iniciando a aplicação

Tenha a certeza de que o diretório app contém arquivo .env com a váriavel MONGO_URI<br>
Esta é a URL de conexão com o Mongo, caso queira rodar na sua máquina utilize a variável no arquivo de exemplo.
Caso deseje utilizar o banco em cloud, entre em contato via e-mail solicitando o acesso.

`uvicorn app.main:app`

Este repositório contém a pasta .vscode que também ajuda a iniciar a aplicação em modo de depuração direto do Visual Studio Code.


### Iniciando a aplicação com o docker

Utilize os seguintes comandos:<br>
`docker-compose build`<br>
`docker-compose up`<br>

### Notas para o deploy

O estado atual da aplicação não é seguro para ambientes cloud, devido a não conter autenticação de nenhum tipo, apesar dos dados serem públicos. Portanto recomenda-se que o deploy seja realizado em um servidor com acesso local aos interessados ou solicitar a implementação da autenticação.
