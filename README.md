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
SERVER_TELEMETRY=False

# URL для доступа к API
SERVICE_URL=http://sprint06_auth_tests_api_server:8000 

# Параметры OAuth провайдеров
GOOGLE_AUTH_NAME=#<имя провайдера oauth>
GOOGLE_AUTH_CLIENT_ID=#<client_id провайдера>
GOOGLE_AUTH_CLIENT_SECRET=#<client_secret провайдера>
GOOGLE_AUTH_AUTHORIZE_URL=#<URL на стороне провайдера для аутентификации>
GOOGLE_AUTH_ACCESS_TOKEN_URL=#URL на стороне провайдера для получения access_token>
GOOGLE_AUTH_API_BASE_URL=#<URL на стороне провайдера для получения информации например, о пользователе>

# Пример ключей
JWT_PRIVATE_KEY='-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCWtNxdEIXjMXZp
YlR8MhFukbcLztdGC3/IhW8s1/wQIxQtz+jCPF9CFzt3UYNr0Zpv5PUJSS3o01fp
BbQ275wNug2QdLh/lBJFehGmT8n/xVCk46XUoIp6Jhg30ofC79XHiXl9+iKkddmp
3ylmLp3Z5ipAm+9nq6f/V0R9x28bStMhzwz7t4uX7HDOErlFYbldP0kSuWvj4QfN
kwvWfc+z2sFlBlZ1ztKys7MBFgZwXmj6ZVlxIi6wudZkLI8X2eF0BrRgq74D5nEx
wpG47VQRIqG1FJjfF+gsyYVfPT+iSHvD4M7Qq6Y5emgWhdRX2ndvv4i23/ZVodhb
+zP0IHB9AgMBAAECggEAAM+DOerrVXAAK4vwWWSpjFczTVh09vb73ne9Q9f7jpip
tJ9gKJ9Lgd7/HmKtWsibVIu+N6kRmqV8XQ//SqZaSAaeqQ6/qUwCFyaTbroSI5KL
nv9sdmrQo9yNl8tFmKpSk4qtQRy1z/2kSJIfNmH8zl27D3LnRD77ndd50lVexx5L
SrqIIF/r2SpefqV0Ov1B6e0HrY/u4Tmawf29+aFjqjL5YQbRRMgcuMAGwyJIacDu
Eb3NUK+Rp78l+IvNQr8q8R95YMSmnH3s6x5cPg8z4dg8hDW1Qw/eXHy5uSDmlQc4
dEx4AhdrhQaKs4OI6mfEf1VVEmVmbY9OkjTyoy0JwQKBgQDU+7xJjXUDwrDixsQa
rIWL87nCA8QSiLBDBmmi0iPaA2fUc7TZ6ueezL0I5h3GXTmXzg5QceueOH0/7Wnj
T6/B32aJW90UMyjyQ2ryBy95BVkmEycs/8b79HVfCFGTU6fO0u4PD80fY0G4qDvs
4N5Cso4V6+4r2TvrqAjWFOTS3QKBgQC1JRysQkmhjS1G2IB04SE9npP6GcV1kJSj
qhy5uOu4QfWXm9ega2Xt6oEBI0nrE/vpva6Bj9G7c6ijwhdrHHXg6agn8BamFJ34
LmmEhMEqiPo98Oy3NI37k2ix4kTZBcihq6XoYQ69tSIB0Zy/M6zA1I5546g0i9d8
fRoPWR0qIQKBgGmaVBaoM//kVe5rnaqYJjNpao5/bYW/Dp59HH2l8i7UB3R41pBC
gAvl+kjiSJsleDwD6GcMxUYTPk8nOZyC02OukFnFGc49O607rlhJJcm81CIj1wXh
4NjmshenuULydL8BKRaAwDUy8tBLYkMmkC3D+N13uQU21hYXoCH+BCNlAoGAXbjZ
4PZbCk71Aha6P77LaApIHbp/w5gOj69QNXdL3oWh/9MN+V4X2sTeAiyz7gDk8cbG
Jxq2NPpeYnvlifGru7ao3iEGVt+L7AB3b60QFGXSs4GXuCJk46kdHgwn+vFXIO6i
ZFzzN4wkEDTXmMWvuAVBwibbvHQuBabkeNRuloECgYEAs+Snww0Bb8yhZxolNmeI
rTWtHwtt5hyQucUrczoaVID4WT7lQUlnnK1onLGqu/NY643HvV74TAzM8IfjN9Ks
hxtUAl0Rvuf8i/zhP00pZtt9knd/Vt5MFBzX3+YvhFfpJCwTh9MFjwWSP6g5Q+z0
CdVXUMISAY78NlZpIo+fbXU=
-----END PRIVATE KEY-----'
JWT_PUBLIC_KEY='-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlrTcXRCF4zF2aWJUfDIR
bpG3C87XRgt/yIVvLNf8ECMULc/owjxfQhc7d1GDa9Gab+T1CUkt6NNX6QW0Nu+c
DboNkHS4f5QSRXoRpk/J/8VQpOOl1KCKeiYYN9KHwu/Vx4l5ffoipHXZqd8pZi6d
2eYqQJvvZ6un/1dEfcdvG0rTIc8M+7eLl+xwzhK5RWG5XT9JErlr4+EHzZML1n3P
s9rBZQZWdc7SsrOzARYGcF5o+mVZcSIusLnWZCyPF9nhdAa0YKu+A+ZxMcKRuO1U
ESKhtRSY3xfoLMmFXz0/okh7w+DO0KumOXpoFoXUV9p3b7+Itt/2VaHYW/sz9CBw
fQIDAQAB
-----END PUBLIC KEY-----'

```

#  **Запуск приложения**

Для запуска приложения необходимо в корневой папке проекта запустить команду `docker-compose up --build`.
Для остановки проекта используйте команду `docker-compose down`.

#  **API**

**Документация в формате OpenAPI:**

Документация API доступна в формате OpenAPI по адресу http://localhost:88/apidocs/

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
15. OAuth2 - функционал регистрации и вход пользователя в аккаунт с помощью социальных сетей Yandex, MailRu, Google, VK

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
