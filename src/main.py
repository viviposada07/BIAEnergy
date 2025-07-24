from db import get_engine, create_tables
from enrich import enrich_and_store
from generate_reports import generate_reports
from datetime import datetime
import os

def main():
    engine = get_engine()
    create_tables(engine)

    fecha_actual = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"codigos_postales_{fecha_actual}"

    enrich_and_store(engine, "data/postcodesgeo.csv", f"reports/{nombre_archivo}.csv")
    generate_reports(engine)
    print("Reporte de estadísticas generado correctamente.")

if __name__ == "__main__":
    main()