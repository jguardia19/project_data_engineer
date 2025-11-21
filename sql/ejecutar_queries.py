#!/usr/bin/env python3
"""
Ejecutor de queries SQL para análisis de datos YOLO
"""
from pyhive import hive
import os
import glob

def conectar_hive():
    """Conectar a Hive usando configuración que funciona"""
    try:
        conn = hive.Connection(
            host='localhost',
            port=10000,
            database='yolo_project',
            username='jose_dev',
            auth='NONE'
        )
        print("✅ Conectado a Hive")
        return conn
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return None

def ejecutar_query_desde_archivo(conn, archivo_sql):
    """Ejecutar query desde archivo SQL"""
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Dividir por queries individuales (separadas por ;)
        queries = [q.strip() for q in contenido.split(';') if q.strip() and not q.strip().startswith('--')]
        
        cursor = conn.cursor()
        
        for i, query in enumerate(queries):
            if query:
                print(f"\n🔍 Ejecutando query {i+1} de {archivo_sql}:")
                print("-" * 50)
                
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                if resultados:
                    # Mostrar primeras 10 filas
                    for j, fila in enumerate(resultados[:10]):
                        print(f"  {fila}")
                    
                    if len(resultados) > 10:
                        print(f"  ... y {len(resultados) - 10} filas más")
                else:
                    print("  (Sin resultados)")
                
                print(f"✅ Query completada: {len(resultados)} resultados")
        
    except Exception as e:
        print(f"❌ Error ejecutando {archivo_sql}: {e}")

def main():
    """Ejecutar todos los queries SQL"""
    print("📊 EJECUTOR DE QUERIES SQL - ANÁLISIS YOLO")
    print("=" * 50)
    
    conn = conectar_hive()
    if not conn:
        return
    
    # Buscar todos los archivos SQL
    archivos_sql = sorted(glob.glob('sql/*.sql'))
    
    if not archivos_sql:
        print("❌ No se encontraron archivos SQL en la carpeta sql/")
        return
    
    print(f"📁 Encontrados {len(archivos_sql)} archivos SQL")
    
    for archivo in archivos_sql:
        print(f"\n🚀 PROCESANDO: {archivo}")
        print("=" * 60)
        ejecutar_query_desde_archivo(conn, archivo)
        
        input("\n⏸️  Presiona ENTER para continuar con el siguiente archivo...")
    
    conn.close()
    print("\n🎉 ¡Análisis completado!")

if __name__ == "__main__":
    main()