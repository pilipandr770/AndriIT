FROM python:3.10-slim

WORKDIR /app

COPY requirements_render.txt .
RUN pip install --no-cache-dir -r requirements_render.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]