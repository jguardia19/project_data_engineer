# Proyecto Final - Ingeniero de Datos de IA

**Curso:** Procesos ETL para Cargas de Trabajo de IA
**Programa:** Certificación de Ingeniero de Datos de IA
**Estudiante:** José Gregorio Guardia
**Tecnologías:** YOLO v11, Apache Hive, Apache Hadoop, Python ETL

---

## 📋 Descripción General

Este proyecto integra **Deep Learning**, **Visión por Computador** y **Procesamiento Big Data** en una solución end-to-end compuesta por **dos sistemas claramente separados**:

1. **Sistema de Clasificación**: Ejecuta YOLO sobre imágenes y videos, extrae atributos enriquecidos y escribe detecciones en archivos CSV locales (capa de staging).

2. **Sistema Batch/ETL**: Lee los CSV generados, realiza limpieza, transformación y carga los datos procesados a Apache Hive en lotes, garantizando que no exista información duplicada.

---

## 🏗️ Arquitectura de Dos Sistemas

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE CLASIFICACIÓN                      │
│  📸 Imágenes/Videos → 🤖 YOLO v11 → 📊 Extracción Atributos     │
│                           ↓                                      │
│                    📁 CSV Locales (Staging)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     SISTEMA BATCH/ETL                            │
│  📁 CSV → 🧹 Limpieza → 🔄 Transformación → 🗄️ Apache Hive     │
│  (Lotes de 10s para videos, batch completo para imágenes)       │
│  ✅ Sin duplicados garantizado                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                      📈 Consultas Analíticas
```

---

## 🚀 Características Principales

### Sistema de Clasificación
- ✅ Detección de objetos con **YOLO v11** (15+ objetos en imágenes, 10+ en videos)
- ✅ Extracción de **26+ atributos** por objeto detectado
- ✅ Cálculo de **color dominante** con OpenCV
- ✅ Análisis de **posición espacial** y región del frame
- ✅ Generación de **CSV locales** como capa de staging
- ✅ **NO se conecta a Hive** (separación de responsabilidades)

### Sistema Batch/ETL
- ✅ Procesamiento **solo con Python** (sin PySpark)
- ✅ **Limpieza y transformación** de datos
- ✅ Envío en **lotes de 10 segundos** para videos
- ✅ Envío **completo al finalizar** para imágenes
- ✅ **Garantía de no duplicados** en Hive
- ✅ Estrategia de **checkpoint** para sincronización

### Calidad de Código
- ✅ **Makefile** para automatización completa
- ✅ **Pruebas unitarias** con pytest
- ✅ **Linting** con pylint
- ✅ **Documentación** completa con docstrings
- ✅ **Logging** detallado del proceso

---

## 📁 Estructura del Proyecto

```
project_data_engineer/
├── 📸 imagenes_entrada/              # 20+ imágenes capturadas
├── 🎬 videos_entrada/                # 2+ videos (max 20s o 50MB)
├── 📊 imagenes_procesadas/           # CSVs generados (staging)
├── 🐍 src/                           # Código fuente
│   ├── sistema_clasificacion.py      # Sistema 1: YOLO → CSV
│   ├── sistema_batch_etl.py          # Sistema 2: CSV → Hive
│   └── test_clasificacion.py         # Pruebas del sistema 1
│   └── test_etl.py                   # Pruebas del sistema 2
├── 🧪 tests/                         # Pruebas unitarias adicionales
│   ├── test_clasificacion.py
│   ├── test_sistema.py
│   └── test_hive_local_wsl.py
├── 📋 sql/                           # Consultas analíticas (5+)
│   ├── 01_consultas_basicas.sql
│   ├── 02_analisis_confianza.sql
│   ├── 03_analisis_espacial.sql
│   ├── 04_analisis_colores.sql
│   ├── 05_analisis_temporal.sql
│   └── 06_reportes_avanzados.sql
├── 🔧 configuracion.py               # Configuraciones centralizadas
├── 🚀 ejecutar_proyecto.py           # Script principal de ejecución
├── 📄 Makefile                       # Automatización completa
├── 📄 requerimientos.txt             # Dependencias Python
├── 📖 README.md                      # Esta documentación
├── 📖 GUIA_PROYECTO_FINAL_ES.md      # Guía del proyecto
└── 🐳 enviroments/                   # Entorno virtual
```

---

## 🛠️ Requisitos del Sistema

### 1. Sistema Operativo y Software Base
- **Ubuntu 24.04** (requerido)
- **Python 3.10** (instalado según guía oficial)
- **Apache HDFS** (instalado y funcionando)
- **Apache Hive** (instalado y funcionando)
- **GPU NVIDIA** (opcional, para aceleración CUDA)

### 2. Instalación de Python 3.10 y OpenCV
Seguir la guía oficial:
```
guias/Guia_Instalacion_Python310_OpenCV_v410.pdf
```

### 3. Instalación de OpenCV con CUDA (Opcional)
Si tienes GPU NVIDIA, seguir:
```
StepByStepToInstallOpenCVWithCudaSupport.txt
```

---

## ⚙️ Configuración del Entorno

### 1. Crear Entorno Virtual
```bash
# Crear entorno virtual
python3.10 -m venv enviroments/project_final

