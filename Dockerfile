FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script a /app
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Luego copias todo lo demás
COPY . .

RUN chmod +x /wait-for-db.sh

ENTRYPOINT ["/wait-for-db.sh"]
CMD ["python", "src/main.py"]