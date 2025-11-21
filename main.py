#!/usr/bin/env python3
"""
MAIN PRINCIPAL - Sistema YOLO + Hive con Batches de 10 segundos
"""
import os
import time
from sistema_clasificacion_con_batches import SistemaClasificacionBatches
from sistema_batch_etl import SistemaBatchETL

def main():
    """Pipeline principal con batches automáticos cada 10 segundos"""
    print("🎬 SISTEMA YOLO + HIVE CON BATCHES DE 10 SEGUNDOS")
    print("=" * 60)
    
    # Verificar carpetas necesarias
    carpetas = ['imagenes_entrada', 'videos_entrada', 'data']
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"📁 Carpeta {carpeta} creada")
    
    # Inicializar sistema con batches
    sistema = SistemaClasificacionBatches()
    
    # Procesar videos (automáticamente envía batches cada 10s)
    videos_procesados = sistema.procesar_videos('videos_entrada')
    
    if videos_procesados > 0:
        print(f"\n🎉 ¡PIPELINE COMPLETADO!")
        print(f"📊 {videos_procesados} videos procesados")
        print("📤 Batches enviados automáticamente cada 10 segundos")
    else:
        print("❌ No se encontraron videos para procesar")

if __name__ == "__main__":
    main()


