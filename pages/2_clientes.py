import streamlit as st
from utils.data_loader import load_all_data
from utils.charts import (
    plot_distribucion_clientes_region, plot_top_clientes,
    plot_frecuencia_compra, plot_clientes_nuevos_vs_recurrentes,
    get_clientes_kpis
)
from utils.ui_components import hide_auto_navigation, render_sidebar

st.set_page_config(page_title="Clientes - Northwind", page_icon="👥", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

data = load_data()

st.title("👥 Análisis de Clientes")
st.markdown("---")

hide_auto_navigation()
render_sidebar()

# KPIs de Clientes
kpis = get_clientes_kpis(data['fact_sales'], data['dim_customers'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Clientes", f"{kpis.get('total_clientes', 0):,}")

with col2:
    st.metric("Clientes Activos", f"{kpis.get('clientes_activos', 0):,}")

with col3:
    st.metric("Tasa de Actividad", f"{kpis.get('tasa_actividad', 0):.1f}%")

with col4:
    st.metric("Compra Promedio por Cliente", f"${kpis.get('compra_promedio_cliente', 0):,.2f}")

if kpis.get('cliente_top'):
    st.info(f"🏆 **Cliente Destacado:** {kpis['cliente_top']} con ${kpis.get('ventas_cliente_top', 0):,.2f} en compras")

st.markdown("---")

# Gráficos de Clientes
col1, col2 = st.columns(2)

with col1:
    fig_distribucion = plot_distribucion_clientes_region(data['dim_customers'])
    if fig_distribucion:
        st.plotly_chart(fig_distribucion, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar distribución por región")

with col2:
    fig_top_clientes = plot_top_clientes(data['fact_sales'], data['dim_customers'])
    if fig_top_clientes:
        st.plotly_chart(fig_top_clientes, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar top clientes")

col1, col2 = st.columns(2)

with col1:
    fig_frecuencia = plot_frecuencia_compra(data['fact_sales'])
    if fig_frecuencia:
        st.plotly_chart(fig_frecuencia, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar frecuencia de compra")

with col2:
    fig_nuevos_recurrentes = plot_clientes_nuevos_vs_recurrentes(data['fact_sales'], data['dim_customers'])
    if fig_nuevos_recurrentes:
        st.plotly_chart(fig_nuevos_recurrentes, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar clientes nuevos")