-- =========================== Kips Compras ===========================
SELECT 
    -- 1. Total comprado en el período
    SUM(pod.unit_cost * pod.quantity) AS total_comprado,
    
    -- 2. Órdenes de compra únicas
    COUNT(DISTINCT po.id) AS total_ordenes_compra,
    
    -- 3. Proveedores activos
    COUNT(DISTINCT po.supplier_id) AS proveedores_activos,
    
    -- 4. Productos distintos comprados
    COUNT(DISTINCT pod.product_id) AS productos_comprados,
    
    -- 5. Unidades totales
    SUM(pod.quantity) AS unidades_totales,
    
    -- 6. Costo promedio por orden
    SUM(pod.unit_cost * pod.quantity) / COUNT(DISTINCT po.id) AS costo_promedio_orden,
    
    -- 7. Costo promedio por unidad (ponderado)
    SUM(pod.unit_cost * pod.quantity) / SUM(pod.quantity) AS costo_promedio_unidad
FROM purchase_order_details pod
JOIN purchase_orders po ON pod.purchase_order_id = po.id;

-- =========================== Compras por Proveedor ===========================
SELECT 
    s.company AS Proveedor,
    SUM(pod.unit_cost * pod.quantity) AS Total_Comprado
FROM purchase_order_details pod
JOIN purchase_orders po ON pod.purchase_order_id = po.id
JOIN suppliers s ON po.supplier_id = s.id
GROUP BY s.id, s.company
ORDER BY Total_Comprado DESC
LIMIT 15;

-- =========================== Tendencia de Costos y Tiempo de Recepción ===========================
SELECT 
    DATE_FORMAT(po.creation_date, '%Y-%m') AS Mes,
    SUM(pod.unit_cost * pod.quantity) AS Costo_Total
FROM purchase_order_details pod
JOIN purchase_orders po ON pod.purchase_order_id = po.id
GROUP BY Mes
ORDER BY Mes;

SELECT 
    DATE_FORMAT(po.creation_date, '%Y-%m') AS Mes,
    AVG(DATEDIFF(pod.date_received, po.creation_date)) AS Promedio_Dias_Recepcion
FROM purchase_order_details pod
JOIN purchase_orders po ON pod.purchase_order_id = po.id
WHERE pod.date_received IS NOT NULL
GROUP BY Mes
ORDER BY Mes;
-- =========================== Órdenes Pendientes ===========================
SELECT 
    pod.purchase_order_id AS sk_purchase,
    po.supplier_id AS sk_supplier,
    pod.quantity,
    pod.unit_cost,
    (pod.quantity * pod.unit_cost) AS Total
FROM purchase_order_details pod
JOIN purchase_orders po ON pod.purchase_order_id = po.id
WHERE pod.posted_to_inventory = 0 
   OR pod.date_received IS NULL;

   
   