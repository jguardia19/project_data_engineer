#!/usr/bin/env python3
"""
Sistema de Clasificación - YOLO para Imágenes y Videos
Genera CSV local (staging layer)
"""
import os
import cv2
import pandas as pd
from ultralytics import YOLO
import uuid
from datetime import datetime
import numpy as np

class SistemaClasificacion:
    """Sistema unificado para clasificar imágenes y videos con YOLO"""
    
    def __init__(self):
        """Inicializar el modelo YOLO"""
        self.model = YOLO('yolov8n.pt')
        self.detecciones = []
        
    def procesar_imagenes(self, carpeta='imagenes_entrada'):
        """Procesa todas las imágenes en la carpeta"""
        if not os.path.exists(carpeta):
            print(f"❌ Carpeta {carpeta} no existe")
            return 0
            
        imagenes = [f for f in os.listdir(carpeta) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"📸 Procesando {len(imagenes)} imágenes...")
        
        for img_file in imagenes:
            img_path = os.path.join(carpeta, img_file)
            self._procesar_imagen(img_path, img_file)
            
        return len(imagenes)
    
    def procesar_videos(self, carpeta='videos_entrada'):
        """Procesa todos los videos en la carpeta"""
        if not os.path.exists(carpeta):
            print(f"❌ Carpeta {carpeta} no existe")
            return 0
            
        videos = [f for f in os.listdir(carpeta) 
                if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        
        print(f"🎥 Procesando {len(videos)} videos...")
        
        for video_file in videos:
            video_path = os.path.join(carpeta, video_file)
            self._procesar_video(video_path, video_file)
            
        return len(videos)
    
    def _procesar_imagen(self, img_path, img_file):
        """Procesa una imagen individual"""
        img = cv2.imread(img_path)
        if img is None:
            return
            
        results = self.model(img)
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    deteccion = self._extraer_atributos(
                        box, img, img_file, 'image', 0, 0
                    )
                    self.detecciones.append(deteccion)
    
    def _procesar_video(self, video_path, video_file):
        """Procesa un video extrayendo frames"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Procesar cada 30 frames (aprox 1 segundo)
            if frame_count % 30 == 0:
                timestamp_sec = frame_count / fps
                results = self.model(frame)
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            deteccion = self._extraer_atributos(
                                box, frame, video_file, 'video', 
                                frame_count, timestamp_sec
                            )
                            self.detecciones.append(deteccion)
            
            frame_count += 1
            
        cap.release()
    
    def _extraer_atributos(self, box, frame, source_id, source_type, 
                          frame_number, timestamp_sec):
        """Extrae todos los atributos requeridos según ProyectoEnEspanol.md"""
        
        # A. Información Básica y de Modelo
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        class_name = self.model.names[cls]
        
        # B. Información del Bounding Box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        width = x2 - x1
        height = y2 - y1
        area_pixels = width * height
        
        frame_height, frame_width = frame.shape[:2]
        bbox_area_ratio = area_pixels / (frame_width * frame_height)
        
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        center_x_norm = center_x / frame_width
        center_y_norm = center_y / frame_height
        
        # Región de posición
        position_region = self._calcular_region_posicion(
            center_x_norm, center_y_norm
        )
        
        # C. Color Dominante
        roi = frame[int(y1):int(y2), int(x1):int(x2)]
        color_info = self._obtener_color_dominante(roi)
        
        return {
            # A. Información Básica
            'source_type': source_type,
            'source_id': source_id,
            'frame_number': frame_number,
            'class_id': cls,
            'class_name': class_name,
            'confidence': conf,
            
            # B. Bounding Box
            'x_min': int(x1),
            'y_min': int(y1),
            'x_max': int(x2),
            'y_max': int(y2),
            'width': int(width),
            'height': int(height),
            'area_pixels': int(area_pixels),
            'frame_width': frame_width,
            'frame_height': frame_height,
            'bbox_area_ratio': bbox_area_ratio,
            'center_x': center_x,
            'center_y': center_y,
            'center_x_norm': center_x_norm,
            'center_y_norm': center_y_norm,
            'position_region': position_region,
            
            # C. Color Dominante
            'dominant_color_name': color_info['name'],
            'dom_r': color_info['r'],
            'dom_g': color_info['g'],
            'dom_b': color_info['b'],
            
            # D. Metadatos
            'timestamp_sec': timestamp_sec,
            'ingestion_date': datetime.now().isoformat(),
            'detection_id': str(uuid.uuid4())
        }
    
    def _calcular_region_posicion(self, center_x_norm, center_y_norm):
        """Calcula la región de posición del objeto"""
        if center_y_norm < 0.33:
            row = 'top'
        elif center_y_norm < 0.67:
            row = 'middle'
        else:
            row = 'bottom'
            
        if center_x_norm < 0.33:
            col = 'left'
        elif center_x_norm < 0.67:
            col = 'center'
        else:
            col = 'right'
            
        return f"{row}-{col}"
    
    def _obtener_color_dominante(self, roi):
        """Obtiene el color dominante de una región"""
        if roi.size == 0:
            return {'name': 'black', 'r': 0, 'g': 0, 'b': 0}
            
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        color_promedio = np.mean(roi_rgb.reshape(-1, 3), axis=0)
        r, g, b = color_promedio.astype(int)
        
        return {
            'name': self._clasificar_color(r, g, b),
            'r': r,
            'g': g,
            'b': b
        }
    
    def _clasificar_color(self, r, g, b):
        """Clasifica un color RGB en nombre"""
        if r > 200 and g > 200 and b > 200:
            return 'white'
        elif r < 50 and g < 50 and b < 50:
            return 'black'
        elif r > g and r > b:
            return 'red'
        elif g > r and g > b:
            return 'green'
        elif b > r and b > g:
            return 'blue'
        elif r > 150 and g > 150:
            return 'yellow'
        else:
            return 'other'
    
    def guardar_csv(self, archivo='detecciones_staging.csv'):
        """Guarda todas las detecciones en CSV (staging layer)"""
        if not self.detecciones:
            print("❌ No hay detecciones para guardar")
            return False
            
        df = pd.DataFrame(self.detecciones)
        df.to_csv(archivo, index=False)
        print(f"✅ Guardadas {len(self.detecciones)} detecciones en {archivo}")
        return True

def main():
    """Función principal del sistema de clasificación"""
    print("🤖 SISTEMA DE CLASIFICACIÓN - YOLO")
    print("=" * 50)
    
    clasificador = SistemaClasificacion()
    
    # Procesar imágenes
    num_imagenes = clasificador.procesar_imagenes()
    
    # Procesar videos
    num_videos = clasificador.procesar_videos()
    
    # Guardar resultados
    if clasificador.guardar_csv():
        print(f"\n📊 RESUMEN:")
        print(f"Imágenes procesadas: {num_imagenes}")
        print(f"Videos procesados: {num_videos}")
        print(f"Total detecciones: {len(clasificador.detecciones)}")
        
        # Mostrar estadísticas
        df = pd.DataFrame(clasificador.detecciones)
        print(f"Clases detectadas: {df['class_name'].nunique()}")
        print("Top 5 clases:", df['class_name'].value_counts().head().to_dict())

if __name__ == "__main__":
    main()