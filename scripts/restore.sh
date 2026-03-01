#!/bin/bash
echo "Restaurando base de datos de NocoDB..."
cat backup_nocodb.sql | docker exec -i sice_postgres psql -U sice_user -d sice_db
echo "Base de datos restaurada correctamente"