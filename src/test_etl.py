#!/usr/bin/env python3
"""
Prueba del sistema ETL con el CSV generado
"""
import sys
import os
sys.path.append('procesosbatch')

from proceso_csv_and_insert_into_hive import SistemaBatchETL

def test_etl():
    print("📤 INICIANDO PRUEBA DEL SISTEMA ETL")
    
    # Verificar que existe el CSV
    csv_file = 'detecciones_prueba.csv'
    if not os.path.exists(csv_file):
        print(f"❌ No se encontró {csv_file}")
        return False
    
    print(f"✅ CSV encontrado: {csv_file}")
    
    # Crear sistema ETL
    etl = SistemaBatchETL(csv_path=csv_file)
    
    # Ejecutar proceso ETL
    resultado = etl.process_csv_and_insert_into_hive(debug=True)
    
    if resultado:
        print("✅ ETL ejecutado exitosamente")
        
        # Mostrar estadísticas
        if os.path.exists('processed_detection_ids.txt'):
            with open('processed_detection_ids.txt', 'r') as f:
                ids_procesados = f.readlines()
            print(f"📊 IDs procesados guardados: {len(ids_procesados)}")
        
        return True
    else:
        print("❌ Error en el proceso ETL")
        return False

if __name__ == "__main__":
    test_etl()
