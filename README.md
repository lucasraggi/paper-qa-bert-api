# Paper Question Answerer with Bert - API

## Como usar o projeto? - Sem docker

Para configurar a API para uso em desenvolvimento:
- Tenha Java 8 instalado

## Iniciar
- Git Clone Repo
- Run `pip install -r requirements.txt`
- Run `python -m deeppavlov install squad_bert`
- Run `python3 paper-qa-api.py`

## Como usar o projeto? -  Com docker

Para configurar a API para uso em desenvolvimento:
- Tenha o Docker Desktop instalado
- Nas configurações do docker, marque o opção 'Expose daemon...' e marque os seus discos como shared drives
- Aumente o limite de ram do docker para pelo menos 4gb

## Iniciar
Para iniciar a API:
`docker-compose up`