# Activar entorno (Linux/Ubuntu)
source enviroments/project_final/bin/activate

# Activar entorno (Windows WSL)
source enviroments/project_final/bin/activate
```

### 2. Instalar Dependencias con Makefile
```bash
# Opción 1: Usar Makefile (recomendado)
make install

# Opción 2: Instalación manual
pip install --upgrade pip
pip install -r requerimientos.txt
```

### 3. Verificar Instalación
```bash
# Verificar todas las dependencias
make test

# Verificar YOLO
python -c "from ultralytics import YOLO; print('✅ YOLO OK')"

# Verificar Hive
python -c "from pyhive import hive; print('✅ Hive OK')"

# Verificar OpenCV
python -c "import cv2; print('✅ OpenCV OK')"
```

### 4. Configurar Apache Hive
```bash
# Verificar servicios Hadoop y Hive
jps | grep -E "(HiveServer2|RunJar|NameNode|DataNode)"

# Iniciar Hadoop (si no está corriendo)
start-dfs.sh
start-yarn.sh

# Iniciar Hive (si no está corriendo)
$HIVE_HOME/bin/hiveserver2 --hiveconf hive.server2.thrift.port=10000 &

# Verificar conexión
beeline -u jdbc:hive2://localhost:10000
```

### 5. Configuración del Proyecto
Editar `configuracion.py` con tus parámetros:
```python
HIVE_CONFIG = {
    'host': 'localhost',
    'port': 10000,
    'username': 'tu_usuario',
    'database': 'yolo_project',
    'auth': 'NONE'
}
```

---

## 🚀 Ejecución del Proyecto

### Opción 1: Ejecución Completa con Makefile (Recomendado)
```bash
# Ejecutar todo el pipeline (clasificación + ETL)
make run

# O ejecutar paso a paso
make run-clasificacion    # Solo Sistema de Clasificación
make run-etl             # Solo Sistema ETL
```

### Opción 2: Ejecución Manual de Sistemas Separados

#### Sistema 1: Clasificación (YOLO → CSV)
```bash
# Activar entorno
source enviroments/project_final/bin/activate

# Ejecutar sistema de clasificación
python src/sistema_clasificacion.py

# Resultado: CSV generados en imagenes_procesadas/
```

#### Sistema 2: Batch/ETL (CSV → Hive)
```bash
# Activar entorno
source enviroments/project_final/bin/activate

# Ejecutar sistema ETL
python src/sistema_batch_etl.py

