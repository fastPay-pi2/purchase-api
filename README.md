# purchase-api

## Executando testes

docker-compose run api coverage run -m unittest discover

## Executando cobertura de testes

docker-compose run api  coverage report

## Executar banco de dados

docker-compose exec purchase_db mongo mongodb://purchase_db:27018/purchase

## Executar população do banco de dados

docker-compose run --rm purchase_db_population python popula_carts.py
docker-compose up purchase_db_population