FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY .env /app/.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

VOLUME /app/db

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
