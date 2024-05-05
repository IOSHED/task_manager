
# Запуск postgres:
```postgres-sql
CREATE EXTENSION pg_trgm;
CREATE INDEX забыл...
```

# План по созданию MVP
+ - Создать auth_service
+ - Написать task_service.  
Он должен отправлять в очередь к отправлению уведомлений в controller_send_notification_service.
Он собирает данные с шалона template_task_service.
+ - Подключить redis к task_service
- Написать template_task_service
- Подключить к template_task_service redis
- Написать controller_send_notification_service с использованием celery и django
- Написать telegram_bot
- Написать сервис send_notification_telegram_service
- Написать интерфейс для сайта
- Подключить GitActions
- Создать мобильное приложение по средствам Progressive Web App
Полезная ссылка ---  https://habr.com/ru/companies/vk/articles/450504/
- Арендовать небольшой сервер и кинуть туда свой сайт
- Создать ветку dev в git
- Разрабатывать дальнейший проект на ветке dev