# Resultado: Datos cargados en Hive sin duplicados
```

### Opción 3: Script Principal Integrado
```bash
# Ejecutar pipeline completo
python ejecutar_proyecto.py
```

---

## 📊 Datos de Entrada

### Imágenes
- **Cantidad mínima:** 20 imágenes diferentes
- **Ubicación:** `imagenes_entrada/`
- **Formato:** JPG, JPEG, PNG
- **Requisito:** Capturadas por el estudiante (no descargadas)
- **Contenido:** Deben contener objetos detectables (personas, vehículos, etc.)

### Videos
- **Cantidad mínima:** 2 videos
- **Ubicación:** `videos_entrada/`
- **Formato:** MP4, MOV, AVI
- **Duración máxima:** 20 segundos
- **Tamaño máximo:** 50 MB por video
- **Requisito:** Capturados por el estudiante (no descargados)
- **Contenido:** Deben contener personas

---

## 🤖 Sistema de Clasificación (Sistema 1)

### Responsabilidades
1. ✅ Cargar modelo YOLO v11
2. ✅ Procesar imágenes y videos
3. ✅ Detectar objetos (15+ en imágenes, 10+ en videos)
4. ✅ Extraer 26+ atributos por objeto
5. ✅ Escribir detecciones en CSV locales
6. ❌ **NO se conecta a Hive**

### Atributos Extraídos (26+ por objeto)

#### A. Información Básica
- `source_type` - "image" o "video"
- `source_id` - nombre del archivo
- `frame_number` - 0 para imágenes, número de frame en video
- `class_id` - ID numérico de la clase
- `class_name` - nombre de la clase detectada
- `confidence` - confianza de la detección (0-1)

#### B. Bounding Box
- `x_min`, `y_min`, `x_max`, `y_max` - coordenadas del bbox
- `width`, `height` - dimensiones del bbox
- `area_pixels` - área del bbox en píxeles
- `frame_width`, `frame_height` - dimensiones del frame
- `bbox_area_ratio` - proporción del bbox respecto al frame

#### C. Posición Espacial
- `center_x`, `center_y` - centro del bbox
- `center_x_norm`, `center_y_norm` - centro normalizado (0-1)
- `position_region` - región del frame (top-left, middle-center, etc.)

#### D. Color Dominante (OpenCV)
- `dominant_color_name` - nombre del color (red, green, blue, etc.)
- `dom_r`, `dom_g`, `dom_b` - componentes RGB del color dominante

#### E. Metadatos Temporales
- `timestamp_sec` - tiempo del frame en segundos (videos)
- `ingestion_date` - fecha/hora de procesamiento
- `detection_id` - identificador único de la detección

### Ejemplo de Ejecución
```bash
python src/sistema_clasificacion.py

# Salida esperada:
# ✅ Procesando imágenes...
# ✅ Procesando videos...
# ✅ CSV generados en: imagenes_procesadas/
# ✅ Total detecciones: 1234
```

---

## � Sistema Batch/ETL (Sistema 2)

### Responsabilidades
1. ✅ Leer CSV generados por Sistema 1
2. ✅ Limpieza de datos (nulos, valores inválidos)
3. ✅ Transformación y normalización
4. ✅ Carga a Hive en lotes
5. ✅ **Garantizar NO duplicados**

### Reglas de Envío de Lotes

#### Para Imágenes
- Se envían **al finalizar** el procesamiento de todas las imágenes
- Un solo lote con todas las detecciones de imágenes

#### Para Videos
- Se envían en **ventanas de 10 segundos** de contenido
- Ejemplo para video de 40 segundos:
  - Lote 1: frames 0-10s
  - Lote 2: frames 10-20s
  - Lote 3: frames 20-30s
  - Lote 4: frames 30-40s

### Estrategia Anti-Duplicados

El sistema implementa **múltiples mecanismos** para evitar duplicados:

1. **Clave única compuesta:**
   ```python
   detection_id = f"{source_id}_{frame_number}_{class_id}_{bbox_hash}"
   ```

2. **Checkpoint de procesamiento:**
   - Archivo `imagenes_procesadas/checkpoint.json`
   - Registra qué archivos ya fueron procesados
   - Evita re-procesar datos ya cargados

3. **Validación pre-inserción:**
   - Consulta a Hive antes de insertar
   - Filtra registros ya existentes

### Proceso ETL Completo

```python
# 1. EXTRACCIÓN
csv_files = leer_csv_staging()

