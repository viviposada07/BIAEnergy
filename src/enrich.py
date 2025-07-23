import pandas as pd
from api_client import fetch_bulk_postcodes
from sqlalchemy import text
import time

def enrich_and_store(engine, input_path, output_path):
    df = pd.read_csv(input_path)
    df.drop_duplicates(subset=["latitude", "longitude"], inplace=True)

    enriched_rows = []
    errors = []

    # Limita para pruebas (opcional)
    df = df.head(1000)

    # Divide en chunks de 100
    batch_size = 100
    for i in range(0, len(df), batch_size):
        chunk = df.iloc[i:i+batch_size].to_dict("records")
        print(f"📦 Procesando lote {i//batch_size + 1} con {len(chunk)} coordenadas...")

        results = fetch_bulk_postcodes(chunk)  # AQUÍ estaba el error

        for entry in results:
            query = entry.get("query")
            result_list = entry.get("result")

            if result_list and isinstance(result_list, list):
                top = result_list[0]  # usamos solo el primer resultado
                enriched_rows.append({
                    "latitude": query["latitude"],
                    "longitude": query["longitude"],
                    "postcode": top.get("postcode"),
                    "admin_district": top.get("admin_district"),
                    "country": top.get("country"),
                    "region": top.get("region"),
                    "longitude_api": top.get("longitude"),
                    "latitude_api": top.get("latitude")
                })
                print(f"✅ {query} → {top.get('postcode')}")
            else:
                errors.append({
                    "latitude": query["latitude"],
                    "longitude": query["longitude"],
                    "error_message": "No se encontró código postal"
                })
                print(f"❌ Sin resultado para {query}")

        time.sleep(1)  # Evita bloqueo de la API

    # Guardar en BD
    duplicates_enriched = 0
    duplicates_errors = 0

    with engine.begin() as conn:
        for r in enriched_rows:
            result = conn.execute(text("""
                INSERT INTO public.enriched_postcodes 
                (latitude, longitude, postcode, admin_district, country, region, longitude_api, latitude_api)
                VALUES (:latitude, :longitude, :postcode, :admin_district, :country, :region, :longitude_api, :latitude_api)
                ON CONFLICT (latitude, longitude) DO NOTHING
            """), r)
            if result.rowcount == 0:
                duplicates_enriched += 1

        for e in errors:
            result = conn.execute(text("""
                INSERT INTO public.error_log (latitude, longitude, error_message)
                VALUES (:latitude, :longitude, :error_message)
                ON CONFLICT (latitude, longitude) DO NOTHING
            """), e)
            if result.rowcount == 0:
                duplicates_errors += 1

    # Guardar CSV enriquecido
    pd.DataFrame(enriched_rows).to_csv(output_path, index=False)
    print("📁 Archivo enriched_postcodes.csv guardado correctamente.")
    print(f"⚠️  Duplicados ignorados en enriched_postcodes: {duplicates_enriched}")
    print(f"⚠️  Duplicados ignorados en error_log: {duplicates_errors}")