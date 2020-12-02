Estando no diretório raiz do backend (dirtorio_do_projeto/backend) é possoivel dar alguns comandos

Para subir um servidor local que atende na porta 8001 e disponibiliza a API de sua documentação para testes manuais.

    uvicorn main:app --reload --port 8001

Para ver a documentação

    http://127.0.0.1:8001/docs
    http://127.0.0.1:8001/redocs

Para rodar no docker, leia o arquivo Dockerfile


