# BetSystem

BetSystem — это система для управления пользовательскими ставками на спортивные события. Система состоит из двух микросервисов:
 - line_provider — сервис для создания и управления событиями, на которые можно делать ставки. 
 - bet_maker — сервис для приема ставок на события и обработки результатов.

Оба сервиса работают асинхронно и взаимодействуют между собой посредством Docker и сети host.docker.internal.
Для отображения статуса события в определенной ставке, реализован вызов callback-урла bet-maker при изменении статуса события
на стороне line-provider.

## Установка проекта

1. Клонируйте репозиторий:
````
 - git clone https://github.com/mishatar/BetSystem.git
 - cd bet-system
````

2. Добавить .env файл
 - пример для line_provider:
````
 - BET_MAKER_CALLBACK_URL = <callback url для обновления статуса в bet_maker>
 - APP_HOST_PORT = <порт сервиса>
 - APP_HOST = <хост сервиса>
 - POSTGRES_DB_USER = <имя пользователя>
 - POSTGRES_DB_PASSWORD = <пароль от пользователя>
 - POSTGRES_DB_HOST_PORT = <порт бд>
 - POSTGRES_DB_HOST = <адрес бд> - host.docker.internal(в случае, если два сервиса работают на локальном компьютере)
 - POSTGRES_DB_NAME = <название бд>
````
 - пример для bet_maker:
````
 - LINE_PROVIDER_URL = <url для получения событий из line_provider>
 - APP_HOST_PORT = <порт сервиса>
 - APP_HOST = <хост сервиса>
 - POSTGRES_DB_USER = <имя пользователя>
 - POSTGRES_DB_PASSWORD = <пароль от пользователя>
 - POSTGRES_DB_HOST_PORT = <порт бд>
 - POSTGRES_DB_HOST = <адрес бд> - host.docker.internal(в случае, если два сервиса работают на локальном компьютере)
 - POSTGRES_DB_NAME = <название бд>
````

3. Запустить миграции
````
 - alembic upgrade head
````

4. Собрать и запустить контейнеры для каждого сервиса
``
 - docker-compose up --build
``