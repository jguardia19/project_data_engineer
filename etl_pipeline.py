#!/usr/bin/env python3
"""
Pipeline ETL Principal
Desarrollado con asistencia de Augment AI Assistant

Orquesta los procesos de Extracción, Transformación y Carga
"""
import pandas as pd
import time
import schedule
import argparse
from etl.extraction import DataExtractor
from etl.transformation import DataTransformer
from etl.loading import DataLoader


class ETLPipeline:
    """Pipeline ETL completo"""

    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()

    def save_sent_data(self, df_sent, clean_data):
        """Guarda registro de datos enviados"""
        if df_sent is None or df_sent.empty:
            df_sent = pd.DataFrame()

        # Concatenar datos enviados
        df_sent = pd.concat([df_sent, clean_data], ignore_index=True)

        # Guardar archivo de control
        df_sent.to_csv("eventosdetectadosnvidia_inHiveQL.csv", index=False)
        print("💾 Archivo de control actualizado")

    def process_csv_and_insert_into_hive(self, debug=False):
        """
        Proceso ETL completo

        Args:
            debug: Activar modo debug

        Returns:
            bool: True si exitoso
        """
        try:
            print("🚀 Iniciando proceso ETL...")

            # EXTRACCIÓN
            df_nvidia, df_sent, flags = self.extractor.extract_data(debug)

            if flags['error']:
                print("❌ Error en extracción - cancelando job")
                return False

            # TRANSFORMACIÓN
            clean_data = self.transformer.transform_data(
                df_nvidia, df_sent, flags, debug)

            if clean_data.empty:
                print("⚠️ No hay datos nuevos para procesar")
                return True

            print(f"📊 Datos a procesar: {len(clean_data)} registros")

            # CARGA
            if self.loader.load_data(clean_data, debug):
                # Actualizar archivo de control
                self.extractor.delete_sent_file()
                self.save_sent_data(df_sent, clean_data)
                print("✅ Proceso ETL completado exitosamente")
                return True
            else:
                print("❌ Error en carga de datos")
                return False

        except Exception as e:
            print(f"❌ Error en pipeline ETL: {e}")
            return False

    def run_scheduled(self, debug=False):
        """Ejecuta ETL con scheduler"""
        schedule.every(10).seconds.do(
            lambda: self.process_csv_and_insert_into_hive(debug)
        )

        last = None
        while True:
            schedule.run_pending()

            next_run = schedule.next_run()
            if next_run != last:
                print(f"⏰ Próxima ejecución: {next_run}")
            last = next_run

            time.sleep(1)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Pipeline ETL Modular")
    parser.add_argument('--debug', action='store_true',
                        help="Activar modo debug")
    parser.add_argument('--once', action='store_true',
                        help="Ejecutar una sola vez")

    args = parser.parse_args()

    pipeline = ETLPipeline()

    if args.once:
        # Ejecutar una sola vez
        pipeline.process_csv_and_insert_into_hive(args.debug)
    else:
        # Ejecutar con scheduler
        pipeline.run_scheduled(args.debug)


if __name__ == '__main__':
    main()
