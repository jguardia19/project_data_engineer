-- ===================================
-- ANÁLISIS ESPACIAL Y POSICIONES
-- ===================================

-- 1. Distribución por región de posición
SELECT 
    position_region,
    COUNT(*) as cantidad,
    ROUND(AVG(confidence), 3) as confianza_promedio
FROM yolo_project.yolo_objects 
GROUP BY position_region 
ORDER BY cantidad DESC;

-- 2. Análisis de tamaños de bounding boxes
SELECT 
    class_name,
    ROUND(AVG(width), 2) as ancho_promedio,
    ROUND(AVG(height), 2) as alto_promedio,
    ROUND(AVG(area_pixels), 2) as area_promedio,
    ROUND(AVG(bbox_area_ratio), 4) as ratio_area_promedio
FROM yolo_project.yolo_objects 
GROUP BY class_name 
ORDER BY area_promedio DESC;

-- 3. Objetos más grandes por clase
SELECT 
    class_name,
    source_id,
    width,
    height,
    area_pixels,
    confidence
FROM yolo_project.yolo_objects 
WHERE (class_name, area_pixels) IN (
    SELECT class_name, MAX(area_pixels)
    FROM yolo_project.yolo_objects 
    GROUP BY class_name
)
ORDER BY area_pixels DESC;

-- 4. Centros de masa por clase
SELECT 
    class_name,
    ROUND(AVG(center_x_norm), 3) as centro_x_promedio,
    ROUND(AVG(center_y_norm), 3) as centro_y_promedio,
    COUNT(*) as total_detecciones
FROM yolo_project.yolo_objects 
GROUP BY class_name;