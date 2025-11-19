from pyhive import hive
import traceback

def test_local_connection():
    print("🔍 Probando conexión local en WSL...")
    
    try:
        print("📡 Conectando a localhost:10000...")
        conn = hive.Connection(
            host='localhost',
            port=10000,
            database='default',
            username='jose_dev',
            auth='NOSASL'
        )
        
        print("✅ Conectado a HiveServer2 localmente")
        
        cursor = conn.cursor()
        
        # Test 1: Mostrar bases de datos
        print("📊 Ejecutando: SHOW DATABASES")
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()
        print(f"� Bases de datos encontradas: {databases}")
        
        # Test 2: Usar base de datos default
        print("🔄 Cambiando a base de datos 'default'")
        cursor.execute('USE default')
        
        # Test 3: Mostrar tablas
        print("📋 Ejecutando: SHOW TABLES")
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        print(f"📄 Tablas en default: {tables}")
        
        # Test 4: Crear base de datos de prueba
        print("🏗️ Creando base de datos yolo_project...")
        cursor.execute('CREATE DATABASE IF NOT EXISTS yolo_project')
        cursor.execute('USE yolo_project')
        print("✅ Base de datos yolo_project lista")
        
        conn.close()
        print("🎉 ¡CONEXIÓN LOCAL WSL COMPLETAMENTE EXITOSA!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("🔍 Detalles del error:")
        traceback.print_exc()
        
        # Diagnósticos adicionales
        print("\n🔧 DIAGNÓSTICOS:")
        print("1. ¿Está HiveServer2 corriendo?")
        print("   Ejecutar: sudo netstat -tlnp | grep 10000")
        print("2. ¿Hadoop está activo?")
        print("   Ejecutar: jps")
        
        return False

if __name__ == "__main__":
    test_local_connection()
