# SAC - Classificação de Emails

Esta aplicação foi construida com o objetivo de ser uma automação para o time do SAC, que precisa ler, classificar e responder diversos e-mails que recebem diariamente dos nossos clientes.
O objetivo desta é conseguir categorizar a voz do cliente dentro das mensagens para que seja possível enviar uma resposta automatica para o cliente sem que seja necessária uma atuação do analista.

## Modelo

O projeto utiliza técnicas de NLP (limpeza + lematizacao + TF-IDF) para tratamento do texto contido nas mensagens para posterior treinamento utilizando o RandomForest.

## Como usar esse projeto

Este repositório é baseado em python, makefile, pip e docker.

### Dados

Os dados para treinamento do modelo podem ser adquiridos através da query contida em `sql/sac_emails.sql`. É necessário baixar esses dados da forma como achar melhor.

### Treino e Predição

Existem 2 formas de usar os recursos aqui contidos: através da AWS, o que irá consumir o serviço Sagamaker, ou rodar localmente usando um docker.

#### Local

Podemos seguir os seguintes comandos `makefile` :


```
make build-docker
```
* Cria um docker com todos os pacotes necessários para funcionamento do modelo

```
make train
```

* Treina o modelo com os dados de entrada disponíveis em `container/local_test/test_dir/input/data/training` e salva seus artefatos na pasta `container/local_test/test_dir/model`

```
make serve
```

* Realiza o deploy do modelo em um endpoint (http://localhost:8080/invocations)

```
make predict
```

* Faz um request ao endpoint criado com os dados contidos no arquivo `container/local_test/payload.json`


#### AWS