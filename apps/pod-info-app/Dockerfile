FROM --platform=$BUILDPLATFORM python:3.11-slim

RUN useradd -m -r appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]