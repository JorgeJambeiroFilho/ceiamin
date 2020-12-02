# ceiamin
Este é um repositório para exemplificação da estrutura de um projeto do mínimo do CEIA disponível via web

A Inteligência Artifical não flutua. Para ser útil ela tem que se ligar a outros sistemas. Aqui exemplificamos esta ligação usando frameworks típicos de 2020.

Para colocar esta exemplificação em funcionamento você precisa ter um ambiente que possua git e docker instalados.

Uso:

  Vá para o diretório que você deseja que seja o pai deste repositório em sua máquina.
  Digite
  
      git clone https://github.com/JorgeJambeiroFilho/ceiamin
  
  O repositório será clonado em sua máquina
  Digite 
  
      cd ceiamin
  para entrar no repositorio
  
  Execute o script 
  
      setup.sh    

   para preparar as imagens docker
   
   Execute 
   
        run.sh
        
  O script acima, apenas define uma variável de configuração e chama    
        
        docker-compose up 
   
   para executar a aplicação completa.

        docker-compose down
   
   A execuçao vai para se bater CRTL-C, mas para limpar tudo e poder executar de novo sem problemas digite:

Você pode acessar a aplicação usando um navegador pelo endereço 127.0.0.1/frontend

Neste momento, vários containers docker estarão em execução. Eles estao se comunicando como se fossem máquinas separadas.

Temos:

  Um container com o frontend em Python.

      Este container serve a página html inicial, um CSS para configuração do estilo da pagina e o código Javascript da aplicação cliente.
      Como são arquivos estáticos, poderíamos serví-los diretamente pelo container nginx que aparecerá a frente, mas poderíamos aproveitar este container para
      transformar as páginas usando templates. Então devemos deixar este recurso disponível.
      O front end atende a um usuário humano usando navegador.
      O Código Javascript se comunica com o backend e usa vue.js para gerar a interface com o usuário dinamicamente.
      
  Um container com o backend em Python
  
      Este container oferece uma API web. Ela é implementada e documentada com uso de FastAPI. Ele pode ser acessado por qualquer aplicação não relacionado com 
      o presente projeto, mas que decida usar seus serviços.
      Então é um container para atender a maquinas e não a humanos.
      O Javascript servidor pelo frontend e executado no navegador faz chamadas ao backend, geralmente, passando informações em formato JSON e recebendo
      informações em JSON.
      O backend, também tem o papel de broker, dividindo a carga das solicitações entre as instância de IA e comandando estas instâncias para que elas 
      se retreinem quando conveniente.
      
  Três containers com uma IA exemplo
  
      Estes containers são acessados via API pelo backend, ou seja, a comunicação ocorre diretamente entre contaners sem participação da máquina do usuário.
      Tods estes containers fazem a mesma coisa. Eles treinam quando são comandados e respondem a solicitação usuando os modelos treinados quando o backend
      assim o pede.
      A comunicação entre o backend e os container de IA também é feita com uso de FastAPI / JSON.
      Note que um container pode estar treinando enquanto outros atendem a solicitações. O atendimento nunca para.
      As IAs leêm os dados para treinamento acessando o container que tem o BD.
      Os dados processadosa (modelos treinados) são armazenados de modo diferente para cada IA. No exemplo são arquivos simples.
      
  Um container com nginx
  
      O frontend e o backend não devem ser expostos na web, pois não tem todos os recursos de segurança e escalabilidade.
      Em vez disto usamos o servidor nginx como proxy reverso e fazemos com que ele atenda aos usuários e redirecione os pedido para o frontend e o backend.
      O nginx também pode agir como balanceador de nível 4 (rede), por exemplo dividindo a carga entre várias instância do frontend e do backend.
      
      
  Não temos um container com balanceador nível 7, mas podemos ter    
      
      Como o balanceaor de nível 4 divide de solicitações vindas do mesmo usuário entre diferentes instâncias do backend, o backend não pode manter um estado 
      em memória. Tudo é carregado do bd a cada pedido.
      Se for preciso manter um estado em memória para ganhar velocidade no tratamento de pequenas solicitações, como ocorre com chatbots, então é
      preciso ter também um balanceador de nível 7 (aplicação), que lá foi implementado também em Python. O balanceador de nível 7 tem várias instâncias
      que são acionadas alternadamente pelo balanceador de nível 4. Elas redirecionam os pedidos lendo o conteúdo das mensagens para manda o mesmo usuário sempre
      para mesma instância do backend.
      Não colocamos isto no exemplo, mas é bom ter em mente esta possibilidade.
      
  Um container com MongoDB
  
      A medida em que os usuários vão interagindo com o frontend, eles vão gerando dados que precisam ser gurdados em algum lugar.
      Assim, já criamos um banco de dados para ser acessado por todos os outros containers.
      
      
      
      
      




