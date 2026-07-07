#!/bin/bash
# Этот скрипт запускается один раз при первом старте мастера
# Создаёт пользователя для репликации

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" << EOSQL
  -- Создаём пользователя для репликации
  CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
  
  -- Даём права на подключение
  GRANT CONNECT ON DATABASE $POSTGRES_DB TO replicator;
EOSQL

# Разрешаем репликацию в pg_hba.conf
echo "host replication replicator all md5" >> "$PGDATA/pg_hba.conf"

# Настраиваем параметры репликации
cat >> "$PGDATA/postgresql.conf" << PGCONF
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64
hot_standby = on
PGCONF