# 2. LIMPIEZA
datos_limpios = limpiar_datos(csv_files)
# - Eliminar nulos
# - Validar rangos (confidence 0-1)
# - Validar coordenadas

# 3. TRANSFORMACIÓN
datos_transformados = transformar_datos(datos_limpios)
# - Normalizar tipos
# - Calcular campos derivados
# - Agrupar por lotes (10s para videos)

# 4. CARGA
cargar_a_hive(datos_transformados)
# - Verificar duplicados
# - Insertar en Hive
# - Actualizar checkpoint
```

### Ejemplo de Ejecución
```bash
python src/sistema_batch_etl.py

# Salida esperada:
# ✅ Conectando a Hive...
# ✅ Leyendo CSV de staging...
# ✅ Limpiando datos...
# ✅ Transformando datos...
# ✅ Cargando lote 1/4 (video: 0-10s)...
# ✅ Cargando lote 2/4 (video: 10-20s)...
# ✅ Cargando lote imágenes...
# ✅ Total registros cargados: 1234
# ✅ Duplicados evitados: 0
```

---

## 🗄️ Esquema de Hive

### Tabla Principal: yolo_objects

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS yolo_objects (
    -- Información Básica
    source_type           STRING,
    source_id             STRING,
    frame_number          INT,
    class_id              INT,
    class_name            STRING,
    confidence            DOUBLE,

    -- Bounding Box
    x_min                 INT,
    y_min                 INT,
    x_max                 INT,
    y_max                 INT,
    width                 INT,
    height                INT,
    area_pixels           INT,
    frame_width           INT,
    frame_height          INT,
    bbox_area_ratio       DOUBLE,

    -- Posición Espacial
    center_x              DOUBLE,
    center_y              DOUBLE,
    center_x_norm         DOUBLE,
    center_y_norm         DOUBLE,
    position_region       STRING,

    -- Color Dominante
    dominant_color_name   STRING,
    dom_r                 INT,
    dom_g                 INT,
    dom_b                 INT,

    -- Metadatos
    timestamp_sec         DOUBLE,
    ingestion_date        STRING,
    detection_id          STRING
)
STORED AS PARQUET
LOCATION 'hdfs:///projects/yolo_objects/hive/';
```

### Creación de Base de Datos
```sql
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS yolo_project;
USE yolo_project;

-- Verificar tabla
SHOW TABLES;
DESCRIBE FORMATTED yolo_objects;
```

---

## 📈 Consultas Analíticas en Hive

El proyecto incluye **5+ consultas analíticas** en la carpeta `sql/`:

### 1. Consultas Básicas (`01_consultas_basicas.sql`)
```sql
-- Conteo de objetos por clase
SELECT class_name, COUNT(*) as total_detecciones
FROM yolo_objects
GROUP BY class_name
ORDER BY total_detecciones DESC;

-- Número de personas por video
SELECT source_id, COUNT(*) as total_personas
FROM yolo_objects
WHERE class_name = 'person' AND source_type = 'video'
GROUP BY source_id;
```

### 2. Análisis de Confianza (`02_analisis_confianza.sql`)
```sql
-- Confianza promedio por clase
SELECT class_name,
       AVG(confidence) as avg_confidence,
       MIN(confidence) as min_confidence,
       MAX(confidence) as max_confidence
FROM yolo_objects
GROUP BY class_name;
```

### 3. Análisis Espacial (`03_analisis_espacial.sql`)
```sql
-- Área promedio de bounding boxes por clase
SELECT class_name,
       AVG(area_pixels) as avg_area,
       AVG(bbox_area_ratio) as avg_ratio
FROM yolo_objects
GROUP BY class_name;

-- Distribución por región del frame
SELECT position_region, COUNT(*) as total
FROM yolo_objects
GROUP BY position_region;
```

### 4. Análisis de Colores (`04_analisis_colores.sql`)
```sql
-- Distribución de colores dominantes por clase
SELECT class_name, dominant_color_name, COUNT(*) as total
FROM yolo_objects
GROUP BY class_name, dominant_color_name
ORDER BY class_name, total DESC;
```

