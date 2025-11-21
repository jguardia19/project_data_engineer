-- ===================================
-- ANÁLISIS DE COLORES DOMINANTES
-- ===================================

-- 1. Distribución de colores dominantes
SELECT 
    dominant_color_name,
    COUNT(*) as cantidad,
    ROUND(AVG(confidence), 3) as confianza_promedio
FROM yolo_project.yolo_objects 
GROUP BY dominant_color_name 
ORDER BY cantidad DESC;

-- 2. Colores por clase de objeto
SELECT 
    class_name,
    dominant_color_name,
    COUNT(*) as cantidad
FROM yolo_project.yolo_objects 
GROUP BY class_name, dominant_color_name 
ORDER BY class_name, cantidad DESC;

-- 3. Valores RGB promedio por clase
SELECT 
    class_name,
    ROUND(AVG(dom_r), 1) as rojo_promedio,
    ROUND(AVG(dom_g), 1) as verde_promedio,
    ROUND(AVG(dom_b), 1) as azul_promedio,
    COUNT(*) as total_detecciones
FROM yolo_project.yolo_objects 
GROUP BY class_name 
ORDER BY total_detecciones DESC;

-- 4. Objetos con colores más intensos
SELECT 
    source_id,
    class_name,
    dominant_color_name,
    dom_r,
    dom_g,
    dom_b,
    (dom_r + dom_g + dom_b) as intensidad_total
FROM yolo_project.yolo_objects 
ORDER BY intensidad_total DESC 
LIMIT 10;