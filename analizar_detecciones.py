import pandas as pd
import os

def analizar_detecciones():
    print("🔍 ANALIZANDO DETECCIONES ENCONTRADAS")
    print("=" * 50)
    
    if not os.path.exists('detecciones_prueba.csv'):
        print("❌ No se encontró detecciones_prueba.csv")
        return
    
    df = pd.read_csv('detecciones_prueba.csv')
    
    print(f"📊 TOTAL DETECCIONES: {len(df)}")
    print(f"📸 IMÁGENES PROCESADAS: {df['source_id'].nunique()}")
    
    print("\n🎯 OBJETOS DETECTADOS:")
    clases = df['class_name'].value_counts()
    for clase, cantidad in clases.items():
        print(f"  • {clase}: {cantidad} detecciones")
    
    print("\n🎨 COLORES DOMINANTES:")
    colores = df['dominant_color_name'].value_counts()
    for color, cantidad in colores.items():
        print(f"  • {color}: {cantidad} objetos")
    
    print("\n📋 DETALLE POR IMAGEN:")
    for imagen in df['source_id'].unique():
        img_data = df[df['source_id'] == imagen]
        print(f"\n📸 {imagen}:")
        for _, row in img_data.iterrows():
            conf_pct = row['confidence'] * 100
            print(f"  ✅ {row['class_name']} ({conf_pct:.1f}% confianza) - Color: {row['dominant_color_name']}")
    
    print("\n🔥 DETECCIONES DE ALTA CONFIANZA (>70%):")
    alta_conf = df[df['confidence'] > 0.7]
    if not alta_conf.empty:
        for _, row in alta_conf.iterrows():
            conf_pct = row['confidence'] * 100
            print(f"  🎯 {row['source_id']}: {row['class_name']} ({conf_pct:.1f}%)")
    else:
        print("  ⚠️ No hay detecciones con alta confianza")
    
    # Mostrar algunas detecciones específicas
    print(f"\n📄 PRIMERAS 5 DETECCIONES COMPLETAS:")
    print(df[['source_id', 'class_name', 'confidence', 'dominant_color_name', 'detection_id']].head().to_string())

if __name__ == "__main__":
    analizar_detecciones()