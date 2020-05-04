# i-cherry Analytics Challenge

## Requisitos

* Docker containers
    - Windows: https://docs.docker.com/docker-for-windows/install/
    - Ubuntu: https://docs.docker.com/engine/install/ubuntu/ 

* Credenciais do Google para utilizar API do Analytics, siga com atenção os passos descritos no tutorial abaixo.
    - https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

* Além das credencias descritas acima é necessário que a conta cadastrada tenha pelo menos uma propriedade e uma view.

## Como executar a instalação

* No diretório raíz do projeto executar:
    - docker-compose up --build
    - Após o término da execução abra o navegador de sua preferência e digite o endereço:
        - http://localhost:8000/

## Tecnologias utilizadas

* Todo o desenvolvimento doi realizado utilizando python.
    - https://www.python.org/
* Para o frontend foi utilizado o framework Django
    - https://www.djangoproject.com/

* Para os componentes de UI foi utilizado bootstrap CDN
    - https://www.bootstrapcdn.com/

* Para garantir a consistência em diferentes plataformas foi utilizado Docker containers
    - https://www.docker.com/resources/what-container

* Para controles de componentes no HTML foi utilizado JavaScript
    - https://www.javascript.com/

## Desenvolvimento da API

* Para o desenvolvimento da API foi utilizada a biblioteca google-api-python-client do Google Analytics
    - https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py