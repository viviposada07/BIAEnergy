
import pandas as pd
from sqlalchemy import create_engine, text
from db import get_engine
from datetime import datetime

def generate_reports(engine, output_path='reports/report_summary.csv'):
    with engine.begin() as conn:
        print("📊 Generando reporte de códigos postales más comunes...")
        top_postcodes = conn.execute(text('''
            SELECT postcode, COUNT(*) as total
            FROM enriched_postcodes
            WHERE postcode IS NOT NULL
            GROUP BY postcode
            ORDER BY total DESC
            LIMIT 10
        ''')).fetchall()

        print("📈 Calculando estadísticas de calidad de datos...")
        total_coords = conn.execute(text('SELECT COUNT(*) FROM enriched_postcodes')).scalar()
        coords_without_postcode = conn.execute(text('SELECT COUNT(*) FROM enriched_postcodes WHERE postcode IS NULL')).scalar()
        pct_without_postcode = (coords_without_postcode / total_coords) * 100 if total_coords else 0

        report_data = {
            "Fecha de generación": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Total coordenadas": [total_coords],
            "Coordenadas sin código postal": [coords_without_postcode],
            "Porcentaje sin código postal": [f"{pct_without_postcode:.2f}%"]
        }

        df_stats = pd.DataFrame(report_data)
        df_top_postcodes = pd.DataFrame(top_postcodes, columns=["Código Postal", "Frecuencia"])

        print("💾 Guardando reporte en CSV...")
        with pd.ExcelWriter(output_path.replace(".csv", ".xlsx")) as writer:
            df_stats.to_excel(writer, sheet_name="Estadísticas Generales", index=False)
            df_top_postcodes.to_excel(writer, sheet_name="Postcodes Más Comunes", index=False)

        print(f"✅ Reporte generado en {output_path.replace('.csv', '.xlsx')}")

if __name__ == '__main__':
    engine = get_engine()
    generate_reports(engine)