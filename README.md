# Дипломный проект SB1. Доска объявлений

Необходимо разработать backend-часть для сайта объявлений. Бэкенд-часть проекта предполагает реализацию следующего функционала:

- Авторизация и аутентификация пользователей.
- Распределение ролей между пользователями (пользователь и админ).
- Восстановление пароля через электронную почту.
- CRUD для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
- Под каждым объявлением пользователи могут оставлять отзывы.
- В заголовке сайта можно осуществлять поиск объявлений по названию.
_____
## Краткое техническое задание и рекомендации по порядку выполнения:
### Этап I. Настройка Django-проекта. 

На данном этапе предстоит подготовить Django-проект к работе. Данный этап состоит из трех подзадач:

1. Подключение базы данных Postgres.
2. Подключение CORS headers.
3. Подключение Swagger.


### Этап II. Создание модели юзера. Настройка авторизации и аутентификации.
- Создание модели пользователя:
    - Необходимые поля:
        - first_name — имя пользователя (строка).
        - last_name — фамилия пользователя (строка).
        - phone — телефон для связи (строка).
        - email — электронная почта пользователя (email) **(используется в качестве логина).**
        - role — роль пользователя, доступные значения: user, admin.
        - image — аватарка пользователя.
- Настройка авторизации и аутентификации:
    - Настроить авторизацию пользователя с помощью библиотеки simple_jwt.
    - Сброс и восстановление пароля через почту
  
### Этап III. Описание моделей объявлений и отзывов.
- Модель объявления должна содержать следующие поля:
    - title — название товара.
    - price — цена товара (целое число).
    - description — описание товара.
    - author — пользователь, который создал объявление.
    - created_at — время и дата создания объявления.
    - Объявления должны быть отсортированы по дате создания (чем новее, тем выше).
- Модель отзыва должна содержать следующие поля:
    - text — текст отзыва.
    - author — пользователь, который оставил отзыв.
    - ad — объявление, под которым оставлен отзыв.
    - created_at — время и дата создания отзыва.

### Этап IV. Создание views и эндпоинтов.
- Создать эндпоинты для всех необходимых операций с использованием DRF.
- Реализовать поиск товаров по названию с использованием библиотеки `django-filter`.
- Эндпоинт `/ads/` должен поддерживать пагинацию с ограничением не более 4 объектов на странице.

### Этап V. Определение permissions к views.
- Анонимный пользователь может:
    - получать список объявлений.
- Пользователь может:
    - получать список объявлений,
    - получать одно объявление,
    - создавать объявление,
    - редактировать и удалять свое объявление,
    - получать список комментариев,
    - создавать комментарии,
    - редактировать/удалять свои комментарии.
- Администратор может:
    - дополнительно к правам пользователя редактировать или удалять объявления и комментарии любых других пользователей.

### Этап VI. Упаковка в Docker.
- Создать `Dockerfile` для сборки образа приложения.
- Создать `docker-compose.yml` для запуска приложения и базы данных PostgreSQL.

### Этап VII. Написание тестов.
- Написать тесты для всех основных функций платформы.
- Использовать библиотеку `pytest` для тестирования.

_____

## Для запуска проекта в Docker необходимо воспользоваться командой:
### в файле .env Прописать POSTGRES_HOST=db

- docker-compose up -d --build

_____
## Для запуска тестов необходимо воспользоваться командой:

- coverage run --source='.' manage.py test

и вывести отчет по покрытию:
- coverage report
_____