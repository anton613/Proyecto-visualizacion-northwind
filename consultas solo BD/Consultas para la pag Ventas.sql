/* Total de consultas para pag Ventas */

-- -----------------------------Total Ventas -----------------------------
SELECT 
    SUM(quantity * unit_price * (1 - (discount / 100))) AS total_ventas
FROM northwind.order_details;

-- -----------------------------Ticket Promedio: Cuanto gastan aprox por cada orden(ticket) -----------------------------
SELECT 
    AVG(subtotal_pedido) AS ticket_promedio
FROM (
    SELECT 
        order_id, 
        SUM(quantity * unit_price * (1 - (discount / 100))) AS subtotal_pedido
    FROM northwind.order_details
    GROUP BY order_id
) AS ventas_por_orden;

-- ----------------------------- Cnt de numero de ordenes -----------------------------
SELECT 
    COUNT(DISTINCT id) AS num_ordenes 
FROM northwind.orders;

SELECT 
    AVG(total_unidades) AS productos_por_orden
FROM (
    SELECT order_id, SUM(quantity) AS total_unidades
    FROM northwind.order_details
    GROUP BY order_id
) AS unidades_por_orden;

-- ----------------------------- Ventas reales cnt pedida * precio_unt * (100 - descuento)% -----------------------------
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS mes,
    SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))) AS ventas_reales
FROM northwind.orders o
JOIN northwind.order_details od ON o.id = od.order_id
GROUP BY mes
ORDER BY mes;

-- ----------------------------- Catogoria de producto con mayor ventas $ -----------------------------
SELECT 
    p.category AS Categoria,
    SUM(od.quantity) AS Unidades_Vendidas,
    ROUND(SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))), 2) AS Ventas_Totales
FROM 
    northwind.order_details od
JOIN 
    northwind.products p ON od.product_id = p.id
JOIN 
    northwind.orders o ON od.order_id = o.id
GROUP BY 
    p.category
ORDER BY 
    Ventas_Totales DESC;

-- ----------------------------- Top 10 Productos más Vendidos ------------------------------------
SELECT 
    p.product_name AS Producto,
    SUM(od.quantity) AS Unidades_Totales,
    ROUND(SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))), 2) AS Ventas_Netas
FROM 
    northwind.order_details od
JOIN 
    northwind.products p ON od.product_id = p.id
GROUP BY 
    p.product_name
ORDER BY 
    Ventas_Netas DESC
LIMIT 10;

-- ----------------------------- Ventas por Empleado -----------------------------
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) AS Empleado,
    COUNT(DISTINCT o.id) AS Cantidad_Ordenes,
    ROUND(SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))), 2) AS Total_Vendido
FROM 
    northwind.employees e
JOIN 
    northwind.orders o ON e.id = o.employee_id
JOIN 
    northwind.order_details od ON o.id = od.order_id
GROUP BY 
    e.id
ORDER BY 
    Total_Vendido DESC;
    
-- ----------------------------- Ventas por Estado -----------------------------
SELECT 
    o.ship_state_province AS Estado,
    COUNT(DISTINCT o.id) AS Numero_Pedidos,
    ROUND(SUM(od.quantity * od.unit_price * (1 - (od.discount / 100))), 2) AS Ventas_Totales
FROM 
    northwind.orders o
JOIN 
    northwind.order_details od ON o.id = od.order_id
WHERE 
    o.ship_state_province IS NOT NULL AND o.ship_state_province != ''
GROUP BY 
    o.ship_state_province
ORDER BY 
    Ventas_Totales DESC;