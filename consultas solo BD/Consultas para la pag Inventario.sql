-- ------------------- Kpis Inventario ---------------
SELECT 
    (SELECT COUNT(*) FROM northwind.products) AS total_productos,
    -- Contamos productos con comentarios de 'back order' en las transacciones
    (SELECT COUNT(DISTINCT product_id) 
     FROM northwind.inventory_transactions 
     WHERE comments LIKE '%back order%') AS productos_backorder,
    COUNT(*) AS total_transacciones,
    SUM(CASE WHEN transaction_type = 1 THEN quantity ELSE 0 END) AS total_entradas,
    SUM(CASE WHEN transaction_type = 2 THEN quantity ELSE 0 END) AS total_salidas,
    -- Ratio Entradas/Salidas
    SUM(CASE WHEN transaction_type = 1 THEN quantity ELSE 0 END) / 
    NULLIF(SUM(CASE WHEN transaction_type = 2 THEN quantity ELSE 0 END), 0) AS ratio_entradas_salidas
FROM northwind.inventory_transactions;

-- ------------------- Nivel de Stock por Categoría ----------------------------
SELECT 
    p.category AS categoria,
    SUM(it.quantity) AS cantidad_comprada
FROM northwind.inventory_transactions it
JOIN northwind.products p ON it.product_id = p.id
WHERE it.transaction_type = 1  -- 1 representa 'Purchased'
GROUP BY p.category
ORDER BY cantidad_comprada DESC;

-- ----------------------- Productos en Backorder --------------------------------
SELECT 
    p.product_name,
    SUM(it.quantity) AS cantidad_pendiente
FROM northwind.inventory_transactions it
JOIN northwind.products p ON it.product_id = p.id
WHERE it.comments LIKE '%back order%'
GROUP BY p.product_name;

-- ----------------------- Rotación de Inventario (Ventas vs Stock) --------------------------------
SELECT 
    p.product_name,
    -- Calculamos las Ventas Totales (Salidas)
    COALESCE(v.ventas_totales, 0) AS ventas_totales,
    -- Calculamos el Stock Total (Entradas por compra)
    COALESCE(s.stock_total, 0) AS stock_total
FROM northwind.products p
LEFT JOIN (
    -- Subconsulta de Ventas (Basada en pedidos reales)
    SELECT product_id, SUM(quantity) AS ventas_totales
    FROM northwind.order_details
    GROUP BY product_id
) v ON p.id = v.product_id
LEFT JOIN (
    -- Subconsulta de Stock (Basada en entradas al almacén)
    -- Usamos el ID 1 que corresponde a 'Purchased'
    SELECT product_id, SUM(quantity) AS stock_total
    FROM northwind.inventory_transactions
    WHERE transaction_type = 1 
    GROUP BY product_id
) s ON p.id = s.product_id;

-- ----------------- Entradas vs Salidas por Mes --------------------------
SELECT 
    DATE_FORMAT(transaction_created_date, '%Y-%m') AS mes,
    -- Sumamos las cantidades cuando el tipo es Entrada (1 = Purchased)
    SUM(CASE WHEN transaction_type = 1 THEN quantity ELSE 0 END) AS entradas,
    -- Sumamos las cantidades cuando el tipo es Salida (2 = Sold)
    SUM(CASE WHEN transaction_type = 2 THEN quantity ELSE 0 END) AS salidas
FROM northwind.inventory_transactions
GROUP BY mes
ORDER BY mes ASC;