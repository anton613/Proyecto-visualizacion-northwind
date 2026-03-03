import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# ==================== FUNCIONES PARA GRÁFICOS DE VENTAS ====================

def plot_ventas_mensuales(df_sales):
    """Evolución de Ventas Mensuales con descuento corregido"""
    if df_sales.empty:
        return None
    
    # Agrupamos por mes y sumamos el total ya corregido
    ventas_mensuales = df_sales.groupby('year_month')['line_total'].sum().reset_index()
    ventas_mensuales['year_month'] = ventas_mensuales['year_month'].astype(str)
    
    # Generar gráfico con Plotly
    fig = px.line(
        ventas_mensuales, 
        x='year_month', 
        y='line_total',
        title='Evolución de Ventas Mensuales (Netas)',
        labels={'year_month': 'Mes', 'line_total': 'Ventas ($)'},
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_ventas_por_categoria(df_sales, df_products):
    """Ventas por Categoría - Barras horizontales"""
    if df_sales.empty or df_products.empty:
        return None
    
    df_merged = df_sales.merge(df_products[['sk_product', 'category']], on='sk_product')
    ventas_categoria = df_merged.groupby('category')['line_total'].sum().sort_values(ascending=True).tail(10)
    
    fig = px.bar(
        x=ventas_categoria.values,
        y=ventas_categoria.index,
        orientation='h',
        title='Top 10 Categorías por Ventas',
        labels={'x': 'Ventas ($)', 'y': 'Categoría'}
    )
    return fig

def plot_ventas_por_region(df_sales, df_customers):
    """Ventas por Región/Estado - Mapa de calor con nombres reales"""
    if df_sales.empty or df_customers.empty:
        return None
    
    # 1. Diccionario de mapeo: Sigla -> Nombre Real
    us_state_to_abbrev = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }

    # 2. Unir ventas con clientes
    df_merged = df_sales.merge(
        df_customers[['sk_customer', 'state_province']], 
        on='sk_customer', 
        how='inner'
    )
    
    # 3. Agrupar por la sigla
    ventas_region = df_merged.groupby('state_province')['line_total'].sum().reset_index()
    
    # 4. Crear columna con el nombre real usando el mapeo
    ventas_region['nombre_estado'] = ventas_region['state_province'].map(us_state_to_abbrev)
    
    # 5. Crear el Mapa
    fig = px.choropleth(
        ventas_region,
        locations='state_province',     # Seguimos usando la sigla para la ubicación técnica
        locationmode="USA-states",
        color='line_total',
        scope="usa",
        # Hover data permite mostrar el nombre real al pasar el mouse
        hover_name='nombre_estado', 
        title='Ventas Netas por Estado (EE.UU.)',
        labels={'state_province': 'Código', 'line_total': 'Ventas ($)', 'nombre_estado': 'Estado'},
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        title_x=0.5
    )
    
    return fig

