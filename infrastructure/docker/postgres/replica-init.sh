#!/bin/bash
# Этот скрипт запускается при старте реплики
# Копирует данные с мастера через pg_basebackup

set -e

# Ждём пока мастер будет готов
until pg_isready -h pg-master -U replicator; do
  echo "Ждём мастера..."
  sleep 2
done

# Очищаем папку данных
rm -rf "$PGDATA"/*

# Копируем данные с мастера
pg_basebackup \
  -h pg-master \
  -U replicator \
  -D "$PGDATA" \
  -P \
  -Xs \
  -R

echo "Репликация настроена успешно!"
