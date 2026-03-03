import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
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

hide_auto_navigation()
render_sidebar()

# KPIs de Ventas
kpis = get_ventas_kpis(data['fact_sales'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ventas Totales", f"${kpis.get('total_ventas', 0):,.0f}")

with col2:
    st.metric("Ticket Promedio", f"${kpis.get('ticket_promedio', 0):,.2f}")

with col3:
    st.metric("Número de Órdenes", f"{kpis.get('num_ordenes', 0):,}")

with col4:
    st.metric("Productos por Orden", f"{kpis.get('productos_por_orden', 0):.1f}")

st.markdown("---")

# Gráficos de Ventas
col1, col2 = st.columns(2)

with col1:
    fig_ventas_mensuales = plot_ventas_mensuales(data['fact_sales'])
    if fig_ventas_mensuales:
        st.plotly_chart(fig_ventas_mensuales, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar evolución de ventas")

with col2:
    fig_ventas_categoria = plot_ventas_por_categoria(data['fact_sales'], data['dim_products'])
    if fig_ventas_categoria:
        st.plotly_chart(fig_ventas_categoria, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar ventas por categoría")

col1, col2 = st.columns(2)

with col1:
    fig_top_productos = plot_top_productos(data['fact_sales'], data['dim_products'])
    if fig_top_productos:
        st.plotly_chart(fig_top_productos, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar top productos")

with col2:
    fig_ventas_empleado = plot_ventas_por_empleado(data['fact_sales'], data['dim_employees'])
    if fig_ventas_empleado:
        st.plotly_chart(fig_ventas_empleado, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar ventas por empleado")

# Gráfico de región ocupa todo el ancho
st.markdown("---")
fig_ventas_region = plot_ventas_por_region(data['fact_sales'], data['dim_customers'])
if fig_ventas_region:
    st.plotly_chart(fig_ventas_region, use_container_width=True)
else:
    st.info("No hay datos suficientes para mostrar ventas por región")