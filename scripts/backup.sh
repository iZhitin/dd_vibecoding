#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
pg_dump -U dd -h db dd | gzip > "$BACKUP_DIR/dd_$TIMESTAMP.sql.gz"
# Ротация: удалить бэкапы старше 7 дней
find "$BACKUP_DIR" -name "dd_*.sql.gz" -mtime +7 -delete
