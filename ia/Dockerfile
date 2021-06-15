# Uso a imagem disponível no dockerhub para o servidor web uvicorn
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Copy the current directory contents into the container at /app
# Assim, o que vocẽ construiu na máquina de desenvolvimento (host) estará disponível dentro do container
# Dentro do container, tudo estára no diretório /app
# Isto é uma cópia, não um mapeamento dinâmico. A imagem fica independente do host original.
ADD . /app

RUN pip install -r requirements.txt


#Para criar a imagem

    #docker build -t rfb_ceiamin_ia .

#Para abrir o container sem rodar nada e obter um prompt. Você pode usar ls para ver a estrutura dentro do container

    #docker run -it rfb_ceiamin_ia /bin/bash

#Para sair digite

    # exit

# Para rodar o container digite

#docker run  -p 8003:80 --name c_rfb_ceiamin_ia --rm rfb_ceiamin_ia

#Note que na máquina host o serviço estara disponível na porta 8003, mas o servidor web, está atendendo na porta 80
#dentro do container. o "-p", faz o mapeamento.
#O --name define o nome do container que é c_rfb_ceiamin_ia
#O rfb_ceiamin_IA é o nome da imagem
#O container pode ser parado e depois continuar após ter alterado seu estado interno.
#Então container != imagem
#Quando o container é parado, por um ^C ou por um

    # docker stop  c_rfb_ceiamin_ia

#ele continuaria existindo. Você poderia reativá-lo com

    # docker start c_rfb_ceiamin_ia

#poŕem, coloquei a diretiva -rm no comando para eliminar o container.
#Fiz isto para começar do zero de novo com outro docker run
#Se o container já existe, o docker run não funmciona.


# para colocar imagem no dockerhub, se quiser

    #docker login --username=seu_usuario_no_docker_hub
    #docker tag rfb_ceiamin_ia seu_usuario_no_docker_hub/seu_repositorio:rfb_ceiamin_ia
    #docker push rfb_ceiamin_ia seu_usuario_no_docker_hub/seu_repositorio:rfb_ceiamin_ia

# Em qualquer outro lugar você pode pegar a imagem e se o repositório for público, qualquer um pode

    #sudo docker pull rfb_ceiamin_ia seu_usuario_no_docker_hub/seu_repositorio:rfb_ceiamin_ia

#Tendo obtido a imagem, ele pode ser executada, não é preciso ter o código fonte para cria a imagem de novo
#Ela vem com tudo

#Se você clonar o repositório do git, aí você não precisa pegar a imagem, pode reconstruí-la onde estiver.
