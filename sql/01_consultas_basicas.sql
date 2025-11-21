-- ===================================
-- CONSULTAS BÁSICAS - YOLO OBJECTS
-- ===================================

-- 1. Ver todos los registros
SELECT * FROM yolo_project.yolo_objects LIMIT 10;

-- 2. Contar total de detecciones
SELECT COUNT(*) as total_detecciones 
FROM yolo_project.yolo_objects;

-- 3. Distribución por clase
SELECT 
    class_name,
    COUNT(*) as cantidad,
    ROUND(AVG(confidence), 3) as confianza_promedio
FROM yolo_project.yolo_objects 
GROUP BY class_name 
ORDER BY cantidad DESC;

-- 4. Detecciones por tipo de fuente
SELECT 
    source_type,
    COUNT(*) as cantidad
FROM yolo_project.yolo_objects 
GROUP BY source_type;

-- 5. Top 10 detecciones con mayor confianza
SELECT 
    source_id,
    class_name,
    confidence,
    ingestion_date
FROM yolo_project.yolo_objects 
ORDER BY confidence DESC 
LIMIT 10;