import streamlit as st
from utils.data_loader import load_all_data
from utils.charts import (
    plot_stock_por_categoria, plot_productos_backorder,
    plot_rotacion_inventario, plot_movimientos_inventario,
    get_inventario_kpis
)
from utils.ui_components import hide_auto_navigation, render_sidebar

st.set_page_config(page_title="Inventario - Northwind", page_icon="📦", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

data = load_data()

st.title("📦 Análisis de Inventario")
st.markdown("---")

hide_auto_navigation()
render_sidebar()

# KPIs de Inventario
kpis = get_inventario_kpis(data['fact_inventory'], data['dim_products'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Productos", f"{kpis.get('total_productos', 0):,}")

with col2:
    st.metric("Productos con Backorder", f"{kpis.get('productos_backorder', 0):,}")

with col3:
    st.metric("Total Transacciones", f"{kpis.get('total_transacciones', 0):,}")

with col4:
    ratio = kpis.get('ratio_entradas_salidas', 0)
    st.metric("Ratio Entradas/Salidas", f"{ratio:.2f}")

st.markdown("---")

# Gráficos de Inventario
col1, col2 = st.columns(2)

with col1:
    fig_stock_categoria = plot_stock_por_categoria(data['fact_inventory'], data['dim_products'])
    if fig_stock_categoria:
        st.plotly_chart(fig_stock_categoria, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar stock por categoría")

with col2:
    backorders_df, num_backorders = plot_productos_backorder(data['fact_inventory'], data['dim_products'])
    if not backorders_df.empty:
        st.subheader(f"📋 Productos con Backorder ({num_backorders})")
        st.dataframe(backorders_df, use_container_width=True)
    else:
        st.info("No hay productos con backorder")

col1, col2 = st.columns(2)

with col1:
    fig_rotacion = plot_rotacion_inventario(data['fact_sales'], data['fact_inventory'], data['dim_products'])
    if fig_rotacion:
        st.plotly_chart(fig_rotacion, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar rotación de inventario")

with col2:
    fig_movimientos = plot_movimientos_inventario(data['fact_inventory'])
    if fig_movimientos:
        st.plotly_chart(fig_movimientos, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar movimientos de inventario")