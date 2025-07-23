#!/bin/sh
# Espera activa hasta que la base de datos esté disponible

echo "⏳ Esperando a que la base de datos esté disponible..."

until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "✅ Base de datos disponible, arrancando aplicación."
exec "$@"
