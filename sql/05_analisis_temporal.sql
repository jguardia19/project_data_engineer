-- ===================================
-- ANÁLISIS TEMPORAL
-- ===================================

-- 1. Detecciones por fecha de ingesta
SELECT 
    DATE(ingestion_date) as fecha,
    COUNT(*) as detecciones_del_dia,
    COUNT(DISTINCT source_id) as archivos_procesados
FROM yolo_project.yolo_objects 
GROUP BY DATE(ingestion_date) 
ORDER BY fecha DESC;

-- 2. Detecciones por hora del día
SELECT 
    HOUR(ingestion_date) as hora,
    COUNT(*) as cantidad
FROM yolo_project.yolo_objects 
GROUP BY HOUR(ingestion_date) 
ORDER BY hora;

-- 3. Análisis de videos por timestamp
SELECT 
    source_id,
    MIN(timestamp_sec) as inicio_video,
    MAX(timestamp_sec) as fin_video,
    (MAX(timestamp_sec) - MIN(timestamp_sec)) as duracion_segundos,
    COUNT(*) as total_detecciones
FROM yolo_project.yolo_objects 
WHERE source_type = 'video'
GROUP BY source_id 
ORDER BY total_detecciones DESC;

-- 4. Últimas detecciones procesadas
SELECT 
    source_id,
    class_name,
    confidence,
    ingestion_date
FROM yolo_project.yolo_objects 
ORDER BY ingestion_date DESC 
LIMIT 20;