def plot_top_productos(df_sales, df_products):
    """Top 10 Productos Más Vendidos - Barras"""
    if df_sales.empty or df_products.empty:
        return None
    
    df_merged = df_sales.merge(df_products[['sk_product', 'product_name']], on='sk_product')
    top_productos = df_merged.groupby('product_name')['line_total'].sum().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=top_productos.index,
        y=top_productos.values,
        title='Top 10 Productos Más Vendidos',
        labels={'x': 'Producto', 'y': 'Ventas ($)'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_ventas_por_empleado(df_sales, df_employees):
    """Ventas por Empleado - Barras ordenadas"""
    if df_sales.empty or df_employees.empty:
        return None
    
    df_merged = df_sales.merge(df_employees[['sk_employee', 'full_name']], on='sk_employee')
    ventas_empleado = df_merged.groupby('full_name')['line_total'].sum().sort_values(ascending=False)
    
    fig = px.bar(
        x=ventas_empleado.index,
        y=ventas_empleado.values,
        title='Ventas por Empleado',
        labels={'x': 'Empleado', 'y': 'Ventas ($)'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# ==================== FUNCIONES PARA GRÁFICOS DE CLIENTES ====================

def plot_distribucion_clientes_region(df_customers):
    """Distribución de Clientes por Estado - Gráfico Circular con Nombres Completos"""
    if df_customers.empty:
        return None
    
    # 1. Diccionario de mapeo: Sigla -> Nombre Real
    us_state_to_abbrev = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }

    # 2. Contar clientes por estado
    region_counts = df_customers['state_province'].value_counts().reset_index()
    region_counts.columns = ['state_code', 'count']
    
    # 3. Crear columna con el nombre completo
    region_counts['state_name'] = region_counts['state_code'].map(us_state_to_abbrev).fillna(region_counts['state_code'])
    
    # 4. Crear el gráfico circular
    fig = px.pie(
        region_counts.head(8),
        values='count',
        names='state_name',
        title='Distribución de Clientes por Estado (Top 8)',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # 5. Ajustar posición del título y etiquetas
    fig.update_layout(
        title={
            'text': 'Distribución de Clientes por Estado (Top 8)',
            'x': 0.05,
            'xanchor': 'left'
        },
        legend_title_text='Estados'
    )
    
    return fig

def plot_top_clientes(df_sales, df_customers):
    """Top 10 Clientes por Ingresos - Barras"""
    if df_sales.empty or df_customers.empty:
        return None
    
    df_merged = df_sales.merge(df_customers[['sk_customer', 'full_name', 'company_name']], on='sk_customer')
    top_clientes = df_merged.groupby(['full_name', 'company_name'])['line_total'].sum().sort_values(ascending=False).head(10)
    
    # Preparar etiquetas
    labels = [f"{name} ({company})" for name, company in top_clientes.index]
    
    fig = px.bar(
        x=labels,
        y=top_clientes.values,
        title='Top 10 Clientes por Ingresos',
        labels={'x': 'Cliente', 'y': 'Ingresos ($)'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_frecuencia_compra(df_sales):
    """Frecuencia de Compra - Histograma"""
    if df_sales.empty:
        return None
    
    freq_compras = df_sales.groupby('sk_customer')['order_id'].nunique().reset_index()
    freq_compras.columns = ['customer', 'num_orders']
    
    fig = px.histogram(
        freq_compras,
        x='num_orders',
        nbins=20,
        title='Distribución de Frecuencia de Compra',
        labels={'num_orders': 'Número de Órdenes', 'count': 'Número de Clientes'}
    )
    return fig

def plot_clientes_nuevos_vs_recurrentes(df_sales, df_customers):
    """Clientes Nuevos vs Recurrentes - Líneas comparativas"""
    if df_sales.empty or 'date' not in df_sales.columns:
        return None
    
    # Primera compra por cliente
    primera_compra = df_sales.groupby('sk_customer')['date'].min().reset_index()
    primera_compra.columns = ['sk_customer', 'primera_compra']
    primera_compra['month'] = primera_compra['primera_compra'].dt.to_period('M')
    
    # Clientes nuevos por mes
    clientes_nuevos = primera_compra.groupby('month').size().reset_index(name='nuevos')
    clientes_nuevos['month'] = clientes_nuevos['month'].astype(str)
    
    fig = px.line(
        clientes_nuevos,
        x='month',
        y='nuevos',
        title='Clientes Nuevos por Mes',
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# ==================== FUNCIONES PARA GRÁFICOS DE INVENTARIO ====================

def plot_stock_por_categoria(df_inventory, df_products):
    """Nivel de Stock por Categoría - Barras apiladas"""
    if df_inventory.empty or df_products.empty:
        return None
    
    # Filtrar solo compras para ver entradas de stock
    compras = df_inventory[df_inventory['transaction_type'] == 'Purchased']
    compras_agg = compras.groupby('sk_product')['quantity'].sum().reset_index()
    
    df_merged = compras_agg.merge(df_products[['sk_product', 'category']], on='sk_product')
    stock_categoria = df_merged.groupby('category')['quantity'].sum().reset_index()
    
    fig = px.bar(
        stock_categoria.sort_values('quantity', ascending=False),
        x='category',
        y='quantity',
        title='Stock por Categoría (Unidades)',
        labels={'category': 'Categoría', 'quantity': 'Cantidad en Stock'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_productos_backorder(df_inventory, df_products):
    """Productos con Backorders - Tabla + indicador"""
    if df_inventory.empty:
        return None, 0
    
    backorders = df_inventory[df_inventory['is_backorder'] == True]
    productos_backorder = backorders['sk_product'].nunique()
    
    if not backorders.empty and not df_products.empty:
        backorders_detail = backorders.groupby('sk_product')['quantity'].sum().reset_index()
        backorders_detail = backorders_detail.merge(
            df_products[['sk_product', 'product_name']], 
            on='sk_product'
        )
        return backorders_detail[['product_name', 'quantity']], productos_backorder
    else:
        return pd.DataFrame(), productos_backorder

def plot_rotacion_inventario(df_sales, df_inventory, df_products):
    """Rotación de Inventario - Scatter (ventas vs stock)"""
    if df_sales.empty or df_inventory.empty or df_products.empty:
        return None
    
    # Ventas por producto
    ventas = df_sales.groupby('sk_product')['quantity'].sum().reset_index()
    ventas.columns = ['sk_product', 'ventas_totales']
    
    # Stock por producto (solo compras)
    compras = df_inventory[df_inventory['transaction_type'] == 'Purchased']
    stock = compras.groupby('sk_product')['quantity'].sum().reset_index()
    stock.columns = ['sk_product', 'stock_total']
    
    df_merged = ventas.merge(stock, on='sk_product', how='outer').fillna(0)
    df_merged = df_merged.merge(df_products[['sk_product', 'product_name']], on='sk_product')
    
    fig = px.scatter(
        df_merged,
        x='stock_total',
        y='ventas_totales',
        text='product_name',
        title='Rotación de Inventario: Ventas vs Stock',
        labels={'stock_total': 'Stock Total (Unidades)', 'ventas_totales': 'Ventas Totales (Unidades)'}
    )
    fig.update_traces(textposition='top center')
    return fig

def plot_movimientos_inventario(df_inventory):
    """Movimientos de Inventario - Excluyendo 'On Hold'"""
    if df_inventory.empty or 'sk_date' not in df_inventory.columns:
        return None
    
    # 1. Copiar y filtrar: Solo queremos 'Purchased' y 'Sold'
    df = df_inventory.copy()
    df = df[df['transaction_type'] != 'On Hold']
    
    # 2. Formatear fechas
    df['date'] = pd.to_datetime(df['sk_date'].astype(str), format='%Y%m%d')
    df['month'] = df['date'].dt.to_period('M')
    
    # 3. Agrupar
    movimientos = df.groupby(['month', 'transaction_type'])['quantity'].sum().reset_index()
    movimientos['month'] = movimientos['month'].astype(str)
    
    # 4. Graficar
    fig = px.line(
        movimientos,
        x='month',
        y='quantity',
        color='transaction_type',
        title='Evolución de Entradas y Salidas de Inventario (Neto)',
        markers=True,
        color_discrete_map={'Purchased': '#2ECC71', 'Sold': '#E74C3C'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        legend_title_text='Movimiento',
        margin=dict(l=20, r=20, t=50, b=20),
        title_x=0.02 # Alineado a la izquierda como pediste antes
    )
    
    return fig

# ==================== FUNCIONES PARA GRÁFICOS DE COMPRAS ====================

def plot_compras_por_proveedor(df_purchases, df_suppliers):
    """Compras por Proveedor - Barras"""
    if df_purchases.empty or df_suppliers.empty:
        return None
    
    compras_proveedor = df_purchases.groupby('sk_supplier').agg({
        'unit_cost': 'sum',
        'quantity': 'sum'
    }).reset_index()
    compras_proveedor['total'] = compras_proveedor['unit_cost'] * compras_proveedor['quantity']
    
    df_merged = compras_proveedor.merge(df_suppliers[['sk_supplier', 'company']], on='sk_supplier')
    
    fig = px.bar(
        df_merged.sort_values('total', ascending=False),
        x='company',
        y='total',
        title='Compras por Proveedor',
        labels={'company': 'Proveedor', 'total': 'Total Comprado ($)'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_tendencia_costos_compra(df_purchases):
    """Tendencia de Costos de Compra - Línea"""
    if df_purchases.empty or 'date' not in df_purchases.columns:
        return None
    
    df_purchases['month'] = df_purchases['date'].dt.to_period('M')
    costos_mensuales = df_purchases.groupby('month').apply(
        lambda x: (x['unit_cost'] * x['quantity']).sum()
    ).reset_index(name='costo_total')
    costos_mensuales['month'] = costos_mensuales['month'].astype(str)
    
    fig = px.line(
        costos_mensuales,
        x='month',
        y='costo_total',
        title='Tendencia de Costos de Compra',
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_tiempo_recepcion(df_purchases):
    """Tiempo Promedio de Recepción - Indicador + tendencia"""
    if df_purchases.empty or 'date_received' not in df_purchases.columns:
        return None, 0
    
    # Filtrar órdenes recibidas
    recibidas = df_purchases[df_purchases['date_received'].notna()].copy()
    if recibidas.empty:
        return None, 0
    
    recibidas['date_received'] = pd.to_datetime(recibidas['date_received'])
    recibidas['dias_recepcion'] = (recibidas['date_received'] - recibidas['date']).dt.days
    
    promedio_dias = recibidas['dias_recepcion'].mean()
    
    # Tendencia mensual
    recibidas['month'] = recibidas['date'].dt.to_period('M')
    tendencia = recibidas.groupby('month')['dias_recepcion'].mean().reset_index()
    tendencia['month'] = tendencia['month'].astype(str)
    
    fig = px.line(
        tendencia,
        x='month',
        y='dias_recepcion',
        title='Tiempo Promedio de Recepción por Mes',
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig, promedio_dias

def plot_ordenes_pendientes(df_purchases):
    """Órdenes Pendientes de Recibir - Contador + tabla"""
    if df_purchases.empty:
        return pd.DataFrame(), 0
    
    pendientes = df_purchases[
        (df_purchases['posted_to_inventory'] == False) | 
        (df_purchases['date_received'].isna())
    ]
    
    if not pendientes.empty:
        pendientes_display = pendientes[['sk_purchase', 'sk_supplier', 'quantity', 'unit_cost']].copy()
        pendientes_display['total'] = pendientes_display['quantity'] * pendientes_display['unit_cost']
        return pendientes_display, len(pendientes)
    else:
        return pd.DataFrame(), 0

# ==================== FUNCIONES PARA GRÁFICOS DE LOGÍSTICA ====================

def plot_uso_transportista(df_sales, df_shippers):
    """Uso por Transportista - Torta"""
    if df_sales.empty or df_shippers.empty:
        return None
    
    uso = df_sales['sk_shipper'].value_counts().reset_index()
    uso.columns = ['sk_shipper', 'count']
    
    df_merged = uso.merge(df_shippers[['sk_shipper', 'company']], on='sk_shipper')
    
    fig = px.pie(
        df_merged,
        values='count',
        names='company',
        title='Distribución de Uso por Transportista',
        hole=0.3
    )
    return fig

def plot_costo_promedio_envio(df_sales, df_shippers):
    """Costo Promedio de Envío - Barras por transportista"""
    if df_sales.empty or df_shippers.empty:
        return None
    
    costo_transportista = df_sales.groupby('sk_shipper')['shipping_fee'].mean().reset_index()
    costo_transportista = costo_transportista.merge(df_shippers[['sk_shipper', 'company']], on='sk_shipper')
    
    fig = px.bar(
        costo_transportista,
        x='company',
        y='shipping_fee',
        title='Costo Promedio de Envío por Transportista',
        labels={'company': 'Transportista', 'shipping_fee': 'Costo Promedio ($)'}
    )
    return fig

def plot_ordenes_sin_transportista(df_sales):
    """Órdenes sin Transportista Asignado - Contador de alerta"""
    if df_sales.empty:
        return 0, pd.DataFrame()
    
    sin_transportista = df_sales[df_sales['sk_shipper'].isna()]
    
    if not sin_transportista.empty:
        ordenes_sin = sin_transportista['order_id'].nunique()
        detalle = sin_transportista[['order_id', 'sk_customer', 'quantity', 'line_total']].drop_duplicates('order_id')
        return ordenes_sin, detalle
    else:
        return 0, pd.DataFrame()

# ==================== FUNCIONES PARA KPIs ESPECÍFICOS ====================

def get_ventas_kpis(df_sales):
    """KPIs para el área de Ventas"""
    kpis = {}
    
    if df_sales.empty:
        return kpis
    
    # Total ventas
    kpis['total_ventas'] = df_sales['line_total'].sum()
    
    # Ticket promedio
    kpis['ticket_promedio'] = df_sales.groupby('order_id')['line_total'].sum().mean()
    
    # Número de órdenes
    kpis['num_ordenes'] = df_sales['order_id'].nunique()
    
    # Productos por orden
    kpis['productos_por_orden'] = df_sales.groupby('order_id')['quantity'].sum().mean()
    
    # Mes con más ventas
    if 'year_month' in df_sales.columns:
        ventas_mensuales = df_sales.groupby('year_month')['line_total'].sum()
        kpis['mes_top_ventas'] = ventas_mensuales.idxmax()
        kpis['ventas_mes_top'] = ventas_mensuales.max()
    
    return kpis

def get_clientes_kpis(df_sales, df_customers):
    """KPIs para el área de Clientes"""
    kpis = {}
    
    if df_sales.empty or df_customers.empty:
        return kpis
    
    # Total clientes
    kpis['total_clientes'] = df_customers['sk_customer'].nunique()
    
    # Clientes con compras
    clientes_compras = df_sales['sk_customer'].nunique()
    kpis['clientes_activos'] = clientes_compras
    kpis['tasa_actividad'] = (clientes_compras / kpis['total_clientes']) * 100
    
    # Cliente top
    top_cliente = df_sales.groupby('sk_customer')['line_total'].sum().idxmax()
    top_cliente_info = df_customers[df_customers['sk_customer'] == top_cliente]
    if not top_cliente_info.empty:
        kpis['cliente_top'] = top_cliente_info['full_name'].iloc[0]
        kpis['ventas_cliente_top'] = df_sales.groupby('sk_customer')['line_total'].sum().max()
    
    # Compra promedio por cliente
    kpis['compra_promedio_cliente'] = df_sales.groupby('sk_customer')['line_total'].sum().mean()
    
    return kpis

def get_inventario_kpis(df_inventory, df_products):
    """KPIs para el área de Inventario"""
    kpis = {}
    
    if df_inventory.empty:
        return kpis
    
    # Total productos
    kpis['total_productos'] = df_products['sk_product'].nunique() if not df_products.empty else 0
    
    # Productos con backorder
    kpis['productos_backorder'] = df_inventory[df_inventory['is_backorder'] == True]['sk_product'].nunique()
    
    # Transacciones totales
    kpis['total_transacciones'] = len(df_inventory)
    
    # Entradas vs Salidas
    entradas = df_inventory[df_inventory['transaction_type'] == 'Purchased']['quantity'].sum()
    salidas = df_inventory[df_inventory['transaction_type'] == 'Sold']['quantity'].sum()
    kpis['total_entradas'] = entradas
    kpis['total_salidas'] = salidas
    kpis['ratio_entradas_salidas'] = entradas / salidas if salidas > 0 else 0
    
    return kpis

def get_compras_kpis(df_purchases):
    """KPIs para el área de Compras"""
    kpis = {}
    
    if df_purchases.empty:
        return kpis
    
    # Total comprado
    kpis['total_comprado'] = (df_purchases['unit_cost'] * df_purchases['quantity']).sum()
    
    # Órdenes de compra
    kpis['total_ordenes_compra'] = df_purchases['purchase_order_id'].nunique()
    
    # Órdenes pendientes
    kpis['ordenes_pendientes'] = df_purchases[df_purchases['date_received'].isna()]['purchase_order_id'].nunique()
    
    # Tasa de recepción
    kpis['tasa_recepcion'] = (1 - kpis['ordenes_pendientes'] / kpis['total_ordenes_compra']) * 100
    
    # Costo promedio por orden
    kpis['costo_promedio_orden'] = kpis['total_comprado'] / kpis['total_ordenes_compra']
    
    return kpis

def get_logistica_kpis(df_sales, df_shippers):
    """KPIs para el área de Logística"""
    kpis = {}
    
    if df_sales.empty:
        return kpis
    
    # Total envíos
    kpis['total_envios'] = df_sales['sk_shipper'].notna().sum()
    
    # Órdenes sin transportista
    kpis['ordenes_sin_transportista'] = df_sales['sk_shipper'].isna().sum()
    
    # Costo envío promedio
    kpis['costo_envio_promedio'] = df_sales['shipping_fee'].mean()
    
    # Transportista más usado
    if not df_shippers.empty and kpis['total_envios'] > 0:
        top_shipper_id = df_sales['sk_shipper'].value_counts().index[0]
        top_shipper = df_shippers[df_shippers['sk_shipper'] == top_shipper_id]
        if not top_shipper.empty:
            kpis['transportista_top'] = top_shipper['company'].iloc[0]
    
    return kpis