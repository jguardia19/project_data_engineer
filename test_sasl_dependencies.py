#!/usr/bin/env python3
"""
Test completo de dependencias SASL para PyHive
"""

def test_imports():
    """Probar todas las importaciones necesarias"""
    print("🔍 Probando importaciones...")
    
    try:
        import thrift
        print(f"✅ thrift: {thrift.__version__}")
    except ImportError as e:
        print(f"❌ thrift: {e}")
        return False
    
    try:
        import sasl
        print(f"✅ sasl: OK")
    except ImportError:
        try:
            import puresasl
            print(f"✅ pure-sasl: OK (fallback)")
        except ImportError as e:
            print(f"❌ SASL: {e}")
            return False
    
    try:
        from pyhive import hive
        print(f"✅ pyhive: OK")
    except ImportError as e:
        print(f"❌ pyhive: {e}")
        return False
    
    return True

def test_hive_connection():
    """Probar conexión a Hive"""
    print("\n🔗 Probando conexión a Hive...")
    
    try:
        from pyhive import hive
        
        conn = hive.Connection(
            host='localhost',
            port=10000,
            database='default',
            username='jose_dev',
            auth='NOSASL'
        )
        
        cursor = conn.cursor()
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()
        
        print(f"✅ Conexión exitosa")
        print(f"📊 Bases de datos: {databases}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TEST DE DEPENDENCIAS SASL")
    print("=" * 40)
    
    if test_imports():
        print("\n✅ Todas las importaciones OK")
        if test_hive_connection():
            print("\n🎉 SISTEMA LISTO PARA USAR")
        else:
            print("\n❌ Problema de conexión a Hive")
    else:
        print("\n❌ Faltan dependencias")