### 5. Análisis Temporal (`05_analisis_temporal.sql`)
```sql
-- Número de objetos por ventana de 10 segundos en cada video
SELECT source_id,
       FLOOR(timestamp_sec / 10) * 10 as ventana_inicio,
       COUNT(*) as objetos_detectados
FROM yolo_objects
WHERE source_type = 'video'
GROUP BY source_id, FLOOR(timestamp_sec / 10)
ORDER BY source_id, ventana_inicio;
```

### Ejecutar Consultas
```bash
# Opción 1: Desde Hive CLI
beeline -u jdbc:hive2://localhost:10000 -f sql/01_consultas_basicas.sql

# Opción 2: Con script Python
python sql/ejecutar_queries.py

# Opción 3: Con Makefile
make queries
```

---

## 🧪 Pruebas y Calidad de Código

### Estructura de Pruebas
```
tests/
├── test_clasificacion.py      # Pruebas del Sistema 1
├── test_sistema.py            # Pruebas integradas
└── test_hive_local_wsl.py     # Pruebas de conexión Hive
```

### Ejecutar Pruebas
```bash
# Opción 1: Con Makefile (recomendado)
make test

# Opción 2: Con pytest directamente
pytest tests/ -v

# Opción 3: Pruebas específicas
pytest tests/test_clasificacion.py -v
pytest tests/test_sistema.py -v
```

### Linting y Formateo
```bash
# Ejecutar pylint
make lint

# Formatear código
make format

# Verificar todo (lint + test)
make check
```

### Cobertura de Pruebas
```bash
# Generar reporte de cobertura
make coverage

# Ver reporte HTML
make coverage-html
```

---

## 📋 Uso del Makefile

El proyecto incluye un **Makefile completo** para automatización:

```bash
# Ver todos los comandos disponibles
make help

# Comandos principales:
make install          # Instalar dependencias
make test            # Ejecutar pruebas
make lint            # Ejecutar pylint
make format          # Formatear código
make run             # Ejecutar pipeline completo
make run-clasificacion  # Solo clasificación
make run-etl         # Solo ETL
make queries         # Ejecutar consultas SQL
make clean           # Limpiar archivos temporales
make check           # Lint + Test
```

---

## 📊 Monitoreo y Logs

### Archivos de Log
El sistema genera logs detallados:
- `logs/clasificacion.log` - Logs del Sistema de Clasificación
- `logs/etl.log` - Logs del Sistema ETL
- `logs/pipeline.log` - Logs del pipeline completo

### Niveles de Log
```python
# Configuración en configuracion.py
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
```

### Ver Logs en Tiempo Real
```bash
# Seguir logs de clasificación
tail -f logs/clasificacion.log

# Seguir logs de ETL
tail -f logs/etl.log
```

---

## 🔧 Solución de Problemas

### Error: No se puede conectar a Hive
```bash
# 1. Verificar que Hive esté corriendo
jps | grep HiveServer2

# 2. Verificar que Hadoop esté corriendo
jps | grep -E "(NameNode|DataNode)"

# 3. Iniciar servicios si es necesario
start-dfs.sh
start-yarn.sh
$HIVE_HOME/bin/hiveserver2 --hiveconf hive.server2.thrift.port=10000 &

# 4. Probar conexión
beeline -u jdbc:hive2://localhost:10000
```

### Error: Módulo 'pyhive' no encontrado
```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requerimientos.txt

# Verificar instalación
python -c "from pyhive import hive; print('✅ Hive OK')"
```

### Error: YOLO no detecta objetos
```bash
# Verificar instalación de YOLO
python -c "from ultralytics import YOLO; print('✅ YOLO OK')"

# Verificar modelo descargado
ls -lh yolo11n.pt

# Re-descargar modelo si es necesario
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

### Error: OpenCV no encuentra CUDA
```bash
# Verificar instalación de OpenCV
python -c "import cv2; print(cv2.getBuildInformation())"

