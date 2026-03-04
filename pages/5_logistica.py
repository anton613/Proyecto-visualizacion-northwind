import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, get_date_filtered_data
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

fechas, filtros_extra = render_sidebar(page_type="logistica")
if isinstance(fechas, tuple) and len(fechas) == 2:
    start_date, end_date = fechas
else:
    start_date, end_date = pd.to_datetime('2025-01-01'), pd.to_datetime('2025-12-31')

hide_auto_navigation()

# Filtrar datos por fecha
filtered_data = get_date_filtered_data(data, start_date, end_date)
df_sales_filtered = filtered_data['fact_sales']

# Aplicar filtro de transportista si está seleccionado
if filtros_extra and filtros_extra.get('transportista') and filtros_extra['transportista'] != "Todos":
    transportista_seleccionado = filtros_extra['transportista']
    # Mapear nombre a sk_shipper
    shipper_map = {
        "Speedy Express": 1,
        "United Package": 2,
        "Federal Shipping": 3
    }
    sk_shipper = shipper_map.get(transportista_seleccionado)
    if sk_shipper and not df_sales_filtered.empty:
        df_sales_filtered = df_sales_filtered[df_sales_filtered['sk_shipper'] == sk_shipper]

# KPIs de Logística (usando datos filtrados)
kpis = get_logistica_kpis(df_sales_filtered, data['dim_shippers'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Envíos", f"{kpis.get('total_envios', 0):,}")

with col2:
    st.metric("Órdenes sin Transportista", f"{kpis.get('ordenes_sin_transportista', 0):,}")

with col3:
    st.metric("Costo Envío Promedio", f"${kpis.get('costo_envio_promedio', 0):,.2f}")

with col4:
    st.metric("Transportista Principal", kpis.get('transportista_top', 'N/A'))

# Mostrar período seleccionado
st.caption(f"📅 Datos mostrados: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")

st.markdown("---")

# Gráficos de Logística
col1, col2 = st.columns(2)

with col1:
    fig_uso_transportista = plot_uso_transportista(df_sales_filtered, data['dim_shippers'])
    if fig_uso_transportista:
        st.plotly_chart(fig_uso_transportista, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar uso por transportista en el período seleccionado")

with col2:
    fig_costos_envio = plot_costo_promedio_envio(df_sales_filtered, data['dim_shippers'])
    if fig_costos_envio:
        st.plotly_chart(fig_costos_envio, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar costos de envío en el período seleccionado")

# Alerta de órdenes sin transportista (usando datos filtrados)
ordenes_sin, detalle_sin = plot_ordenes_sin_transportista(df_sales_filtered)
if ordenes_sin > 0:
    st.error(f"⚠️ **ALERTA EN EL PERÍODO SELECCIONADO:** {ordenes_sin} órdenes necesitan asignación de transportista")
    
    with st.expander("Ver detalles de órdenes sin transportista"):
        st.dataframe(detalle_sin, use_container_width=True)
else:
    st.success(f"✅ Todas las órdenes en el período tienen transportista asignado")