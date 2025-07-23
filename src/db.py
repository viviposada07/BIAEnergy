from sqlalchemy import create_engine, text
import os

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    return create_engine(db_url)

def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS public.enriched_postcodes (
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                postcode TEXT,
                admin_district TEXT,
                country TEXT,
                region TEXT,
                longitude_api DOUBLE PRECISION,
                latitude_api DOUBLE PRECISION,
                load_dts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (latitude, longitude)
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS public.error_log (
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                error_message TEXT,
                load_dts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (latitude, longitude)
            );
        """))