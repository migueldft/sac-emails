# SAC - Classificação de Emails

Esta aplicação foi construida com o objetivo de ser uma automação para o time do SAC, que precisa ler, classificar e responder diversos e-mails que recebem diariamente dos nossos clientes.
O objetivo desta é conseguir categorizar a voz do cliente dentro das mensagens para que seja possível enviar uma resposta automatica para o cliente sem que seja necessária uma atuação do analista.

## Modelo

O projeto utiliza técnicas de NLP (limpeza + lematizacao + TF-IDF) para tratamento do texto contido nas mensagens para posterior treinamento utilizando o RandomForest.

## Estrutura dos Arquivos

Esta seção serve para descrever um pouco sobre a estrutura das pastas e arquivos contidos neste repositório de modo a facilitar o entendimento do projeto.

```
sac_emails
│   README.md
└─── .circleci (1)
└─── aws_scripts (2)
└─── container (3)
│       └─── local_test (3.1)
│       └─── src (3.2)
│ ....
```

1. **.circleci**

    Arquivo de configuracao `config.yml` que tem como objetivo compilar um container no CircleCI e subi-lo no Amazon ECR sempre que um novo commit for feito no repositório. Devemos adicionar algumas variáveis de ambiente no projeto do CircleCI para que ele consiga acessar os serviços da AWS [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION]

2. **aws_scripts** 

    Nesta pasta temos alguns códigos em python responsáveis por colocar o projeto em produção. Todos eles atuam diretamente no Sagemaker.
    - `create_training_job.py` - Treina o modelo e salva seus artefatos em um bucket do S3.
    - `create_model.py` - Cria um modelo no Sagemaker a partir do ultimo treinamento realizado.
    - `create_batch_transform_job.py` - Faz o processamento em batches de um arquivo de inferencia.
    - `create_endpoint.py` - Faz o deploy do modelo em um endpoint.

3. **container**

    Pasta que contém o código principal da aplicação e scripts auxiliares para o treinamento local.

    - `Dockefile` - Arquivo que descreve como compilar o container Docker e o que ele contém.
    - `build_and_push.sh` - Script que utiliza o Dockerfile para compilar o Docker e enviar sua imagem para o Amazon ECR.

    #### local_test

    Diretório com os scripts necessários para rodar processos de treinamento e inferência localmente, de modo que seja possivel testar se tudo está funcionando corretamente.
    
    - `train_local.sh` - Treina o modelo com os dados de entrada disponíveis em *container/local_test/test_dir/input/data/training* e salva o modelo na pasta *container/local_test/test_dir/model*
    - `serve_local.sh` - Realiza o deploy do modelo em um endpoint (http://localhost:8080/invocations)
    - `predict_local.sh` - Faz um request ao endpoint criado com os dados contidos no arquivo *container/local_test/payload.json*

    #### src

    Diretório que contém a aplicação que será executade pelo container.

    - `train` - Script responsável pelo treinamento do modelo.
    - `predictor.py`- Script para inferência/predição.
    - `CustomClasses.py` - Classe criada para fazer parte do PipeLine do modelo.


## Referencias

* https://github.com/aws/amazon-sagemaker-examples/tree/main/advanced_functionality/scikit_bring_your_own/container
* https://towardsdatascience.com/bring-your-own-container-with-amazon-sagemaker-37211d8412f4