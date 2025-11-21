#!/usr/bin/env python3
"""
Sistema Batch ETL - Carga CSV a Hive
Ubicado en sesion_5_y_6/
"""
import pandas as pd
from pyhive import hive
import subprocess
import os
from datetime import datetime

class SistemaBatchETL:
    def __init__(self):
        # Usar configuración exacta del test exitoso
        self.hive_host = 'localhost'
        self.hive_port = 10000
        self.database = 'yolo_project'
        self.tabla = 'yolo_objects'
        self.username = 'jose_dev'
        self.conn = None
        
        print(f"🔧 ETL configurado para Hive en {self.hive_host}:{self.hive_port}")
    
    def _get_wsl_ip(self):
        """Obtener IP de WSL desde Windows"""
        try:
            result = subprocess.run(['wsl', 'hostname', '-I'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                wsl_ip = result.stdout.strip().split()[0]
                print(f"🌐 IP de WSL detectada: {wsl_ip}")
                return wsl_ip
        except Exception as e:
            print(f"⚠️ No se pudo obtener IP de WSL: {e}")
        
        return 'localhost'
    
    def conectar_hive(self):
        """Conectar a HiveServer2 usando configuración que funciona"""
        try:
            print(f"🔗 Conectando a {self.hive_host}:{self.hive_port}...")
            self.conn = hive.Connection(
                host='localhost', 
                port=10000,
                database='default',
                username='jose_dev',
                auth='NONE' 
            )
            print("✅ Conectado a HiveServer2")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Hive: {e}")
            return False
    
    def crear_base_datos_y_tabla(self):
        """Crear base de datos y tabla si no existen"""
        try:
            cursor = self.conn.cursor()
            
            # Crear base de datos
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
            cursor.execute(f'USE {self.database}')
            print(f"✅ Base de datos {self.database} lista")
            
            # Crear tabla con todos los campos del CSV
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.tabla} (
                source_type STRING,
                source_id STRING,
                frame_number INT,
                class_id INT,
                class_name STRING,
                confidence DOUBLE,
                x_min INT,
                y_min INT,
                x_max INT,
                y_max INT,
                width INT,
                height INT,
                area_pixels INT,
                frame_width INT,
                frame_height INT,
                bbox_area_ratio DOUBLE,
                center_x DOUBLE,
                center_y DOUBLE,
                center_x_norm DOUBLE,
                center_y_norm DOUBLE,
                position_region STRING,
                dominant_color_name STRING,
                dom_r INT,
                dom_g INT,
                dom_b INT,
                timestamp_sec DOUBLE,
                ingestion_date STRING,
                detection_id STRING
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            """
            
            cursor.execute(create_table_sql)
            print(f"✅ Tabla {self.tabla} verificada/creada")
            return True
            
        except Exception as e:
            print(f"❌ Error creando tabla: {e}")
            return False
    
    def cargar_csv_a_hive(self, csv_file='detecciones_prueba.csv'):
        """Cargar CSV a Hive"""
        if not os.path.exists(csv_file):
            print(f"❌ No se encontró {csv_file}")
            return 0
        
        try:
            # Leer CSV
            df = pd.read_csv(csv_file)
            print(f"📊 Cargando {len(df)} registros...")
            
            cursor = self.conn.cursor()
            cursor.execute(f'USE {self.database}')
            
            # Insertar registros uno por uno
            registros_insertados = 0
            
            for _, row in df.iterrows():
                insert_sql = f"""
                INSERT INTO {self.tabla} VALUES (
                    '{row['source_type']}', '{row['source_id']}', {row['frame_number']},
                    {row['class_id']}, '{row['class_name']}', {row['confidence']},
                    {row['x_min']}, {row['y_min']}, {row['x_max']}, {row['y_max']},
                    {row['width']}, {row['height']}, {row['area_pixels']},
                    {row['frame_width']}, {row['frame_height']}, {row['bbox_area_ratio']},
                    {row['center_x']}, {row['center_y']}, {row['center_x_norm']}, {row['center_y_norm']},
                    '{row['position_region']}', '{row['dominant_color_name']}',
                    {row['dom_r']}, {row['dom_g']}, {row['dom_b']},
                    {row['timestamp_sec']}, '{row['ingestion_date']}', '{row['detection_id']}'
                )
                """
                
                cursor.execute(insert_sql)
                registros_insertados += 1
                
                if registros_insertados % 10 == 0:
                    print(f"📤 Insertados {registros_insertados}/{len(df)} registros...")
            
            print(f"✅ Cargados {registros_insertados} registros a Hive")
            return registros_insertados
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return 0
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas de la tabla"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'USE {self.database}')
            
            # Total registros
            cursor.execute(f'SELECT COUNT(*) FROM {self.tabla}')
            total = cursor.fetchone()[0]
            print(f"📊 Total registros en Hive: {total}")
            
            # Por clase
            cursor.execute(f'SELECT class_name, COUNT(*) FROM {self.tabla} GROUP BY class_name')
            clases = cursor.fetchall()
            print("🎯 Distribución por clase:")
            for clase, count in clases:
                print(f"   {clase}: {count}")
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
    
    def cerrar_conexion(self):
        """Cerrar conexión a Hive"""
        if self.conn:
            self.conn.close()
            print("🔌 Conexión a Hive cerrada")

if __name__ == "__main__":
    print("📤 SISTEMA BATCH ETL - PRUEBA INDEPENDIENTE")
    
    etl = SistemaBatchETL()
    
    if etl.conectar_hive():
        if etl.crear_base_datos_y_tabla():
            registros = etl.cargar_csv_a_hive()
            if registros > 0:
                etl.mostrar_estadisticas()
        etl.cerrar_conexion()



