FROM python:3.9-alpine

RUN adduser -D myuser

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 755 /app

USER myuser
EXPOSE 8080

ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]