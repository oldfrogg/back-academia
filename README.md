# back-academia

A aplicação tem como objetivo fazer o controle de cadastro dos alunos da Academia da PUC.
Ela tem as opções de 


Para executar a aplicação, é recomendável realizar a instalação dos pacotes necessários e executá-lo em um ambiente virtual.

Para criar um ambiente virtual é necessário navegar no terminal até o diretório da aplicação e dar o comando:
    > python -m venv venv

Além de criar é necessário deixá-lo ativado para a instalação das bibliotecas e execução da aplicação.

Para ativar o ambiente virtual, faça o  seguinte:
    No Windows:
        > .\venv\Scripts\activate

    No Linux:
        > source venv/bin/activate

Pronto, agora deve aparecer um "(venv)" no início da sua linha de comando no terminal. 

Isso indica que o ambiente virtual está ativo.

Caso queira desativá-lo, basta executar:
    > deactivate


Agora, com o ambiente virtual ativo, você deve instalar as bibliotecas necessárias na aplicação.

Para isso, execute o comando:
    > pip install -r requirements.txt

Com isso, a aplicação estará pronta para a execução.

O banco de dados utilizado é o SQLite, o arquivo db.sqlite3 será criado em sua máquina na primeira execução do programa.

Por fim, para executar a aplicação, basta executar o flask da seguinte forma:
    > flask run

Com isso a aplicação ficará ativa em um servidor local. Você poderá acessá-lo através do navegador utilizando:
    http://localhost:5000
ou:
    http://127.0.0.1:5000/

Você terá 3 escolhas de documentação, mas é recomendável a utilização do Swagger.
