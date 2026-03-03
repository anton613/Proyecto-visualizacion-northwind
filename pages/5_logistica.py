import streamlit as st
from utils.data_loader import load_all_data
from utils.charts import (
    plot_uso_transportista, plot_costo_promedio_envio,
    plot_ordenes_sin_transportista, get_logistica_kpis
)
from utils.ui_components import hide_auto_navigation, render_sidebar

st.set_page_config(page_title="Logística - Northwind", page_icon="🚚", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

data = load_data()

st.title("🚚 Análisis de Logística")
st.markdown("---")

hide_auto_navigation()
render_sidebar()

# KPIs de Logística
kpis = get_logistica_kpis(data['fact_sales'], data['dim_shippers'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Envíos", f"{kpis.get('total_envios', 0):,}")

with col2:
    st.metric("Órdenes sin Transportista", f"{kpis.get('ordenes_sin_transportista', 0):,}")

with col3:
    st.metric("Costo Envío Promedio", f"${kpis.get('costo_envio_promedio', 0):,.2f}")

with col4:
    st.metric("Transportista Principal", kpis.get('transportista_top', 'N/A'))

st.markdown("---")

# Gráficos de Logística
col1, col2 = st.columns(2)

with col1:
    fig_uso_transportista = plot_uso_transportista(data['fact_sales'], data['dim_shippers'])
    if fig_uso_transportista:
        st.plotly_chart(fig_uso_transportista, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar uso por transportista")

with col2:
    fig_costos_envio = plot_costo_promedio_envio(data['fact_sales'], data['dim_shippers'])
    if fig_costos_envio:
        st.plotly_chart(fig_costos_envio, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar costos de envío")

# Alerta de órdenes sin transportista
ordenes_sin, detalle_sin = plot_ordenes_sin_transportista(data['fact_sales'])
if ordenes_sin > 0:
    st.error(f"⚠️ **ALERTA:** {ordenes_sin} órdenes necesitan asignación de transportista")
    
    with st.expander("Ver detalles de órdenes sin transportista"):
        st.dataframe(detalle_sin, use_container_width=True)
else:
    st.success("✅ Todas las órdenes tienen transportista asignado")