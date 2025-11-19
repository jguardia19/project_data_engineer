import pandas as pd
import cv2
import os
import csv
from datetime import datetime
from ultralytics import YOLO
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
                if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        
        print(f"🎥 Procesando {len(videos)} videos...")
        
        for vid_file in videos:
            vid_path = os.path.join(carpeta, vid_file)
            self._procesar_video(vid_path, vid_file)
            
        return len(videos)
    
    def _procesar_imagen(self, ruta_imagen, nombre_archivo):
        """Procesa una imagen individual"""
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            return
            
        results = self.model(imagen)
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:  # Solo detecciones con alta confianza
                        cls_id = int(box.cls[0])
                        cls_name = self.model.names[cls_id]
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        deteccion = {
                            'imagen': nombre_archivo,
                            'clase': cls_name,
                            'confianza': conf,
                            'x': int(x1),
                            'y': int(y1),
                            'ancho': int(x2 - x1),
                            'alto': int(y2 - y1),
                            'timestamp_proc': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.detecciones.append(deteccion)
    
    def _procesar_video(self, ruta_video, nombre_archivo):
        """Procesa un video frame por frame"""
        cap = cv2.VideoCapture(ruta_video)
        if not cap.isOpened():
            return
            
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Procesar cada 30 frames para optimizar
            if frame_count % 30 == 0:
                results = self.model(frame)
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            conf = float(box.conf[0])
                            if conf > 0.5:
                                cls_id = int(box.cls[0])
                                cls_name = self.model.names[cls_id]
                                x1, y1, x2, y2 = box.xyxy[0].tolist()
                                
                                deteccion = {
                                    'imagen': f"{nombre_archivo}_frame_{frame_count}",
                                    'clase': cls_name,
                                    'confianza': conf,
                                    'x': int(x1),
                                    'y': int(y1),
                                    'ancho': int(x2 - x1),
                                    'alto': int(y2 - y1),
                                    'timestamp_proc': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                                
                                self.detecciones.append(deteccion)
        
        cap.release()
    
    def guardar_csv(self, archivo='detecciones_yolo.csv'):
        """Guarda todas las detecciones en CSV"""
        if not self.detecciones:
            print("❌ No hay detecciones para guardar")
            return False
            
        df = pd.DataFrame(self.detecciones)
        df.to_csv(archivo, index=False)
        print(f"💾 Guardadas {len(self.detecciones)} detecciones en {archivo}")
        return True

if __name__ == "__main__":
    sistema = SistemaClasificacion()
    sistema.procesar_imagenes()
    sistema.procesar_videos()
    sistema.guardar_csv()
