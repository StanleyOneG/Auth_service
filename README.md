#  **Ссылка на репозиторий** https://github.com/VladIs10ve/Auth_sprint_1


#  **Ссылка на репозиторий Async_API** https://github.com/VladIs10ve/Async_API_sprint_1_team

Для интеграции сервисов используется jwt token и общий public_key

#  **Описание**

Это API реализует функциональность аутентификации и авторизации пользователей, а также управление правами доступа к API.
API позволяет зарегистрировать нового пользователя, войти в систему, получить доступ к ресурсам API, обновить токены и
выйти из системы.

#  **Зависимости**

Перед запуском проекта на локальной машине, необходимо установить следующие зависимости:

- Docker
- docker-compose

Для локального запуска:

- Python (версии 3.10)
- библиотеки Python, указанные в файле requirements.txt, можно установить с помощью команды:
  pip install -r requirements.txt

#  **Переменные окружения**

Для запуска приложения необходимо в **корне проекта** создать `.env` файл и заполнить его следующими переменными (
значения по умолчанию оставить неизменными):

```

# Параметры базы данных PostgreSQL
DB_ENGINE=postgresql
POSTGRES_DB=service_auth
POSTGRES_PASSWORD=#<пароль для PostgreSQL>
POSTGRES_USER=#<имя пользователя  PostgreSQL>
POSTGRES_HOST=sprint06_auth_tests_pg_server # название Докер контейнера с базой PostgreSQL
POSTGRES_PORT=5432
POSTGRES_OPTIONS="-c search_path=auth" 

# Параметры базы данных Redis
REDIS_HOST=sprint06_auth_tests_redis_server # название Докер контейнера с базой Redis
REDIS_REFRESH_TOKEN_EXPIRE=#<Время жизни refresh токена>
REDIS_ACCESS_TOKEN_EXPIRE=#<Время жизни access токена>
REDIS_PORT=6379

# Параметры входа в PGAdmin
PGADMIN_DEFAULT_EMAIL=#<Почта для входа в PGADMIN>
PGADMIN_DEFAULT_PASSWORD=#<Пароль для входа в PGADMIN>

# Параметры суперпользователя
SUPERUSER_LOGIN=#<Логин суперпользователя>
SUPERUSER_EMAIL=#<Почта суперпользователя>
SUPERUSER_PASSWORD=#<Пароль суперпользователя>

# Параметры API
SERVER_HOST=sprint06_auth_tests_api_server # название Докер контейнера с Auth API
SERVER_PORT=8000
SERVER_DEBUG=True # Использовать True только для тестирования

# URL для доступа к API
SERVICE_URL=http://sprint06_auth_tests_api_server:8000 

# Параметры OAuth провайдеров
GOOGLE_AUTH_NAME=#<имя провайдера oauth>
GOOGLE_AUTH_CLIENT_ID=#<client_id провайдера>
GOOGLE_AUTH_CLIENT_SECRET=#<client_secret провайдера>
GOOGLE_AUTH_AUTHORIZE_URL=#<URL на стороне провайдера для аутентификации>
GOOGLE_AUTH_ACCESS_TOKEN_URL=#URL на стороне провайдера для получения access_token>
GOOGLE_AUTH_API_BASE_URL=#<URL на стороне провайдера для получения информации например, о пользователе>

```

#  **Запуск приложения**

Для запуска приложения необходимо в корневой папке проекта запустить команду `docker-compose up --build`.
Для остановки проекта используйте команду `docker-compose down`.

#  **API**

**Документация в формате OpenAPI:**

Документация API доступна в формате OpenAPI по адресу http://localhost:8000/apidocs/

***Реализованный функционал***

API предоставляет набор функций для работы с авторизацией и правами доступа пользователей.

1. Sign up - регистрация пользователя
2. Log in - функционал входа пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh
   токен)
3. Обновление access-токена
4. Выход пользователя из аккаунта
5. Изменение логина или пароля
6. Получение пользователем своей истории входов в аккаунт
7. Создание прав доступа
8. Удаление прав доступа
9. Изменение прав доступа
10. Просмотр всех существующих прав доступа
11. Просмотр прав доступа конкретного пользователя
12. Назначение прав доступа пользователю
13. Удаление прав доступа у конкретного пользователя
14. Реализована функция проверки прав доступа пользователя

**Хранение данных**

Для хранения прав доступа используется PostgreSQL, а для хранения токенов используется Redis.

#  **Как начать**

Для начала работы с API необходимо выполнить следующие шаги:

1. Зарегистрировать нового пользователя с помощью функции Sign up
2. Авторизоваться с помощью функции Log in и получить access и refresh токены
3. Использовать полученный access токен для выполнения запросов к другим функциям API
4. При необходимости обновить access токен с помощью функции Refresh access token
5. Выйти из аккаунта с помощью функции Log out

Токены хранятся в cookies браузера


#  **Тесты**

Тесты работы api реализованы с помощью библиотеки pytest. Для запуска функциональных тестов необходимо:

В папке auth_tests создать .env файл (пример расположен в файле auth_tests/.env.example)
В консоли перейти в директорию auth_tests и выполнить команду docker-compose up --build --exit-code-from sprint06_auth_tests_tests
