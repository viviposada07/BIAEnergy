# 📍 Bia Energy – Prueba Técnica Data Engineer

Este proyecto es una solución para la prueba técnica de Bia Energía. Consiste en leer un archivo de coordenadas (`postcodesgeo.csv`), enriquecer los datos mediante la API pública `postcodes.io`, almacenarlos en una base de datos PostgreSQL y generar reportes automáticos con estadísticas relevantes.

---

## 🧩 Estructura del Proyecto

```
bia_energy_project/
├── data/                       # Archivo original CSV con coordenadas
├── reports/                    # Archivos CSV y Excel generados con los reportes
├── src/                        # Código fuente de la aplicación
│   ├── main.py                 # Script principal
│   ├── enrich.py               # Lógica para enriquecer los datos con la API
│   ├── db.py                   # Conexión a base de datos y creación de tablas
│   ├── generate_reports.py     # Generación de reportes desde la base de datos
│   └── utils.py                # Funciones utilitarias
├── docker-compose.yml          # Orquestador de contenedores
├── Dockerfile                  # Imagen de la aplicación
├── requirements.txt            # Dependencias de Python
└── README.md                   # Este archivo
```

---

## ⚙️ Requisitos

- Docker y Docker Compose
- Cuenta en GitHub (opcional para clonar el repo)

---

## 🚀 ¿Cómo ejecutar el proyecto?

1. Clona el repositorio:
   ```bash
   git clone https://github.com/viviposada07/BIAEnergy.git
   cd BIAEnergy
   ```

2. Ejecuta los contenedores:
   ```bash
   docker-compose up --build
   ```

3. El sistema:
   - Lee el archivo `data/postcodesgeo.csv`.
   - Llama la API `https://api.postcodes.io` por lotes.
   - Inserta la información en la base de datos PostgreSQL.
   - Genera los reportes en la carpeta `reports/`.

---

## 📊 Reportes generados

- `enriched_postcodes.csv`: archivo enriquecido con la info geográfica.
- `report.xlsx`: contiene:
  - Códigos postales más comunes.
  - Porcentaje de coordenadas sin código postal.
  - Estadísticas generales.

---

## 🛡️ Validaciones y manejo de errores

- Detección de duplicados (por latitud y longitud).
- Logs de errores insertados en una tabla `error_log`.
- Evita reintentos si ya existen las coordenadas.

---

## 🗄️ Base de Datos

El sistema crea las siguientes tablas automáticamente:

- `enriched_postcodes`
- `error_log`

Incluyen una columna `load_dts` con la fecha y hora de carga.

---

## 📫 Contacto

Proyecto desarrollado por **Viviana Posada Restrepo** como parte del proceso de selección para el cargo de **Ingeniera de Datos en Bia Energía**.
