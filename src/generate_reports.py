
import pandas as pd
from sqlalchemy import text
from db import get_engine
from datetime import datetime

def generate_reports(engine):
    with engine.begin() as conn:
        print("Reporte códigos postales más comunes en el dataset.")
        top_postcodes = conn.execute(text('''
            SELECT trim(postcode), COUNT(*) as total
            FROM enriched_postcodes
            WHERE postcode IS NOT NULL
            GROUP BY 1
            HAVING COUNT(*) > 1
            ORDER BY total DESC
        ''')).fetchall()

        print("Calculo de estadisticas - Calidad de datos")
        total_coords = conn.execute(text('SELECT COUNT(*) FROM enriched_postcodes')).scalar()
        coords_without_postcode = conn.execute(text('''
                                                    SELECT COUNT(*) 
                                                    FROM public.error_log 
                                                    WHERE error_message = 'No se encontró código postal'
                                                    ''')).scalar()
        pct_without_postcode = (coords_without_postcode / total_coords) * 100 if total_coords else 0

        report_data = {
            "Fecha de generacion": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Total coordenadas": [total_coords],
            "Coordenadas sin codigo postal": [coords_without_postcode],
            "Porcentaje sin codigo postal": [f"{pct_without_postcode:.2f}%"]
        }

        df_stats = pd.DataFrame(report_data)
        df_top_postcodes = pd.DataFrame(top_postcodes, columns=["Código Postal", "Frecuencia"])

        print("Guardamos el reporte en CSV")
        fecha = datetime.now().strftime("%Y%m%d")
        output_path = f"reports/datos_estadisticas_{fecha}.xlsx"
        with pd.ExcelWriter(output_path) as writer:
            df_stats.to_excel(writer, sheet_name="Estadísticas generales", index=False)
            df_top_postcodes.to_excel(writer, sheet_name="Códigos postales más comunes en el dataset", index=False)

        print(f"Archivo generado en {output_path.replace('.csv', '.xlsx')}")

if __name__ == '__main__':
    engine = get_engine()
    generate_reports(engine)