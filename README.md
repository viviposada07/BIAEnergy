# Bia Energy – Prueba Técnica Data Engineer
Este proyecto es una solución para la prueba técnica de Bia Energía. Consiste en leer un archivo de coordenadas (`postcodesgeo.csv`), enriquecer los datos mediante la API pública `postcodes.io`, almacenarlos en una base de datos PostgreSQL y generar reportes automáticos con estadísticas relevantes.

## Estructura del Proyecto
bia_energy_project/
├── data/                       # Archivo original CSV con coordenadas
├── reports/                    # Archivos CSV y Excel generados con los reportes
├── src/                        # Código fuente de la aplicación
│   ├── main.py                 # Script principal
│   ├── enrich.py               # Lógica para procesar los datos con la API
│   ├── db.py                   # Conexión a base de datos y creación de tablas
│   ├── generate_reports.py     # Generación de reportes desde la base de datos
│   └── api_client.py           # Funcion de conexión a la API.
├── docker-compose.yml          # Orquestador de contenedores
├── Dockerfile                  # Imagen de la aplicación
├── requirements.txt            # Dependencias de Python
├── wait-for-db.sh              # Espera activa hasta que la base de datos esté disponible
└── README.md                   # Este archivo

## Requisitos
- Docker y Docker Compose
- Cuenta en GitHub (opcional para clonar el repo)

## ¿Cómo ejecutar el proyecto?
1. Clona el repositorio:
git clone https://github.com/viviposada07/BIAEnergy.git
cd BIAEnergy
2. Abrir la aplicacion de Docker Desktop. 
3. Construye e inicia el proyecto con el comando en terminal: docker-compose up --build
4. El sistema:
   - Lee el archivo data/postcodesgeo.csv.
   - Llama la API https://api.postcodes.io por lotes.
   - Inserta la información en la base de datos PostgreSQL.
   - Genera los reportes en la carpeta reports.
5. Elimina contenedores y volúmenes al finalizar el uso: docker-compose down -v

## Reportes generados
- enriched_postcodes.csv: archivo enriquecido con la info geográfica.
- report.xlsx: contiene:
  - Códigos postales mas comunes.
  - Porcentaje de coordenadas sin código postal.
  - Estadisticas generales.

## Validaciones y manejo de errores
- Detección de duplicados (por latitud y longitud).
- Logs de errores insertados en una tabla error_log.
- Evita reintentos si ya existen las coordenadas.

## Base de Datos
El sistema crea las siguientes tablas automáticamente:
- enriched_postcodes
- error_log
Incluyen una columna load_dts con la fecha y hora de carga.

## Contacto
Proyecto desarrollado por **Viviana Posada Restrepo** como parte del proceso de selección para el cargo de Data Engineer.