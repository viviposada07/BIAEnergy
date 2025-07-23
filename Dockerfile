FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar el script al contenedor
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Usar el script como entrypoint
ENTRYPOINT ["/wait-for-db.sh"]
CMD ["python", "src/main.py"]