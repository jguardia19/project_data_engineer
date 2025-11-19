#!/usr/bin/env python3
"""
Limpieza completa del proyecto - Eliminar archivos innecesarios
"""
import os
import shutil
import glob

def limpiar_proyecto():
    print("🧹 LIMPIANDO PROYECTO - ELIMINANDO ARCHIVOS INNECESARIOS")
    print("=" * 60)
    
    # 1. Archivos de prueba y temporales
    archivos_eliminar = [
        'test_*.py',
        'debug_*.py', 
        'verificar_*.py',
        'crear_*.py',
        'organizar_*.py',
        'check_*.py',
        'sistema_video_*.py',
        '*_prueba.csv',
        'detecciones_videos.csv',
        'detecciones_prueba.csv'
    ]
    
    print("🗑️ ELIMINANDO ARCHIVOS DE PRUEBA:")
    for patron in archivos_eliminar:
        archivos = glob.glob(patron)
        for archivo in archivos:
            if os.path.exists(archivo):
                os.remove(archivo)
                print(f"❌ {archivo}")
    
    # 2. Carpetas innecesarias
    carpetas_eliminar = [
        'procesosbatch',
        '__pycache__',
        '.pytest_cache',
        'logs',
        'sql_scripts'
    ]
    
    print("\n🗂️ ELIMINANDO CARPETAS INNECESARIAS:")
    for carpeta in carpetas_eliminar:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            print(f"❌ {carpeta}/")
    
    # 3. Archivos de configuración duplicados
    archivos_config_duplicados = [
        'requirements_tf_ubuntu.txt',
        'Makefile.bak',
        'README.bak'
    ]
    
    print("\n📄 ELIMINANDO ARCHIVOS DUPLICADOS:")
    for archivo in archivos_config_duplicados:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"❌ {archivo}")
    
    # 4. Limpiar archivos Python compilados
    print("\n🐍 LIMPIANDO ARCHIVOS PYTHON COMPILADOS:")
    for root, dirs, files in os.walk('.'):
        # Eliminar __pycache__
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"❌ {pycache_path}")
        
        # Eliminar .pyc
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                os.remove(pyc_path)
                print(f"❌ {pyc_path}")
    
    print("\n✅ LIMPIEZA COMPLETADA")
    
    # 5. Mostrar estructura final limpia
    print("\n📁 ESTRUCTURA FINAL DEL PROYECTO:")
    mostrar_estructura()

def mostrar_estructura():
    """Muestra la estructura limpia del proyecto"""
    estructura_esperada = [
        'src/',
        'tests/',
        'imagenes_entrada/',
        'videos_entrada/',
        'README.md',
        'Makefile',
        'requirements.txt',
        '.gitignore'
    ]
    
    for item in estructura_esperada:
        if os.path.exists(item):
            if item.endswith('/'):
                archivos = len(os.listdir(item.rstrip('/')))
                print(f"✅ {item} ({archivos} archivos)")
            else:
                print(f"✅ {item}")
        else:
            print(f"❌ {item} - FALTA")

def confirmar_limpieza():
    """Confirma antes de eliminar"""
    print("⚠️  ESTA OPERACIÓN ELIMINARÁ ARCHIVOS PERMANENTEMENTE")
    print("¿Continuar con la limpieza? (s/n): ", end="")
    respuesta = input().lower()
    return respuesta == 's'

if __name__ == "__main__":
    if confirmar_limpieza():
        limpiar_proyecto()
    else:
        print("❌ Limpieza cancelada")