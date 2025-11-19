import pandas as pd
import os

if os.path.exists('detecciones_prueba.csv'):
    df = pd.read_csv('detecciones_prueba.csv')
    
    print(f"📊 RESULTADOS: {len(df)} detecciones encontradas")
    print("\n🎯 Resumen por clase:")
    print(df['class_name'].value_counts())
    
    print("\n🎨 Colores dominantes:")
    print(df['dominant_color_name'].value_counts())
    
    print("\n📋 Todas las detecciones:")
    print(df[['source_id', 'class_name', 'confidence', 'dominant_color_name']].to_string())
else:
    print("❌ No se encontró detecciones_prueba.csv")
