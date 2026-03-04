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
WITH PrimerasCompras AS (
    -- Identificamos la fecha de la primera orden de cada cliente
    SELECT 
        customer_id, 
        MIN(order_date) as fecha_inicio
    FROM orders
    GROUP BY customer_id
),
ClasificacionOrdenes AS (
    -- Clasificamos cada orden como 'Nuevo' o 'Recurrente'
    SELECT 
        o.customer_id,
        o.order_date,
        -- Truncamos la fecha al primer día del mes para agrupar temporalmente
        DATE_FORMAT(o.order_date, '%Y-%m-01') AS mes,
        CASE 
            WHEN o.order_date = pc.fecha_inicio THEN 'Nuevo'
            ELSE 'Recurrente'
        END AS tipo_cliente
    FROM orders o
    JOIN PrimerasCompras pc ON o.customer_id = pc.customer_id
)
-- Agrupamos para obtener el conteo único de clientes por mes y tipo
SELECT 
    mes,
    tipo_cliente,
    COUNT(DISTINCT customer_id) AS total_clientes
FROM ClasificacionOrdenes
GROUP BY mes, tipo_cliente
ORDER BY mes ASC, tipo_cliente DESC;