-- ===================================
-- REPORTES AVANZADOS
-- ===================================

-- 1. Reporte completo por archivo
SELECT 
    source_id,
    source_type,
    COUNT(*) as total_detecciones,
    COUNT(DISTINCT class_name) as clases_diferentes,
    ROUND(AVG(confidence), 3) as confianza_promedio,
    MAX(ingestion_date) as fecha_procesamiento
FROM yolo_project.yolo_objects 
GROUP BY source_id, source_type 
ORDER BY total_detecciones DESC;

-- 2. Top archivos con más diversidad de objetos
SELECT 
    source_id,
    COUNT(DISTINCT class_name) as clases_detectadas,
    COUNT(*) as total_detecciones,
    COLLECT_SET(class_name) as lista_clases
FROM yolo_project.yolo_objects 
GROUP BY source_id 
ORDER BY clases_detectadas DESC, total_detecciones DESC 
LIMIT 10;

-- 3. Matriz de co-ocurrencia (objetos que aparecen juntos)
SELECT 
    a.class_name as clase_1,
    b.class_name as clase_2,
    COUNT(*) as apariciones_juntas
FROM yolo_project.yolo_objects a
JOIN yolo_project.yolo_objects b ON a.source_id = b.source_id 
WHERE a.class_name < b.class_name
GROUP BY a.class_name, b.class_name 
HAVING COUNT(*) > 1
ORDER BY apariciones_juntas DESC;

-- 4. Resumen ejecutivo
SELECT 
    'Total de archivos procesados' as metrica,
    CAST(COUNT(DISTINCT source_id) AS STRING) as valor
FROM yolo_project.yolo_objects
UNION ALL
SELECT 
    'Total de detecciones',
    CAST(COUNT(*) AS STRING)
FROM yolo_project.yolo_objects
UNION ALL
SELECT 
    'Clases diferentes detectadas',
    CAST(COUNT(DISTINCT class_name) AS STRING)
FROM yolo_project.yolo_objects
UNION ALL
SELECT 
    'Confianza promedio general',
    CAST(ROUND(AVG(confidence), 3) AS STRING)
FROM yolo_project.yolo_objects;