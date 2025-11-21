#!/usr/bin/env python3
"""
Configuraciones del sistema YOLO + Hive
"""

# Configuración de Hive
HIVE_CONFIG = {
    'host': 'localhost',
    'port': 10000,
    'username': 'jose_dev',
    'database': 'yolo_project',
    'auth': 'NONE'
}

# Configuración de batches
BATCH_DURACION_SEGUNDOS = 10
BATCH_TAMAÑO_MAXIMO = 100

# Configuración de YOLO
YOLO_MODEL = 'yolov8n.pt'
CONFIDENCE_THRESHOLD = 0.5

# Carpetas
CARPETA_IMAGENES = 'imagenes_entrada'
CARPETA_VIDEOS = 'videos_entrada'
CARPETA_DATA = 'data'