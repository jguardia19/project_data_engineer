#!/usr/bin/env python3
"""
Sistema de Clasificación YOLO con Batches de 10 segundos para videos
"""
import cv2
import pandas as pd
from ultralytics import YOLO
import os
from datetime import datetime
import uuid
import colorsys
import numpy as np
from sistema_batch_etl import SistemaBatchETL

class SistemaClasificacionBatches:
    def __init__(self):
        print("🤖 Inicializando YOLO con sistema de batches...")
        self.model = YOLO('yolov8n.pt')
        self.detecciones = []
        self.etl = SistemaBatchETL()
        
        # Configuración de batches para videos
        self.BATCH_DURACION_SEGUNDOS = 10
        self.batch_actual = []
        self.tiempo_inicio_batch = 0
        
        print("✅ Sistema listo con batches de 10 segundos")
    
    def _procesar_video_con_batches(self, video_path, video_file):
        """Procesa video enviando batches cada 10 segundos"""
        print(f"🎬 Procesando video con batches: {video_file}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_count = 0
        
        # Inicializar primer batch
        self.batch_actual = []
        self.tiempo_inicio_batch = 0
        batch_numero = 1
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Procesar cada 30 frames (aprox 1 segundo)
            if frame_count % 30 == 0:
                timestamp_sec = frame_count / fps
                
                # Verificar si necesitamos enviar batch (cada 10 segundos)
                if timestamp_sec >= (batch_numero * self.BATCH_DURACION_SEGUNDOS):
                    if self.batch_actual:
                        self._enviar_batch_a_hive(video_file, batch_numero - 1)
                    
                    # Iniciar nuevo batch
                    self.batch_actual = []
                    batch_numero += 1
                
                # Procesar frame
                results = self.model(frame)
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            deteccion = self._extraer_atributos(
                                box, frame, video_file, 'video', 
                                frame_count, timestamp_sec
                            )
                            # Agregar al batch actual
                            self.batch_actual.append(deteccion)
            
            frame_count += 1
        
        # Enviar último batch si tiene datos
        if self.batch_actual:
            self._enviar_batch_a_hive(video_file, batch_numero - 1)
        
        cap.release()
        print(f"✅ Video procesado: {video_file} - {batch_numero} batches enviados")
    
    def _enviar_batch_a_hive(self, video_file, batch_numero):
        """Envía un batch de 10 segundos a Hive"""
        if not self.batch_actual:
            return
        
        tiempo_inicio = (batch_numero - 1) * self.BATCH_DURACION_SEGUNDOS
        tiempo_fin = batch_numero * self.BATCH_DURACION_SEGUNDOS
        
        print(f"📤 Enviando batch {batch_numero} de {video_file}")
        print(f"   ⏱️  Ventana: {tiempo_inicio}s - {tiempo_fin}s")
        print(f"   📊 Detecciones: {len(self.batch_actual)}")
        
        # Crear DataFrame del batch
        df_batch = pd.DataFrame(self.batch_actual)
        
        # Guardar CSV temporal del batch
        csv_batch = f"batch_{video_file}_{batch_numero:03d}.csv"
        df_batch.to_csv(csv_batch, index=False)
        
        # Conectar y enviar a Hive
        if self.etl.conectar_hive():
            if self.etl.crear_base_datos_y_tabla():
                registros = self.etl.cargar_csv_a_hive(csv_batch)
                print(f"   ✅ {registros} registros enviados a Hive")
            self.etl.cerrar_conexion()
        
        # Limpiar archivo temporal
        if os.path.exists(csv_batch):
            os.remove(csv_batch)
        
        print(f"   🎯 Batch {batch_numero} completado")
    
    def _extraer_atributos(self, box, frame, source_id, source_type, frame_number=0, timestamp_sec=0.0):
        """Extraer atributos de una detección"""
        # Obtener coordenadas y confianza
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        cls_name = self.model.names[cls_id]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Calcular dimensiones
        width = int(x2 - x1)
        height = int(y2 - y1)
        area_pixels = width * height
        
        # Dimensiones del frame
        frame_height, frame_width = frame.shape[:2]
        bbox_area_ratio = area_pixels / (frame_width * frame_height)
        
        # Centro del bounding box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        center_x_norm = center_x / frame_width
        center_y_norm = center_y / frame_height
        
        # Región de posición
        if center_x_norm < 0.33:
            pos_x = "left"
        elif center_x_norm < 0.66:
            pos_x = "center"
        else:
            pos_x = "right"
        
        if center_y_norm < 0.33:
            pos_y = "top"
        elif center_y_norm < 0.66:
            pos_y = "middle"
        else:
            pos_y = "bottom"
        
        position_region = f"{pos_y}_{pos_x}"
        
        # Color dominante del bounding box
        roi = frame[int(y1):int(y2), int(x1):int(x2)]
        if roi.size > 0:
            avg_color = np.mean(roi, axis=(0, 1))
            dom_b, dom_g, dom_r = avg_color.astype(int)
            
            # Convertir a nombre de color aproximado
            dominant_color_name = self._get_color_name(dom_r, dom_g, dom_b)
        else:
            dom_r = dom_g = dom_b = 128
            dominant_color_name = "gray"
        
        return {
            'source_type': source_type,
            'source_id': source_id,
            'frame_number': frame_number,
            'class_id': cls_id,
            'class_name': cls_name,
            'confidence': round(conf, 4),
            'x_min': int(x1),
            'y_min': int(y1),
            'x_max': int(x2),
            'y_max': int(y2),
            'width': width,
            'height': height,
            'area_pixels': area_pixels,
            'frame_width': frame_width,
            'frame_height': frame_height,
            'bbox_area_ratio': round(bbox_area_ratio, 6),
            'center_x': round(center_x, 2),
            'center_y': round(center_y, 2),
            'center_x_norm': round(center_x_norm, 4),
            'center_y_norm': round(center_y_norm, 4),
            'position_region': position_region,
            'dominant_color_name': dominant_color_name,
            'dom_r': dom_r,
            'dom_g': dom_g,
            'dom_b': dom_b,
            'timestamp_sec': round(timestamp_sec, 2),
            'ingestion_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'detection_id': str(uuid.uuid4())[:8]
        }
    
    def _get_color_name(self, r, g, b):
        """Obtener nombre aproximado del color"""
        colors = {
            'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
            'yellow': (255, 255, 0), 'cyan': (0, 255, 255), 'magenta': (255, 0, 255),
            'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (128, 128, 128),
            'orange': (255, 165, 0), 'purple': (128, 0, 128), 'brown': (165, 42, 42)
        }
        
        min_dist = float('inf')
        closest_color = 'gray'
        
        for name, (cr, cg, cb) in colors.items():
            dist = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_color = name
        
        return closest_color
    
    def procesar_videos(self, carpeta_videos='videos_entrada'):
        """Procesar todos los videos con sistema de batches"""
        if not os.path.exists(carpeta_videos):
            print(f"❌ Carpeta {carpeta_videos} no existe")
            return 0
        
        videos_procesados = 0
        extensiones = ('.mp4', '.avi', '.mov', '.mkv')
        
        for archivo in os.listdir(carpeta_videos):
            if archivo.lower().endswith(extensiones):
                video_path = os.path.join(carpeta_videos, archivo)
                print(f"\n🎬 Procesando: {archivo}")
                
                self._procesar_video_con_batches(video_path, archivo)
                videos_procesados += 1
        
        print(f"\n✅ Videos procesados con batches: {videos_procesados}")
        return videos_procesados

    def procesar_imagenes(self, carpeta_imagenes='imagenes_entrada'):
        """Procesar imágenes (envío inmediato a Hive)"""
        if not os.path.exists(carpeta_imagenes):
            print(f"❌ Carpeta {carpeta_imagenes} no existe")
            return 0
        
        imagenes_procesadas = 0
        extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
        detecciones_imagenes = []
        
        for archivo in os.listdir(carpeta_imagenes):
            if archivo.lower().endswith(extensiones):
                imagen_path = os.path.join(carpeta_imagenes, archivo)
                print(f"🖼️  Procesando: {archivo}")
                
                # Cargar y procesar imagen
                frame = cv2.imread(imagen_path)
                if frame is None:
                    print(f"❌ No se pudo cargar: {archivo}")
                    continue
                
                # Detectar objetos
                results = self.model(frame)
                detecciones_imagen = 0
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            deteccion = self._extraer_atributos(
                                box, frame, archivo, 'image', 0, 0.0
                            )
                            detecciones_imagenes.append(deteccion)
                            detecciones_imagen += 1
                
                print(f"   ✅ {detecciones_imagen} objetos detectados")
                imagenes_procesadas += 1
        
        # Enviar todas las imágenes a Hive de una vez
        if detecciones_imagenes:
            print(f"\n📤 Enviando {len(detecciones_imagenes)} detecciones de imágenes a Hive...")
            
            # Crear DataFrame
            df_imagenes = pd.DataFrame(detecciones_imagenes)
            
            # Guardar CSV temporal
            csv_imagenes = "detecciones_imagenes_temp.csv"
            df_imagenes.to_csv(csv_imagenes, index=False)
            
            # Enviar a Hive
            if self.etl.conectar_hive():
                if self.etl.crear_base_datos_y_tabla():
                    registros = self.etl.cargar_csv_a_hive(csv_imagenes)
                    print(f"   ✅ {registros} registros enviados a Hive")
                self.etl.cerrar_conexion()
            
            # Limpiar archivo temporal
            if os.path.exists(csv_imagenes):
                os.remove(csv_imagenes)
        
        print(f"✅ Imágenes procesadas: {imagenes_procesadas}")
        return imagenes_procesadas

if __name__ == "__main__":
    print("🎬 SISTEMA DE CLASIFICACIÓN CON BATCHES DE 10 SEGUNDOS")
    print("=" * 60)
    
    sistema = SistemaClasificacionBatches()
    
    # Procesar videos con batches automáticos
    videos = sistema.procesar_videos('videos_entrada')
    
    if videos > 0:
        print(f"\n🎉 ¡Procesamiento completado!")
        print(f"📊 {videos} videos procesados con batches de 10 segundos")
    else:
        print("❌ No se encontraron videos para procesar")