# Si no tiene CUDA, reinstalar siguiendo:
# StepByStepToInstallOpenCVWithCudaSupport.txt
```

### Error: Duplicados en Hive
```bash
# Limpiar tabla y checkpoint
beeline -u jdbc:hive2://localhost:10000 -e "TRUNCATE TABLE yolo_project.yolo_objects;"
rm imagenes_procesadas/checkpoint.json

# Re-ejecutar ETL
python src/sistema_batch_etl.py
```

---

## 📈 Resultados Esperados

### Al ejecutar el Sistema de Clasificación:
1. ✅ Procesamiento de 20+ imágenes
2. ✅ Procesamiento de 2+ videos
3. ✅ Detección de 15+ objetos en imágenes
4. ✅ Detección de 10+ objetos en videos
5. ✅ Generación de CSV con 26+ atributos por objeto
6. ✅ CSV guardados en `imagenes_procesadas/`

### Al ejecutar el Sistema ETL:
1. ✅ Lectura de CSV de staging
2. ✅ Limpieza de datos (nulos, valores inválidos)
3. ✅ Transformación y normalización
4. ✅ Carga en lotes de 10s para videos
5. ✅ Carga completa para imágenes
6. ✅ **0 duplicados** en Hive
7. ✅ Checkpoint actualizado

### Al ejecutar Consultas Analíticas:
1. ✅ Estadísticas por clase de objeto
2. ✅ Análisis de confianza
3. ✅ Distribución espacial
4. ✅ Análisis de colores
5. ✅ Análisis temporal (ventanas de 10s)

---



## 📚 Documentación Adicional

### Guías Incluidas
- `guias/Guia_Instalacion_Python310_OpenCV_v410.pdf` - Instalación de Python 3.10
- `guias/Manual_Instalacion_Apache_Hive.pdf` - Instalación de Hive
- `guias/Manual_Instalacion_Hadoop_3.4.2_BSG_Institute.pdf` - Instalación de Hadoop
- `StepByStepToInstallOpenCVWithCudaSupport.txt` - OpenCV con CUDA

### Referencias Externas
- [Documentación YOLO v11](https://docs.ultralytics.com/)
- [Apache Hive Documentation](https://hive.apache.org/)
- [Apache Hadoop Documentation](https://hadoop.apache.org/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

## 🎯 Casos de Uso del Proyecto

- **🔒 Seguridad y Vigilancia:** Detección de personas y objetos en tiempo real
- **🚗 Análisis de Tráfico:** Conteo de vehículos y peatones
- **🏪 Retail Analytics:** Análisis de comportamiento de clientes
- **🏭 Seguridad Industrial:** Detección de incidentes y anomalías
- **📊 Big Data Analytics:** Procesamiento masivo de datos visuales

---

## 👨‍💻 Autor

**José Gregorio Guardia**
Programa de Certificación de Ingeniero de Datos de IA
Curso: Procesos ETL para Cargas de Trabajo de IA

---

## 🚀 Inicio Rápido

```bash
# 1. Activar entorno virtual
source enviroments/project_final/bin/activate

# 2. Instalar dependencias
make install

# 3. Verificar instalación
make test

# 4. Ejecutar pipeline completo
make run

# 5. Ejecutar consultas analíticas
make queries
```

---

## 📝 Notas Finales

Este proyecto cumple con todos los requisitos del **Proyecto Final** del curso:

✅ **Arquitectura de dos sistemas separados** (Clasificación + ETL)
✅ **Python 3.10** en Ubuntu 24.04
✅ **YOLO v11** para detección de objetos
✅ **26+ atributos** extraídos por objeto
✅ **CSV como capa de staging**
✅ **ETL solo con Python** (sin PySpark)
✅ **Lotes de 10 segundos** para videos
✅ **Sin duplicados** en Hive
✅ **Makefile** completo
✅ **Pruebas unitarias** con pytest
✅ **5+ consultas analíticas** en Hive
✅ **Documentación completa**

**¡El sistema está listo para producción!** 🎉
