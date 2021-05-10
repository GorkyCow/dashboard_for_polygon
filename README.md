Dashboard for polygon.io
================================

Для развертывания создайте свои конфиг-файлы (config.yml и postgres_conf.yml) из файлов-примеров (config.yml.dist и postgres_conf.yml.dist)
В config.yml добавьте рабочий ключ API для polygon.io

Для сборки docker-образов запустите:<br>
    docker-compose build

Для старта проекта запустите:<br>
    docker-compose up -d

Для того, чтобы воркеру было что искать нужно заполнить справочник инструментов. Для этого запустите команду:<br>
    docker-compose exec worker python setup.py
