#!/usr/bin/env python3
"""
Prueba del sistema de clasificación con tus imágenes
"""
import sys
import os
sys.path.append('procesosbatch')

from main import DeteccionInfracciones

def test_clasificacion():
    print("🔍 INICIANDO PRUEBA DE CLASIFICACIÓN")
    
    # Verificar que existan imágenes
    if not os.path.exists('imagenes_entrada'):
        print("❌ Carpeta imagenes_entrada no existe")
        return False
    
    imagenes = [f for f in os.listdir('imagenes_entrada') 
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not imagenes:
        print("❌ No hay imágenes en imagenes_entrada")
        return False
    
    print(f"📸 Encontradas {len(imagenes)} imágenes:")
    for img in imagenes:
        print(f"  - {img}")
    
    # Crear detector
    detector = DeteccionInfracciones(
        modelo_yolo_path='yolo11n.pt',
        archivo_csv='detecciones_prueba.csv',
        carpeta_imagenes='imagenes_entrada',
        carpeta_videos='videos_entrada'
    )
    
    # Procesar solo imágenes
    detector.iniciar_procesamiento_batch()
    
    # Verificar resultados
    if os.path.exists('detecciones_prueba.csv'):
        import pandas as pd
        df = pd.read_csv('detecciones_prueba.csv')
        print(f"✅ CSV generado con {len(df)} detecciones")
        print("\n📊 Primeras 3 detecciones:")
        print(df.head(3)[['source_id', 'class_name', 'confidence', 'dominant_color_name']])
        return True
    else:
        print("❌ No se generó el CSV")
        return False

if __name__ == "__main__":
    test_clasificacion()