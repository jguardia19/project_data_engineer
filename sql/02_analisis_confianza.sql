-- ===================================
-- ANÁLISIS DE CONFIANZA
-- ===================================

-- 1. Estadísticas de confianza por clase
SELECT 
    class_name,
    COUNT(*) as total_detecciones,
    ROUND(MIN(confidence), 3) as confianza_minima,
    ROUND(MAX(confidence), 3) as confianza_maxima,
    ROUND(AVG(confidence), 3) as confianza_promedio,
    ROUND(STDDEV(confidence), 3) as desviacion_estandar
FROM yolo_project.yolo_objects 
GROUP BY class_name 
ORDER BY confianza_promedio DESC;

-- 2. Detecciones con alta confianza (>0.8)
SELECT 
    class_name,
    COUNT(*) as detecciones_alta_confianza
FROM yolo_project.yolo_objects 
WHERE confidence > 0.8
GROUP BY class_name 
ORDER BY detecciones_alta_confianza DESC;

-- 3. Detecciones con baja confianza (<0.5)
SELECT 
    source_id,
    class_name,
    confidence,
    position_region
FROM yolo_project.yolo_objects 
WHERE confidence < 0.5
ORDER BY confidence ASC;

-- 4. Distribución de confianza por rangos
SELECT 
    CASE 
        WHEN confidence >= 0.9 THEN 'Muy Alta (0.9-1.0)'
        WHEN confidence >= 0.7 THEN 'Alta (0.7-0.9)'
        WHEN confidence >= 0.5 THEN 'Media (0.5-0.7)'
        ELSE 'Baja (<0.5)'
    END as rango_confianza,
    COUNT(*) as cantidad
FROM yolo_project.yolo_objects 
GROUP BY 
    CASE 
        WHEN confidence >= 0.9 THEN 'Muy Alta (0.9-1.0)'
        WHEN confidence >= 0.7 THEN 'Alta (0.7-0.9)'
        WHEN confidence >= 0.5 THEN 'Media (0.5-0.7)'
        ELSE 'Baja (<0.5)'
    END
ORDER BY cantidad DESC;