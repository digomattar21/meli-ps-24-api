FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY wait-for-it.sh /usr/local/bin/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV=development

CMD ["python", "app.py"]
