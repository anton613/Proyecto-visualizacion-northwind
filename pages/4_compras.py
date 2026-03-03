import streamlit as st
from utils.data_loader import load_all_data
from utils.charts import (
    plot_compras_por_proveedor, plot_tendencia_costos_compra,
    plot_tiempo_recepcion, plot_ordenes_pendientes,
    get_compras_kpis
)
from utils.ui_components import hide_auto_navigation, render_sidebar

st.set_page_config(page_title="Compras - Northwind", page_icon="🛒", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

data = load_data()

st.title("🛒 Análisis de Compras")
st.markdown("---")

hide_auto_navigation()
render_sidebar()

# KPIs de Compras
kpis = get_compras_kpis(data['fact_purchases'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Comprado", f"${kpis.get('total_comprado', 0):,.0f}")

with col2:
    st.metric("Órdenes de Compra", f"{kpis.get('total_ordenes_compra', 0):,}")

with col3:
    st.metric("Órdenes Pendientes", f"{kpis.get('ordenes_pendientes', 0):,}")

with col4:
    st.metric("Costo Promedio por Orden", f"${kpis.get('costo_promedio_orden', 0):,.2f}")

st.markdown("---")

# Gráficos de Compras
col1, col2 = st.columns(2)

with col1:
    fig_compras_proveedor = plot_compras_por_proveedor(data['fact_purchases'], data['dim_suppliers'])
    if fig_compras_proveedor:
        st.plotly_chart(fig_compras_proveedor, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar compras por proveedor")

with col2:
    fig_tendencia_costos = plot_tendencia_costos_compra(data['fact_purchases'])
    if fig_tendencia_costos:
        st.plotly_chart(fig_tendencia_costos, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar tendencia de costos")

# Segunda fila
col1, col2 = st.columns(2)

with col1:
    fig_tiempo_recepcion, promedio_dias = plot_tiempo_recepcion(data['fact_purchases'])
    if fig_tiempo_recepcion:
        st.plotly_chart(fig_tiempo_recepcion, use_container_width=True)
        st.metric("Tiempo Promedio de Recepción", f"{promedio_dias:.1f} días")
    else:
        st.info("No hay datos suficientes para mostrar tiempo de recepción")

with col2:
    pendientes_df, num_pendientes = plot_ordenes_pendientes(data['fact_purchases'])
    if not pendientes_df.empty:
        st.subheader(f"📋 Órdenes Pendientes de Recibir ({num_pendientes})")
        st.dataframe(pendientes_df, use_container_width=True)
    else:
        st.info("No hay órdenes pendientes de recibir")