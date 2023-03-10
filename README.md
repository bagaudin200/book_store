# Книжный магазин
[Техническое задание](...)

### Инструкция по установке и первому запуску 

Установить зависимости:

```bash
pip install -r requirements.txt
```

Провести миграцию:

```bash
python manage.py makemigrations
python manage.py migrate
```

Загрузить тестовые данные:

```bash
python manage.py loaddata goods.csv
```

Создать суперпользователя:

```bash
python manage.py createsuperuser
```

Запустить веб-сервер проекта:

```bash
python manage.py runserver
```

> Внимание: поскольку реализована OTP-авторизация без отправки sms, одноразовый код можно увидеть в консоли, либо в админке в модели Profile.

Сформировать отчет по покупкам с группировкой по дням  

> В разделе админки [Заказы покупателей](http://127.0.0.1:8000/admin/cart/order/) фильтруем по дате и отмечаем интересующие нас заказы. После чего выбираем действие "Сформировать отчет по выбранным заказам" 

Тестирование кода
> Реализованы примеры тестирования для двух приложений
```bash
python manage.py test store

```


## Примеры работы API
По умолчанию пагинация установлена на 2 записи
* [получение полного списка товаров](http://127.0.0.1:8000/api)
* [получение списка товаров по группе](http://127.0.0.1:8000/api?group=30)
* [получение списка товаров по названию или его части](http://127.0.0.1:8000/api?name=sams)
* [получение списка групп](http://127.0.0.1:8000/groups)