#!/usr/bin/env python3
"""
Ejecutor principal del proyecto - Dos sistemas separados
"""
import subprocess
import sys
import time

def ejecutar_clasificacion():
    """Ejecuta SOLO el sistema de clasificación"""
    print("🔍 Iniciando Sistema de Clasificación...")
    result = subprocess.run([sys.executable, "procesosbatch/main.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Clasificación completada")
        return True
    else:
        print(f"❌ Error en clasificación: {result.stderr}")
        return False

def ejecutar_etl():
    """Ejecuta SOLO el sistema ETL"""
    print("📤 Iniciando Sistema ETL...")
    result = subprocess.run([sys.executable, "procesosbatch/proceso_csv_and_insert_into_hive.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ ETL completado")
        return True
    else:
        print(f"❌ Error en ETL: {result.stderr}")
        return False

if __name__ == "__main__":
    print("=== PROYECTO: SISTEMAS SEPARADOS ===")
    
    # 1. Ejecutar clasificación
    if ejecutar_clasificacion():
        # 2. Esperar un momento
        time.sleep(2)
        
        # 3. Ejecutar ETL
        ejecutar_etl()
    
    print("=== PROYECTO COMPLETADO ===")