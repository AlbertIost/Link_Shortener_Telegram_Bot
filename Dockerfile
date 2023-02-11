# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/web_app

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/link_shortener_tgbot/requirements.txt

COPY link_shortener_tgbot /usr/src/web_app

EXPOSE 8000
#CMD["python", "manage.py", "migrate"]
#CMD["python", "manage.py", "runserver", "0.0.0.0:8000"]