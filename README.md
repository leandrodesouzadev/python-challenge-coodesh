# Python Challenge 20200228

## Introdução

Nesse desafio trabalharemos no desenvolvimento de uma REST API para utilizar os dados do projeto Open Food Facts, que é um banco de dados aberto com informação nutricional de diversos produtos alimentícios.

O projeto tem como objetivo dar suporte a equipe de nutricionistas da empresa Fitness Foods LC para que eles possam revisar de maneira rápida a informação nutricional dos alimentos que os usuários enviam pela aplicação móvel.

### Obrigatório
 
- Trabalhar em um FORK deste repositório em seu usuário;
- O projeto back-end deverá ser desenvolvido usando Python com o framework Django;
- Configurar os testes usando Pytest;
- Documentação para configuração do projeto em ambientes de produção;
 

## O projeto
 
- Criar um banco de dados no Mongo Atlas: https://www.mongodb.com/cloud/atlas
- Criar uma REST API usando Django com as melhores práticas de desenvolvimento
- Integrar a API com o banco de dados MongoDB criado no Atlas para persistir os dados
- Recomendável usar (PyMongo)[https://api.mongodb.com/python/current/] 
- Desenvolver Testes Unitários

### Modelo de Datos:

Para a definição do modelo, consultar o arquivo [products.json](./products.json) que foi exportado do Open Food Facts, um detalhe importante é que temos dois campos personalizados para poder fazer o controle interno do sistema e que deverão ser aplicados em todos os alimentos no momento da importação, os campos são:

- `imported_t`: campo do tipo Date com a dia e hora que foi importado;
- `status`: campo do tipo Enum com os possíveis valores draft, trash e published;

### Sistema do CRON

Para prosseguir com o desafio, precisaremos criar na API um sistema de atualização que vai importar os dados para MongoDB com a versão mais recente do [Open Food Facts](https://br.openfoodfacts.org/data) uma vez ao día. Adicionar aos arquivos de configuração o melhor horário para executar a importação.

A lista de arquivos do Open Food, pode ser encontrada em: 

- https://static.openfoodfacts.org/data/delta/index.txt

Onde cada linha representa um arquivo que está disponível em https://static.openfoodfacts.org/data/delta/{filename}. O nome do arquivo contém o timestamp UNIX da primeira e última alteração contida no arquivo JSON, para que os arquivos possam ser importados (após extracção) em ordem alfabética.

É recomendável utilizar uma Collection secundária para controlar os históricos das importações e facilitar a validação durante a execução.

Nota: Importante lembrar que todos os dados deverão ter os campos personalizados `imported_t` e `status`.

### A REST API

Na REST API teremos um CRUD com os seguintes endpoints:

 - `GET /`: Detalhes da API, se conexão leitura e escritura com a base de datos está OK, horário da última vez que o CRON foi executado, tempo online e uso de memória.
 - `PUT /products/:code`: Será responsável por receber atualizações do Projeto Web
 - `DELETE /products/:code`: Mudar o status do produto para `trash`
 - `GET /products/:code`: Obter a informação somente de um produto da base de dados
 - `GET /products`: Listar todos os produtos da base de dados, adicionar sistema de paginação para não sobrecarregar o `REQUEST`.

Ao terminar os endpoints, configurar os testes usando Pytest.


## [Bônus] DevOps

Depois de um árduo trabalho de desenvolvimento na API chegou a hora mais esperada, 
o lançamento do projeto, é uma das partes mais motivadoras verdade? Então, a equipe de administração de 
sistemas precisará dos mínimos detalhes para configurar o projeto em produção, 
por isso é sua responsabilidade documentar todo o fluxo e facilitar a configuração dos dois projetos com 
tecnologias chaves para rodar em ambientes de Cloud Computing. 

Para isso deveremos configurar:

- Dockerfile
- Docker compose para executar o projeto em ambiente local


## Readme do Repositório
 
- Deve conter o título de cada projeto
- Uma descrição de uma frase
- Como instalar e usar o projeto (instruções)