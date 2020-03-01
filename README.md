# Paper Question Answerer with Bert - API


## About

Upload the pdf of any article in english and ask her any questions about its content "where the dataset came from?", "what is the neural network architecture used?" then and the model will answer the question.

Some filters are applied to the article to remove the garbage and leave only the necessary information and the model used is Bert from the DeepPavlov library, which is a transformer that uses the seq2seq neural network architecture to model language, the model was trained in english with the Squad dataset to answer questions given a text.

[Webapp](https://github.com/lucasraggi89/paper-qa-bert-webapp)

## How to use the project? - Without docker

To configure the API for development use:
- Have Java 8 installed

## Run
- Git Clone Repo
- Run `pip install -r requirements.txt`
- Run `python -m deeppavlov install squad_bert`
- Run `python3 paper-qa-api.py`

## How to use the project? - With docker

To configure the API for development use:
- Have Docker Desktop installed
- In the docker settings, check the 'Expose daemon ...' option and mark your disks as shared drives
- Increase the docker ram limit to at least 4gb

## Run
to start the API:
Run `docker-compose up`


