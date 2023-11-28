FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt update && apt install gettext -y
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY requirements_dev.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
COPY . /code/
RUN python manage.py compilemessages --locale=es
