import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, get_date_filtered_data
from utils.charts import (
    plot_ventas_mensuales, plot_ventas_por_categoria, plot_ventas_por_region,
    plot_top_productos, plot_ventas_por_empleado, get_ventas_kpis
)
from utils.ui_components import hide_auto_navigation, render_sidebar

st.set_page_config(page_title="Ventas - Northwind", page_icon="📈", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

data = load_data()

st.title("📈 Análisis de Ventas")
st.markdown("---")

# --- MODIFICADO: Pasar data a render_sidebar ---
fechas, filtros_extra = render_sidebar(page_type="ventas", data=data)
if isinstance(fechas, tuple) and len(fechas) == 2:
    start_date, end_date = fechas
else:
    start_date, end_date = pd.to_datetime('2025-01-01'), pd.to_datetime('2025-12-31')

hide_auto_navigation()

# Filtrar datos por fecha
filtered_data = get_date_filtered_data(data, start_date, end_date)
df_sales_filtered = filtered_data['fact_sales'].copy()

# Verificar si hay datos después del filtro de fecha
if df_sales_filtered.empty:
    st.warning("⚠️ No hay datos de ventas en el período seleccionado")
    df_sales_filtered = pd.DataFrame()

# APLICAR FILTROS DE CATEGORÍA (AHORA CON DATOS REALES)
if filtros_extra and filtros_extra.get('categoria') and not df_sales_filtered.empty:
    categorias_seleccionadas = filtros_extra['categoria']
    if categorias_seleccionadas:
        productos_categoria = data['dim_products'][data['dim_products']['category'].isin(categorias_seleccionadas)]
        if not productos_categoria.empty:
            sk_products_filtrados = productos_categoria['sk_product'].unique()
            df_sales_filtered = df_sales_filtered[df_sales_filtered['sk_product'].isin(sk_products_filtrados)]
            if df_sales_filtered.empty:
                st.info(f"ℹ️ No hay ventas en las categorías seleccionadas para el período")

# KPIs de Ventas (usando datos filtrados)
kpis = get_ventas_kpis(df_sales_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ventas Totales", f"${kpis.get('total_ventas', 0):,.0f}")

with col2:
    st.metric("Ticket Promedio", f"${kpis.get('ticket_promedio', 0):,.2f}")

with col3:
    st.metric("Número de Órdenes", f"{kpis.get('num_ordenes', 0):,}")

with col4:
    st.metric("Productos por Orden", f"{kpis.get('productos_por_orden', 0):.1f}")

# Mostrar período seleccionado
st.caption(f"📅 Datos mostrados: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")
if filtros_extra and filtros_extra.get('categoria'):
    st.caption(f"🏷️ Categorías seleccionadas: {', '.join(filtros_extra['categoria'])}")

st.markdown("---")

# Gráficos de Ventas
col1, col2 = st.columns(2)

with col1:
    # GRÁFICO DE LÍNEA DE TIEMPO - SIN FILTRO DE TIEMPO (usa datos completos)
    fig_ventas_mensuales = plot_ventas_mensuales(data['fact_sales'])  # Usamos datos completos sin filtrar
    if fig_ventas_mensuales:
        st.plotly_chart(fig_ventas_mensuales, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar evolución de ventas")

with col2:
    fig_ventas_categoria = plot_ventas_por_categoria(df_sales_filtered, data['dim_products'])
    if fig_ventas_categoria:
        st.plotly_chart(fig_ventas_categoria, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar ventas por categoría en el período seleccionado")

col1, col2 = st.columns(2)

with col1:
    fig_top_productos = plot_top_productos(df_sales_filtered, data['dim_products'])
    if fig_top_productos:
        st.plotly_chart(fig_top_productos, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar top productos en el período seleccionado")

with col2:
    fig_ventas_empleado = plot_ventas_por_empleado(df_sales_filtered, data['dim_employees'])
    if fig_ventas_empleado:
        st.plotly_chart(fig_ventas_empleado, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar ventas por empleado en el período seleccionado")

# Gráfico de región ocupa todo el ancho
st.markdown("---")
fig_ventas_region = plot_ventas_por_region(df_sales_filtered, data['dim_customers'])
if fig_ventas_region:
    st.plotly_chart(fig_ventas_region, use_container_width=True)
else:
    st.info("No hay datos suficientes para mostrar ventas por región en el período seleccionado")