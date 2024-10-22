FROM python:3.11.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY routes.py /app/routes.py
COPY app.py /app/app.py

COPY uwsgi.ini /app/uwsgi.ini

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
