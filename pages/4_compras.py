import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, get_date_filtered_data
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

fechas, filtros_extra = render_sidebar(page_type="compras", data=data)
if isinstance(fechas, tuple) and len(fechas) == 2:
    start_date, end_date = fechas
else:
    start_date, end_date = pd.to_datetime('2025-01-01'), pd.to_datetime('2025-12-31')

hide_auto_navigation()

# Filtrar datos por fecha
filtered_data = get_date_filtered_data(data, start_date, end_date)
df_purchases_filtered = filtered_data['fact_purchases'].copy()

# Verificar si hay datos después del filtro de fecha
if df_purchases_filtered.empty:
    st.warning("⚠️ No hay datos de compras en el período seleccionado")
    df_purchases_filtered = pd.DataFrame()

# APLICAR FILTROS DE PROVEEDOR MULTISELECT
if filtros_extra and filtros_extra.get('proveedor') and not df_purchases_filtered.empty:
    proveedores_seleccionados = filtros_extra['proveedor']
    if proveedores_seleccionados:
        proveedores_info = data['dim_suppliers'][data['dim_suppliers']['company'].isin(proveedores_seleccionados)]
        if not proveedores_info.empty:
            sk_proveedores_filtrados = proveedores_info['sk_supplier'].unique()
            df_purchases_filtered = df_purchases_filtered[df_purchases_filtered['sk_supplier'].isin(sk_proveedores_filtrados)]
            if df_purchases_filtered.empty:
                st.info(f"ℹ️ No hay compras de los proveedores seleccionados en el período")

# KPIs de Compras (ahora con función mejorada)
kpis = get_compras_kpis(df_purchases_filtered)

# --- MEJORA: KPIs más relevantes y organizados ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Comprado", 
        f"${kpis.get('total_comprado', 0):,.0f}",
        help="Suma total de todas las compras en el período"
    )

with col2:
    st.metric(
        "Órdenes de Compra", 
        f"{kpis.get('total_ordenes_compra', 0):,}",
        help="Número de órdenes de compra en el período"
    )

with col3:
    st.metric(
        "Costo Promedio por Orden", 
        f"${kpis.get('costo_promedio_orden', 0):,.2f}",
        help="Valor promedio de cada orden de compra"
    )

with col4:
    st.metric(
        "Proveedores Activos", 
        f"{kpis.get('proveedores_activos', 0):,}",
        help="Número de proveedores distintos en el período"
    )

# Segunda fila de KPIs (opcional, puedes ponerlos en expander)
with st.expander("📊 Métricas adicionales de compras", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Unidades Compradas", f"{kpis.get('unidades_totales', 0):,.0f}")
    
    with col2:
        st.metric("Costo Promedio por Unidad", f"${kpis.get('costo_promedio_unidad', 0):,.2f}")
    
    with col3:
        if 'orden_maxima' in kpis:
            st.metric("Orden Más Grande", f"${kpis['orden_maxima']:,.0f} (ID: {kpis['orden_maxima_id']})")

# Mostrar período seleccionado y filtros
st.caption(f"📅 Datos mostrados: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")
if filtros_extra and filtros_extra.get('proveedor'):
    if filtros_extra['proveedor']:
        st.caption(f"🏢 Proveedor(es) seleccionado(s): {', '.join(filtros_extra['proveedor'])}")
    else:
        st.caption(f"🏢 Proveedor(es): Todos")

st.markdown("---")

# Gráficos de Compras
col1, col2 = st.columns(2)

with col1:
    # --- AHORA EL GRÁFICO USA EL MISMO CÁLCULO QUE LOS KPIs ---
    fig_compras_proveedor = plot_compras_por_proveedor(df_purchases_filtered, data['dim_suppliers'])
    if fig_compras_proveedor:
        st.plotly_chart(fig_compras_proveedor, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar compras por proveedor en el período seleccionado")

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
        st.metric("Tiempo Promedio de Recepción (histórico)", f"{promedio_dias:.1f} días")
    else:
        st.info("No hay datos suficientes para mostrar tiempo de recepción")

with col2:
    pendientes_df, num_pendientes = plot_ordenes_pendientes(data['fact_purchases'])
    if not pendientes_df.empty:
        st.subheader(f"📋 Órdenes Pendientes de Recibir ({num_pendientes})")
        st.dataframe(pendientes_df, use_container_width=True)
    else:
        st.info("No hay órdenes pendientes de recibir")