import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, get_date_filtered_data
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

# --- MODIFICADO: Pasar data a render_sidebar ---
fechas, filtros_extra = render_sidebar(page_type="inventario", data=data)
if isinstance(fechas, tuple) and len(fechas) == 2:
    start_date, end_date = fechas
else:
    start_date, end_date = pd.to_datetime('2025-01-01'), pd.to_datetime('2025-12-31')

hide_auto_navigation()

# --- LÓGICA MEJORADA: Separar datos para stock (completo) y actividad (filtrado) ---
filtered_data = get_date_filtered_data(data, start_date, end_date)
df_inventory_filtered = filtered_data['fact_inventory'].copy()
df_sales_filtered = filtered_data['fact_sales'].copy()

# Datos completos (para stock y backorders)
df_inventory_full = data['fact_inventory'].copy()

# Verificar si hay datos después del filtro de fecha
if df_inventory_filtered.empty:
    st.warning("⚠️ No hay datos de movimientos de inventario en el período seleccionado. Mostrando datos históricos para stock.")
    # No vaciamos df_inventory_filtered, solo mostramos la advertencia.

# APLICAR FILTROS ESPECÍFICOS (sobre los datos filtrados por fecha)
if filtros_extra and not df_inventory_filtered.empty:
    stock_bajo_activo = filtros_extra.get('stock_bajo', False) # Esto se manejará en el gráfico, no aquí.
    
    tipo_movimiento = filtros_extra.get('tipo_movimiento', "Todos")
    if tipo_movimiento != "Todos":
        if tipo_movimiento == "Compras":
            df_inventory_filtered = df_inventory_filtered[df_inventory_filtered['transaction_type'] == 'Purchased']
        elif tipo_movimiento == "Ventas":
            df_inventory_filtered = df_inventory_filtered[df_inventory_filtered['transaction_type'] == 'Sold']
        elif tipo_movimiento == "Ajustes":
            df_inventory_filtered = df_inventory_filtered[df_inventory_filtered['transaction_type'] == 'On Hold']

# KPIs de Inventario (Usamos datos filtrados para los KPIs de transacciones)
kpis = get_inventario_kpis(df_inventory_filtered, data['dim_products'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Productos", f"{kpis.get('total_productos', 0):,}")

with col2:
    # Productos con backorder (usamos datos completos para este KPI)
    _, num_backorders = plot_productos_backorder(df_inventory_full, data['dim_products'])
    st.metric("Productos con Backorder (Histórico)", f"{num_backorders:,}")

with col3:
    st.metric("Total Transacciones", f"{kpis.get('total_transacciones', 0):,}")

with col4:
    ratio = kpis.get('ratio_entradas_salidas', 0)
    st.metric("Ratio Entradas/Salidas", f"{ratio:.2f}")

# Mostrar período seleccionado y filtros
st.caption(f"📅 Datos mostrados (movimientos): {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")
if filtros_extra:
    if filtros_extra.get('stock_bajo'):
        st.caption("📉 (Pendiente) Mostrando solo productos con stock bajo")
    if filtros_extra.get('tipo_movimiento') and filtros_extra['tipo_movimiento'] != "Todos":
        st.caption(f"📊 Tipo de movimiento: {filtros_extra['tipo_movimiento']}")

st.markdown("---")
st.subheader("📊 Estado Actual del Inventario (Datos Históricos Completos)")

# Gráficos de Inventario (ESTADO)
col1, col2 = st.columns(2)

with col1:
    # GRÁFICO DE STOCK POR CATEGORÍA - Usamos datos COMPLETOS
    fig_stock_categoria = plot_stock_por_categoria(df_inventory_full, data['dim_products'])
    if fig_stock_categoria:
        st.plotly_chart(fig_stock_categoria, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar stock por categoría")

with col2:
    # PRODUCTOS BACKORDER - Usamos datos COMPLETOS
    backorders_df, num_backorders = plot_productos_backorder(df_inventory_full, data['dim_products'])
    if not backorders_df.empty:
        st.subheader(f"📋 Productos con Backorder (Histórico)")
        st.dataframe(backorders_df, use_container_width=True)
    else:
        st.info("No hay productos con backorder en el histórico")

st.markdown("---")
st.subheader(f"📈 Actividad de Inventario ({start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')})")

# Gráficos de Inventario (ACTIVIDAD)
col1, col2 = st.columns(2)

with col1:
    # ROTACIÓN - Usamos datos FILTRADOS (ventas y compras en el período)
    fig_rotacion = plot_rotacion_inventario(df_sales_filtered, df_inventory_filtered, data['dim_products'])
    if fig_rotacion:
        st.plotly_chart(fig_rotacion, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar rotación de inventario en el período seleccionado")

with col2:
    # MOVIMIENTOS - Usamos datos FILTRADOS (excluyendo 'On Hold' dentro del filtro)
    fig_movimientos = plot_movimientos_inventario(df_inventory_filtered)
    if fig_movimientos:
        st.plotly_chart(fig_movimientos, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar movimientos de inventario en el período seleccionado")