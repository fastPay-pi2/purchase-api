# purchase-api

## Executando testes

docker-compose run api coverage run -m unittest discover

## Executando cobertura de testes

docker-compose run api  coverage report

## Executar banco de dados

docker-compose exec database-purchase mongo mongodb://database-purchase:27017/purchase