-- ------------------- Kpis pag Analisis de cliente --------------------------
SELECT 
    (SELECT COUNT(*) FROM northwind.customers) AS total_clientes,
    COUNT(DISTINCT o.customer_id) AS clientes_activos,
    (COUNT(DISTINCT o.customer_id) / (SELECT COUNT(*) FROM northwind.customers)) * 100 AS tasa_actividad,
    AVG(venta_por_cliente.total_gastado) AS compra_promedio_cliente
FROM northwind.orders o
CROSS JOIN (
    -- Subconsulta para el promedio de compra por cliente
    SELECT customer_id, SUM(quantity * unit_price * (1 - (discount / 100))) AS total_gastado
    FROM northwind.order_details od
    JOIN northwind.orders o ON od.order_id = o.id
    GROUP BY customer_id
) AS venta_por_cliente;

-- --------------- Cliente con mayor compras $ ------------
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))) AS total_compras
FROM northwind.customers c
JOIN northwind.orders o ON c.id = o.customer_id
JOIN northwind.order_details od ON o.id = od.order_id
GROUP BY c.id
ORDER BY total_compras DESC
LIMIT 1;

-- --------------- Distribución por Estado ------------
SELECT 
    state_province AS state, 
    COUNT(*) AS count
FROM northwind.customers
WHERE state_province IS NOT NULL
GROUP BY state_province
ORDER BY count DESC
LIMIT 8;

-- --------------- Top 10 Clientes por Ingresos ------------
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    c.company AS company_name,
    SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))) AS ingresos
FROM northwind.customers c
JOIN northwind.orders o ON c.id = o.customer_id
JOIN northwind.order_details od ON o.id = od.order_id
GROUP BY c.id, c.first_name, c.last_name, c.company
ORDER BY ingresos DESC
LIMIT 10;

-- --------------- Frecuencia de Compra ------------
SELECT 
    customer_id, 
    COUNT(id) AS num_orders
FROM northwind.orders
GROUP BY customer_id
ORDER BY num_orders DESC;

-- --------------- Clientes Nuevos por Mes ------------
SELECT 
    DATE_FORMAT(primera_compra, '%Y-%m') AS month,
    COUNT(customer_id) AS nuevos
FROM (
    -- Obtenemos la fecha mínima de orden para cada cliente
    SELECT customer_id, MIN(order_date) AS primera_compra
    FROM northwind.orders
    GROUP BY customer_id
) AS clientes_primera_vez
GROUP BY month
ORDER BY month ASC;