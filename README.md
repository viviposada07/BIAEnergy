# BIA Energy - Data Engineer Test

Este proyecto lee coordenadas geográficas desde un archivo CSV, consulta la API pública `postcodes.io` para enriquecer los datos con información del código postal más cercano, y los almacena en PostgreSQL. Finalmente, genera un reporte enriquecido en CSV.

## 🚀 Cómo correr

1. Instala Docker Desktop y asegúrate de que está corriendo.
2. Clona el repositorio o copia los archivos.
3. En la raíz del proyecto, ejecuta:

```bash
docker-compose up --build
