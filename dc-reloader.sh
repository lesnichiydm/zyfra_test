#!/bin/bash
while :
do
    if [ ! -f .env ]; then
        cp .env.dist .env
    fi

    docker-compose stop
    docker-compose rm -f
    docker-compose down --volumes
    touch .env
    docker-compose build
    docker-compose run -d postgres

    sleep 1
    docker-compose run web python ./manage.py migrate
    docker-compose run web python ./manage.py createsuperuser --no-input
    docker-compose run web python ./manage.py loaddata -i fixtures/all_fixtures.json
    docker-compose stop
    docker-compose run --name web --service-ports web $1
    sleep 1
done
