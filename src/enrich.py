import pandas as pd
from api_client import fetch_bulk_postcodes
from sqlalchemy import text
import time

def enrich_and_store(engine, input_path, output_path):
    df = pd.read_csv(input_path)
    df.drop_duplicates(subset=["lat", "lon"], inplace=True)

    # Variables de monitoreo
    duplicates_enriched = 0
    duplicates_errors = 0
    enriched_rows = []  # Solo para guardar CSV al final

    batch_size = 100
    for i in range(0, len(df), batch_size):
        chunk = df.iloc[i:i+batch_size].to_dict("records")
        print(f"Procesando lote {i//batch_size + 1}, coordenadas: {len(chunk)}.")

        results = fetch_bulk_postcodes(chunk)

        with engine.begin() as conn:
            for entry in results:
                query = entry.get("query")
                result_list = entry.get("result")

                if result_list and isinstance(result_list, list):
                    top = result_list[0]
                    enriched = {
                        "latitude": query["latitude"],
                        "longitude": query["longitude"],
                        "postcode": top.get("postcode"),
                        "admin_district": top.get("admin_district"),
                        "country": top.get("country"),
                        "region": top.get("region"),
                        "longitude_api": top.get("longitude"),
                        "latitude_api": top.get("latitude")
                    }

                    enriched_rows.append(enriched)

                    result = conn.execute(text("""
                        INSERT INTO public.enriched_postcodes 
                        (latitude, longitude, postcode, admin_district, country, region, longitude_api, latitude_api)
                        VALUES (:latitude, :longitude, :postcode, :admin_district, :country, :region, :longitude_api, :latitude_api)
                        ON CONFLICT (latitude, longitude) DO NOTHING
                    """), enriched)

                    if result.rowcount == 0:
                        duplicates_enriched += 1

                    print(f"{query}: {top.get('postcode')}")
                else:
                    error = {
                        "latitude": query["latitude"],
                        "longitude": query["longitude"],
                        "error_message": "No se encontró código postal"
                    }

                    result = conn.execute(text("""
                        INSERT INTO public.error_log (latitude, longitude, error_message)
                        VALUES (:latitude, :longitude, :error_message)
                        ON CONFLICT (latitude, longitude) DO NOTHING
                    """), error)

                    if result.rowcount == 0:
                        duplicates_errors += 1

                    print(f"Sin información: {query}")

        time.sleep(1)  # Control de tasa ante API

    # Guardamos CSV al final
    pd.DataFrame(enriched_rows).to_csv(output_path, index=False)
    print("Archivo enriched_postcodes.csv guardado con éxito.")
    print(f"Duplicados ignorados en enriched_postcodes: {duplicates_enriched}")
    print(f"Duplicados ignorados en error_log: {duplicates_errors}")
