from src.sistema_clasificacion import SistemaClasificacion
from src.sistema_batch_etl import SistemaBatchETL
import os

def ejecutar_pipeline_completo():
    print("🚀 INICIANDO PIPELINE COMPLETO YOLO → HIVE")
    print("=" * 50)
    
    # FASE 1: CLASIFICACIÓN CON YOLO
    print("\n📸 FASE 1: CLASIFICACIÓN DE IMÁGENES Y VIDEOS")
    print("-" * 40)
    
    sistema = SistemaClasificacion()
    
    # Procesar imágenes
    imagenes_procesadas = sistema.procesar_imagenes('imagenes_entrada')
    print(f"✅ Procesadas {imagenes_procesadas} imágenes")
    
    # Procesar videos
    videos_procesados = sistema.procesar_videos('videos_entrada')
    print(f"✅ Procesados {videos_procesados} videos")
    
    # Guardar CSV
    if sistema.guardar_csv('detecciones_yolo.csv'):
        print(f"✅ CSV generado con {len(sistema.detecciones)} detecciones")
    else:
        print("❌ Error generando CSV")
        return False
    
    # FASE 2: ETL A HIVE
    print("\n📤 FASE 2: CARGA ETL A HIVE")
    print("-" * 40)
    
    etl = SistemaBatchETL()
    
    # Conectar a Hive
    if etl.conectar_hive():
        print("✅ Conectado a Hive")
    else:
        print("❌ Error conectando a Hive")
        return False
    
    # Crear tabla
    if etl.crear_tabla():
        print("✅ Tabla verificada/creada")
    else:
        print("❌ Error creando tabla")
        return False
    
    # Cargar datos
    registros_cargados = etl.cargar_csv_a_hive('detecciones_yolo.csv')
    if registros_cargados > 0:
        print(f"✅ Cargados {registros_cargados} registros a Hive")
    else:
        print("❌ Error cargando datos")
        return False
    
    # Mostrar estadísticas
    etl.mostrar_estadisticas()
    
    # Cerrar conexión
    etl.cerrar_conexion()
    
    print("\n🎉 ¡PIPELINE COMPLETO EJECUTADO EXITOSAMENTE!")
    return True

if __name__ == "__main__":
    ejecutar_pipeline_completo()