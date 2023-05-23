FROM python:3.9

# Ustawienie zmiennych środowiskowych dla Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

# Utworzenie i ustawienie katalogu roboczego
RUN mkdir /code
WORKDIR /code

# Instalacja zależności Pythona
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Skopiowanie kodu źródłowego aplikacji Django
COPY . /code/

# Uruchomienie serwera Django
CMD python manage.py runserver 0.0.0.0:8000 & celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler