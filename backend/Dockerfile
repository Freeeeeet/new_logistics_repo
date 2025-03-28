FROM python:3.9-slim

# Устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . /app

# Открываем порт приложения
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "run.py"]
