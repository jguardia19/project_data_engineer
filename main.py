#!/usr/bin/env python3
"""
MAIN.PY - Sistema Completo YOLO + Hive ETL
Ejecuta clasificación de imágenes/videos y carga a Hive
"""
import os
import sys
import time
from datetime import datetime

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sistema_clasificacion import SistemaClasificacion
from sistema_batch_etl import SistemaBatchETL

def main():
    """Función principal que ejecuta todo el pipeline"""
    print("🤖 SISTEMA COMPLETO: YOLO + HIVE ETL")
    print("=" * 50)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. CLASIFICACIÓN CON YOLO
        print("\n📸 FASE 1: CLASIFICACIÓN DE IMÁGENES/VIDEOS")
        print("-" * 40)
        
        clasificador = SistemaClasificacion()
        
        # Procesar imágenes
        num_imagenes = clasificador.procesar_imagenes('imagenes_entrada')
        print(f"✅ Procesadas {num_imagenes} imágenes")
        
        # Procesar videos
        num_videos = clasificador.procesar_videos('videos_entrada')
        print(f"✅ Procesados {num_videos} videos")
        
        # Guardar CSV
        if clasificador.guardar_csv():
            print(f"✅ Guardadas {len(clasificador.detecciones)} detecciones en CSV")
        else:
            print("❌ Error guardando CSV")
            return False
        
        # 2. ETL A HIVE
        print("\n📤 FASE 2: CARGA ETL A HIVE")
        print("-" * 40)
        
        etl = SistemaBatchETL()
        
        # Conectar a Hive
        if etl.conectar_hive():
            print("✅ Conectado a Hive")
        else:
            print("❌ Error conectando a Hive")
            return False
        
        # Crear tabla si no existe
        if etl.crear_tabla():
            print("✅ Tabla verificada/creada")
        else:
            print("❌ Error creando tabla")
            return False
        
        # Cargar datos con batch processing optimizado
        registros_cargados = etl.cargar_csv_a_hive(
            archivo_csv='detecciones_yolo.csv',
            batch_size=500,  # Lotes de 500 registros
            debug=False      # Cambiar a True para ver queries
        )
        if registros_cargados > 0:
            print(f"✅ Cargados {registros_cargados} registros a Hive")
        else:
            print("❌ Error cargando datos")
            return False
        
        # 3. RESUMEN FINAL
        print("\n📊 RESUMEN FINAL")
        print("-" * 40)
        print(f"Imágenes procesadas: {num_imagenes}")
        print(f"Videos procesados: {num_videos}")
        print(f"Total detecciones: {len(clasificador.detecciones)}")
        print(f"Registros en Hive: {registros_cargados}")
        
        # Estadísticas
        etl.mostrar_estadisticas()
        
        print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False
    
    finally:
        # Limpiar conexiones
        try:
            if 'etl' in locals():
                etl.cerrar_conexion()
        except:
            pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
