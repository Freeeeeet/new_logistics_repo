# Используем nginx для доставки статических файлов
FROM nginx:alpine

# Копируем HTML, CSS и JS файлы в папку с веб-страницей nginx
COPY ./ /usr/share/nginx/html

# Открываем порт 80 для nginx
EXPOSE 80