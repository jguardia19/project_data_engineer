import os  

# 👇 DESACTIVAR GPU / CUDA PARA TENSORFLOW ANTES DE IMPORTARLO
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # TensorFlow no verá ninguna GPU
os.environ["TF_XLA_FLAGS"] = "--tf_xla_enable_xla_devices=false"  # Desactiva XLA en GPU
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # (Opcional) menos ruido de logs de TF

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from ultralytics import YOLO
from datetime import datetime
import csv

# Refuerzo: decirle explícitamente a TF que no use GPU
try:
    tf.config.set_visible_devices([], 'GPU')
except Exception as e:
    print("Aviso al desactivar GPUs en TF:", e)

print("GPUs visibles para TF:", tf.config.list_physical_devices('GPU'))  # Debería imprimir []


class DeteccionInfracciones:
    def __init__(self, modelo_yolo_path, carpeta_infracciones, archivo_csv, fuente=0, ancho_deseado=640, alto_deseado=480, id_camara=1, zona="Zona 1"):
        # Inicializar captura de video (para modo cámara en vivo)
        self.cap = cv2.VideoCapture(fuente)

        # Cargar el modelo YOLO
        self.modelo_yolo = YOLO(modelo_yolo_path)

        # Cargar el modelo MoveNet para detección de poses
        self.modelo_movenet = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1').signatures['serving_default']

        # Cargar el clasificador de rostros
        self.clasificador_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Configuración del sustractor de fondo
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # Dimensiones deseadas para el video redimensionado
        self.ancho_deseado = ancho_deseado
        self.alto_deseado = alto_deseado

        # Índices de las clases de interés
        self.clases_interes = {
            0: 'persona',
            41: 'objetomano',
            63: 'laptop',
            67: 'celular'
        }

        # Colores para cada clase
        self.colores = {
            'persona': (0, 255, 0),      # Verde
            'objetomano': (0, 128, 255), # Naranja
            'celular': (255, 0, 0),      # Azul
            'laptop': (0, 0, 255)        # Rojo
        }

        # Puntos del área de interés (ROI)
        self.area_pts = np.array([[230, 70], [380, 70], [1060, self.alto_deseado], [-280, self.alto_deseado]])

        # Carpeta donde guardar las infracciones
        self.carpeta_infracciones = carpeta_infracciones
        if not os.path.exists(self.carpeta_infracciones):
            os.makedirs(self.carpeta_infracciones)

        # Archivo CSV para guardar las infracciones
        self.archivo_csv = archivo_csv
        if not os.path.exists(self.archivo_csv):
            self.crear_csv()

        # Variables para el seguimiento y rastreo de infracciones
        self.infracciones_guardadas = {}  # Diccionario para llevar el registro de infracciones por tipo

        # Identificación de cámara y zona de infracción
        self.id_camara = id_camara
        self.zona = zona

        # Bordes para conexiones de puntos clave (keypoints) en pose estimation
        self.EDGES = {
            (0, 1): 'm', (0, 2): 'c', (1, 3): 'm', (2, 4): 'c', (0, 5): 'm',
            (0, 6): 'c', (5, 7): 'm', (7, 9): 'm', (6, 8): 'c', (8, 10): 'c',
            (5, 6): 'y', (5, 11): 'm', (6, 12): 'c', (11, 12): 'y', (11, 13): 'm',
            (13, 15): 'm', (12, 14): 'c', (14, 16): 'c'
        }

    def crear_csv(self):
        with open(self.archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dispositivo", "tipoinfraccion", "imagen", "ubicacion", "zonainteres", "fechahora"])

    def guardar_infraccion_csv(self, etiqueta, ruta_archivo):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.archivo_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["NVIDIATSS01", etiqueta, ruta_archivo, "Escaleras Universidad Piso 1 Ed Sistemas", self.zona, timestamp])

    def procesar_frame(self):
        ret, frame = self.cap.read()
        if not ret: 
            return None

        frame_redimensionado = cv2.resize(frame, (self.ancho_deseado, self.alto_deseado))
        return frame_redimensionado

    def aplicar_zona_interes(self, frame_redimensionado):
        imAux = np.zeros(shape=(self.alto_deseado, self.ancho_deseado), dtype=np.uint8)
        imAux = cv2.drawContours(imAux, [self.area_pts], -1, (255), -1)
        zona_interes = cv2.bitwise_and(frame_redimensionado, frame_redimensionado, mask=imAux)

        fgmask = self.fgbg.apply(zona_interes)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        fgmask = cv2.dilate(fgmask, None, iterations=2)

        return zona_interes

    def detectar_infraccion(self, frame_redimensionado, zona_interes):
        resultados = self.modelo_yolo(zona_interes)
        for resultado in resultados:
            detecciones_filtradas = [det for det in resultado.boxes if int(det.cls) in self.clases_interes]
            for deteccion in detecciones_filtradas:
                coordenadas = deteccion.xyxy[0].tolist()
                x1, y1, x2, y2 = map(int, coordenadas)
                clase = int(deteccion.cls)
                etiqueta = self.clases_interes.get(clase, 'desconocido')
                color = self.colores.get(etiqueta, (255, 255, 255))

                # Centro del bounding box
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # Verificar si la detección está dentro de la zona de interés
                if cv2.pointPolygonTest(self.area_pts, (cx, cy), False) >= 0:
                    cv2.rectangle(frame_redimensionado, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame_redimensionado, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                    # Guardar infracción solo si no ha sido registrada previamente por tipo
                    if etiqueta in ['celular', 'laptop', 'objetomano'] and (etiqueta not in self.infracciones_guardadas):
                        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                        nombre_archivo = f"{etiqueta}_infraccion_{timestamp}.jpg"
                        ruta_archivo = os.path.join(self.carpeta_infracciones, nombre_archivo)
                        cv2.imwrite(ruta_archivo, frame_redimensionado)

                        # Guardar infracción en CSV
                        self.guardar_infraccion_csv(etiqueta, ruta_archivo)

                        # Marcar la infracción como guardada
                        self.infracciones_guardadas[etiqueta] = timestamp

        cv2.drawContours(frame_redimensionado, [self.area_pts], -1, (255, 0, 255), 1)
        return frame_redimensionado

    def detectar_rostros(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = self.clasificador_rostros.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in rostros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

    def detectar_pose(self, frame):
        img = tf.image.resize_with_pad(tf.expand_dims(frame, axis=0), 256, 256)
        img = tf.cast(img, dtype=tf.int32)
        resultados = self.modelo_movenet(img)
        puntos = resultados['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))

        for persona in puntos:
            self.dibujar_pose(frame, persona)

    def dibujar_pose(self, frame, puntos):
        for (i, j), color in self.EDGES.items():
            if puntos[i][2] > 0.5 and puntos[j][2] > 0.5:
                # 'color' aquí es 'm', 'c', 'y', así que usamos blanco como default
                color_rgb = self.colores.get(color, (255, 255, 255))
                cv2.line(frame,
                        (int(puntos[i][1]), int(puntos[i][0])),
                        (int(puntos[j][1]), int(puntos[j][0])),
                        color_rgb, 2)

        for punto in puntos:
            if punto[2] > 0.5:
                cv2.circle(frame, (int(punto[1]), int(punto[0])), 5, (0, 255, 255), -1)

    def iniciar_desde_carpeta(self, carpeta_fuente):
        """Procesa todos los videos e imágenes de una carpeta."""
        extensiones_video = ('.mp4', '.avi', '.mov', '.mkv')
        extensiones_imagen = ('.jpg', '.jpeg', '.png', '.bmp')

        archivos = sorted(os.listdir(carpeta_fuente))

        for archivo in archivos:
            ruta = os.path.join(carpeta_fuente, archivo)
            if os.path.isdir(ruta):
                continue

            archivo_lower = archivo.lower()

            # ---- Procesar videos ----
            if archivo_lower.endswith(extensiones_video):
                cap = cv2.VideoCapture(ruta)
                print(f"Procesando video: {archivo}")

                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps <= 0 or fps is None:
                    fps = 30
                
                frames_por_batch = int(fps * 10)
                frame_count = 0

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        if frame_count % frames_por_batch != 0:
                            print("Ejecutando ETL al final del video (último batch incompleto)...")
                            #process_csv_and_insert_into_hive(False)  # debug=False
                            # Opcional: limpiar infracciones guardadas por batch
                            self.infracciones_guardadas = {}
                        break


                    frame = cv2.resize(frame, (self.ancho_deseado, self.alto_deseado))

                    zona_interes = self.aplicar_zona_interes(frame)
                    self.detectar_infraccion(frame, zona_interes)
                    self.detectar_rostros(frame)
                    self.detectar_pose(frame)

                    cv2.imshow(f'Video: {archivo}', frame)

                    frame_count += 1

                    if frame_count % frames_por_batch == 0:
                        print("Ejecutando ETL...")
                        #process_csv_and_insert_into_hive(False)  # debug=False
                        # Opcional: limpiar infracciones guardadas por batch
                        self.infracciones_guardadas = {}

                    # ESC para salir de TODO el procesamiento
                    if cv2.waitKey(1) & 0xFF == 27:
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                cap.release()
                cv2.destroyAllWindows()

            # ---- Procesar imágenes ----
            elif archivo_lower.endswith(extensiones_imagen):
                print(f"Procesando imagen: {archivo}")
                img = cv2.imread(ruta)
                if img is None:
                    continue

                img = cv2.resize(img, (self.ancho_deseado, self.alto_deseado))

                zona_interes = self.aplicar_zona_interes(img)
                self.detectar_infraccion(img, zona_interes)
                self.detectar_rostros(img)
                self.detectar_pose(img)

                cv2.imshow(f'Imagen: {archivo}', img)

                # Espera una tecla: ESC termina todo, otra tecla pasa a la siguiente imagen
                key = cv2.waitKey(0) & 0xFF
                if key == 27:
                    cv2.destroyAllWindows()
                    return

        cv2.destroyAllWindows()


# Uso de la clase DeteccionInfracciones
if __name__ == "__main__":
    deteccion = DeteccionInfracciones(
        modelo_yolo_path='yolov8n.pt',
        carpeta_infracciones='imageneseventos',
        archivo_csv='eventosdetectadosnvidia.csv',
        fuente=0,          # Se usa solo si llamas a iniciar() para cámara
        ancho_deseado=640,
        alto_deseado=480,
        id_camara=1,
        zona="RIESGO MEDIO"
    )

    # MODO 2: leer imágenes y videos de una carpeta
    deteccion.iniciar_desde_carpeta('imagenes_entrada')
