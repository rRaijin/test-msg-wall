Установить окружение коммандой:

virtualenv .venv

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

...

python manage.py runserver 8000 (авторизация через соцюсети работает только на порту 8000)

В браузере откройте http://127.0.0.1:8000
