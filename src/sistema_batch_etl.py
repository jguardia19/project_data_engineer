import pandas as pd
from pyhive import hive
import math
from datetime import datetime

class SistemaBatchETL:
    """Sistema ETL para cargar datos YOLO a Hive"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.hive_config = {
            'host': '172.25.54.102',  # IP de WSL
            'port': 10000,
            'database': 'yolo_project',
            'username': 'jose_dev',
            'auth': 'NOSASL'
        }
    
    def str_literal(self, value):
        """Convierte valor a string literal SQL seguro"""
        if pd.isna(value) or value is None:
            return 'NULL'
        return f"'{str(value).replace(chr(39), chr(39)+chr(39))}'"  # Escapar comillas simples
    
    def conectar_hive(self):
        """Conecta a HiveServer2"""
        try:
            print("🔗 Conectando a Hive...")
            self.conn = hive.Connection(**self.hive_config)
            self.cursor = self.conn.cursor()
            print("✅ Conectado a Hive exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Hive: {e}")
            return False
    
    def crear_tabla(self):
        """Crea la base de datos y tabla si no existen"""
        try:
            # Crear base de datos
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS yolo_project")
            self.cursor.execute("USE yolo_project")
            
            # Crear tabla
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS yolo_objects (
                    imagen STRING,
                    clase STRING,
                    confianza DOUBLE,
                    x INT,
                    y INT,
                    ancho INT,
                    alto INT,
                    timestamp_proc STRING
                ) STORED AS TEXTFILE
            """
            
            self.cursor.execute(create_table_sql)
            print("✅ Tabla yolo_objects verificada/creada")
            return True
            
        except Exception as e:
            print(f"❌ Error creando tabla: {e}")
            return False
    
    def cargar_csv_a_hive(self, archivo_csv, batch_size=1000, debug=False):
        """Carga datos del CSV a Hive usando batch processing optimizado"""
        try:
            # Leer CSV
            df = pd.read_csv(archivo_csv)
            print(f"📊 Datos leídos: {len(df)} registros")
            
            # Limpiar datos
            clean_data = df.dropna()
            print(f"� Datos limpios: {len(clean_data)} registros")
            
            if len(clean_data) == 0:
                print("❌ No hay datos válidos para cargar")
                return 0
            
            # Configurar batch processing
            n = len(clean_data)
            total_batches = math.ceil(n / batch_size)
            table_name = "yolo_objects"
            cols = "(imagen, clase, confianza, x, y, ancho, alto, timestamp_proc)"
            
            print(f"📤 Cargando {n} registros en {total_batches} lotes de {batch_size}...")
            
            registros_cargados = 0
            
            # Procesar en lotes
            for i, start in enumerate(range(0, n, batch_size), start=1):
                chunk = clean_data.iloc[start:start+batch_size]
                print(f"📦 Enviando paquete {i} de {total_batches}... ({len(chunk)} registros)")
                
                values = []
                for _, row in chunk.iterrows():
                    imagen = self.str_literal(row.get('imagen'))
                    clase = self.str_literal(row.get('clase'))
                    confianza = row.get('confianza', 0.0)
                    x = int(row.get('x', 0))
                    y = int(row.get('y', 0))
                    ancho = int(row.get('ancho', 0))
                    alto = int(row.get('alto', 0))
                    timestamp_proc = self.str_literal(row.get('timestamp_proc'))
                    
                    tuple_sql = f"({imagen},{clase},{confianza},{x},{y},{ancho},{alto},{timestamp_proc})"
                    values.append(tuple_sql)
                
                # Ejecutar INSERT batch
                query = f"INSERT INTO {table_name} {cols} VALUES {', '.join(values)}"
                
                if debug:
                    print(f"🔍 Query: {query[:200]}...")  # Mostrar solo primeros 200 chars
                
                try:
                    self.cursor.execute(query)
                    registros_cargados += len(chunk)
                    print(f"✅ Paquete {i} cargado exitosamente")
                    
                except Exception as e:
                    print(f"❌ Error en paquete {i}: {e}")
                    # Continuar con el siguiente paquete
                    continue
            
            print(f"🎉 Carga completada: {registros_cargados}/{n} registros cargados")
            return registros_cargados
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return 0
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de la tabla"""
        try:
            # Total de registros
            self.cursor.execute("SELECT COUNT(*) FROM yolo_objects")
            total = self.cursor.fetchone()[0]
            print(f"📊 Total registros en Hive: {total}")
            
            # Top 5 clases
            self.cursor.execute("""
                SELECT clase, COUNT(*) as cantidad 
                FROM yolo_objects 
                GROUP BY clase 
                ORDER BY cantidad DESC 
                LIMIT 5
            """)
            
            top_clases = self.cursor.fetchall()
            print("🏆 Top 5 clases detectadas:")
            for clase, cantidad in top_clases:
                print(f"   {clase}: {cantidad}")
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
    
    def cerrar_conexion(self):
        """Cierra la conexión a Hive"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("🔒 Conexión a Hive cerrada")
        except:
            pass

if __name__ == "__main__":
    etl = SistemaBatchETL()
    
    # Conectar a Hive
    if etl.conectar_hive():
        # Crear tabla
        etl.crear_tabla()
        
        # Cargar datos
        archivo_csv = 'detecciones_completas.csv'
        etl.cargar_csv_a_hive(archivo_csv)
        
        # Mostrar estadísticas
        etl.mostrar_estadisticas()
        
        # Cerrar conexión
        etl.cerrar_conexion()
    else:
        print("❌ No se pudo conectar a Hive")
