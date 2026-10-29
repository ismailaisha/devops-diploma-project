FROM nginx:alpine AS runtime

# Конфигурация Nginx для Docker Compose
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Статические файлы приложения
COPY index.html /usr/share/nginx/html/index.html
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY pages/ /usr/share/nginx/html/pages/

EXPOSE 80

# Проверяет доступность API через Nginx
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/health || exit 1