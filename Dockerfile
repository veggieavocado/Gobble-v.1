FROM python:3.7

RUN apt-get install -f && \
    apt-get update && \
    apt-get install -y && \
    apt-get install -y g++ openjdk-8-jdk python3-pip python3-dev && \
    pip3 install JPype1-py3 && \
    pip3 install konlpy && \
    pip3 install uwsgi

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -q Django==2.0 && \
    pip3 install -r requirements.txt

RUN python manage.py makemigrations && \
    python manage.py makemigrations contents && \
    python manage.py migrate --database=contents && \
    python manage.py migrate sessions && \
    python manage.py migrate && \
    python manage.py migrate django_celery_results && \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]
