from db import get_engine, create_tables
from enrich import enrich_and_store
from generate_reports import generate_reports
import os

def main():
    engine = get_engine()
    create_tables(engine)
    enrich_and_store(engine, "data/postcodesgeo.csv", "reports/enriched_postcodes.csv")
    generate_reports(engine)
    print("📊 Reporte de estadísticas generado correctamente.")


if __name__ == "__main__":
    main()
