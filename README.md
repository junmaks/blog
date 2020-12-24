# blog

Инструкция

Необходимо установить виртуальное окружение (python -m venv venv)
Активировать его (Windows: .\venv\Scripts\activate, Linux: source venv/Scripts/activate)
Необходимые библиотеки:
          pip install django
python manage.py collectstatic для работы статики
python manage.py python manage.py makemigrations (python manage.py python manage.py makemigrations blogs)
python manage.py migrate
python manage.py createsuperuser
Запустить сервер: python manage.py runserver 8000
Пройти по ссылке http://127.0.0.1:8000
При регистрации новых пользователей в админке необходимо указать username и email
Для отправки писем необходимо в settings.py указать email, port и пароль (проверялось на mail.ru). Для работы с другими почтовыми серверами необходимо внести корректировку в EMAIL_HOST)
 
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 'port'
EMAIL_HOST_USER = "your_email"
EMAIL_HOST_PASSWORD = "your_password"
