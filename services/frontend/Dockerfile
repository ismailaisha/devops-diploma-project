# ── Стадия 1: просто копируем статику ──
FROM nginx:alpine AS runtime

# Копируем конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем фронтенд файлы
COPY index.html /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost/health || exit 1