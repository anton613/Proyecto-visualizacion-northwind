-- =========================== KPIs Logística ===========================
SELECT 
    -- Cuenta cuántos pedidos tienen un transportista asignado
    COUNT(shipper_id) AS total_envios,
    
    -- Detecta órdenes que no tienen shipper_id (pendientes de despacho)
    SUM(CASE WHEN shipper_id IS NULL THEN 1 ELSE 0 END) AS ordenes_sin_transportista,
    
    -- Promedio del cargo por envío registrado en la tabla orders
    AVG(shipping_fee) AS costo_envio_promedio,
    
    -- Subconsulta para identificar el nombre de la empresa de transporte más utilizada
    (SELECT s.company 
     FROM orders o 
     JOIN shippers s ON o.shipper_id = s.id 
     GROUP BY s.company 
     ORDER BY COUNT(*) DESC 
     LIMIT 1) AS transportista_top
FROM orders;


-- =========================== Distribución de Uso por Transportista ===========================
SELECT 
    s.company AS transportista,
    COUNT(o.id) AS cantidad_pedidos
FROM orders o
JOIN shippers s ON o.shipper_id = s.id
GROUP BY s.company
ORDER BY cantidad_pedidos DESC;


-- =========================== Costo Promedio de Envío por Transportista ===========================
SELECT 
    s.company AS transportista,
    AVG(o.shipping_fee) AS costo_promedio_envio
FROM orders o
JOIN shippers s ON o.shipper_id = s.id
GROUP BY s.company
ORDER BY costo_promedio_envio DESC;


-- =========================== Alerta: Órdenes sin Transportista Asignado ===========================
SELECT 
    o.id AS order_id, 
    o.customer_id, 
    o.order_date, 
    o.ship_city,
    o.ship_country_region,
    -- Calcula el total de unidades de la orden para medir la magnitud del envío
    (SELECT SUM(quantity) FROM order_details WHERE order_id = o.id) AS unidades_totales
FROM orders o
WHERE o.shipper_id IS NULL;