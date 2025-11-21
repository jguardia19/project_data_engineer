#!/usr/bin/env python3
"""
Script de prueba para verificar que todo funciona
"""
import os
import sys

def test_imports():
    """Prueba todas las importaciones"""
    print("🧪 PROBANDO IMPORTACIONES...")
    
    try:
        import cv2
        print("✅ OpenCV")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ YOLO")
    except ImportError as e:
        print(f"❌ YOLO: {e}")
        return False
    
    try:
        from pyhive import hive
        print("✅ PyHive")
    except ImportError as e:
        print(f"❌ PyHive: {e}")
        return False
    
    return True

def test_hive_connection():
    """Prueba conexión a Hive"""
    print("\n🐘 PROBANDO CONEXIÓN A HIVE...")
    try:
        from pyhive import hive
        conn = hive.Connection(
            host='localhost',
            port=10000,
            username='jose_dev',
            database='default',
            auth='NONE'
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        print("✅ Hive conectado")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Hive: {e}")
        return False

def test_yolo_model():
    """Prueba carga del modelo YOLO"""
    print("\n🎯 PROBANDO MODELO YOLO...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ Modelo YOLO cargado")
        return True
    except Exception as e:
        print(f"❌ YOLO: {e}")
        return False

def main():
    print("🔍 VERIFICANDO SISTEMA COMPLETO")
    print("=" * 40)
    
    tests = [
        test_imports(),
        test_hive_connection(), 
        test_yolo_model()
    ]
    
    if all(tests):
        print("\n🎉 ¡TODO FUNCIONA!")
        return True
    else:
        print("\n❌ HAY PROBLEMAS QUE RESOLVER")
        return False

if __name__ == "__main__":
    main()