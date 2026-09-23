# MyBookList

Rede social para listar, salvar e descobrir livros.

## Instalar as dependências

Para instalar as dependências, só é necessário rodar o comando:

### `pip install -r requirements.txt`

### Ambiente virtual

É recomendado criar um [ambiente virtual](https://flask.palletsprojects.com/en/stable/installation/#virtual-environments) para a aplicação.

## Rodar a aplicação

Para rodar a aplicação, execute o seguinte comando:

### `flask --app app run`

Abra [http://localhost:5000](http://localhost:5000) no seu navegador, que será redirecionado para a documentação no Swagger.

### Rodar pelo Docker

É necessário ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução.

Abrir o terminal como administrador no diretório que possui o arquivo **Dockerfile** e criar a imagem:

#### `docker build -t mybooklist-back .`

Em seguida, para rodar o projeto, execute o comando:

#### `docker run -p 5000:5000 mybooklist-back`

Para abrir a aplicação, basta acessar o link [http://localhost:5000/](http://localhost:5000/) no navegador.

## Fluxograma do projeto
