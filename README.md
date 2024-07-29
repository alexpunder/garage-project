## Описание проекта.

*Ссылка на сайт в боевом режиме*: https://garage-vlz.ru/

_**Автозапчасти "Гараж"**_ - личный проект по созданию и развитию сайта для магазина автомобильных запчастей **"ГАРАЖ"**. Шаблоны для frontend'а приобретены в магазине (https://themeforest.net/item/stroyka-tools-store-html-template/23326943), по-большей части переделаны под свои нужды. Backend написан на Django 3.2, структурно - это монолитный сервис, где код разделён на логические модули, а методы по-возможности вынесены в сервисный слой приложения:  
1. 'shop' - работа с товарами, категориями, подкатегориями, брендами. Сюда же входит работа с различными акциями.
2. 'authorization' - авторизация пользователей; в основном изменены формы, но не принцип встроенной авторизации. Установле, подключен и настроен пакет 'allauth' для OAuth2 авторизации.
3. 'users' - работа с пользователями и их автомобилями (имеется возможность сохранить данные своего автомобиля в профиль).
4. 'cart' - корзина только для авторизованного пользователя. Добавление товара анонимным пользователем не реализована.
5. 'orders' - история заказов пользователя. Здесь реализована логика сохранения товаров из заказа в историю и окончательное подтверждение оформления заказа.
6. 'pages' - здесь собраны остальные страницы, такие как: "О нас", "Контакты", "Пользовательское соглашение" и другие.

В проекте используется глобальное кеширование через связку `Redis` и библиотеки `django-cachalot`. Так же используется Celery для отправки сообщения на почту пользователя с информацией о созданном заказе; после оформления заказа клиентом, telegram-бот так же посредством Celery отправляет сообщение администратору сайта с информацией о размещённом заказе.

Написан кастомный `management commands` для загрузки в БД информации из заготовленных .csv-файлов.

В директории проекта находятся два .yml-файла для Docker compose:  
1. `docker-compose.yml` - для локальной сборки без привязки образов к Docker Hub
2. `docker-compose.production.yml` - для сборки на сервере, где установлен и настроен Docker

Для поисковых краулеров, доступ к файлам robots.txt и sitemap.xml осуществляется через их добавление в директорию `static/` (так настроено в файле-конфигурации Nginx при создании образа).

Код сайт оптимизировался в соответствии с тестированием в `Lighthouse`.

## Используемые технологии.

![Python 3.12](https://img.shields.io/badge/Python-3.12-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Celery 5.4.0](https://img.shields.io/badge/Celery-5.4.0-brightgreen.svg?style=flat&logo=celery&logoColor=white)
![Redis 5.0.4](https://img.shields.io/badge/Redis-5.0.4-brightgreen.svg?style=flat&logo=redis&logoColor=white)
![Python-telegram-bot 21.4](https://img.shields.io/badge/python--telegram--bot-21.1.1-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Django 5.0.7](https://img.shields.io/badge/Django-5.0.4-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Django-filter 24.2](https://img.shields.io/badge/Django--filter-24.2-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Django-cachalot 2.6.2](https://img.shields.io/badge/Django--cachalot-2.6.2-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Django-phonenumber-field 8.0.0](https://img.shields.io/badge/Django--phonenumber--field-8.0.0-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Django-allauth 0.60.1](https://img.shields.io/badge/Django--allauth-0.60.1-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-brightgreen.svg?style=flat&logo=docker&logoColor=white&color=blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-brightgreen.svg?style=flat&logo=gunicorn&logoColor=white&color=blue)
![Nginx](https://img.shields.io/badge/Nginx-brightgreen.svg?style=flat&logo=nginx&logoColor=white&color=blue)
