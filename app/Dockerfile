# Используем Python в качестве базового образа
FROM python:3.11-slim

# Устанавливаем зависимости для nextflow и Python
RUN apt-get update && \
    apt-get install -y curl openjdk-17-jdk git && \
    apt-get clean

# Устанавливаем Nextflow
RUN curl -s https://get.nextflow.io | bash && \
    mv nextflow /usr/local/bin/ && \
    chmod +x /usr/local/bin/nextflow

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем зависимости
COPY app/requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY app /code/app

# Открываем порт (если нужно)
EXPOSE 8000

# Запускаем FastAPI (или другой ASGI-сервер)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
