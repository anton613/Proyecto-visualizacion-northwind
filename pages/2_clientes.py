import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, get_date_filtered_data
from utils.charts import (
    plot_distribucion_clientes_region, plot_top_clientes,
    plot_frecuencia_compra, get_clientes_kpis
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

fechas, filtros_extra = render_sidebar(page_type="clientes")
if isinstance(fechas, tuple) and len(fechas) == 2:
    start_date, end_date = fechas
else:
    start_date, end_date = pd.to_datetime('2025-01-01'), pd.to_datetime('2025-12-31')

hide_auto_navigation()

# Filtrar datos por fecha
filtered_data = get_date_filtered_data(data, start_date, end_date)
df_sales_filtered = filtered_data['fact_sales'].copy()

# APLICAR FILTROS ESPECÍFICOS
if filtros_extra and filtros_extra.get('estado_cliente') and filtros_extra['estado_cliente'] != "Todos" and not df_sales_filtered.empty:
    estado = filtros_extra['estado_cliente']
    # Este filtro se aplica en la lógica de KPIs, no aquí directamente

# KPIs de Clientes
kpis = get_clientes_kpis(df_sales_filtered, data['dim_customers'])

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
    st.info(f"🏆 **Cliente Destacado en el período:** {kpis['cliente_top']} con ${kpis.get('ventas_cliente_top', 0):,.2f} en compras")

# Mostrar período seleccionado
st.caption(f"📅 Datos mostrados: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")

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
    fig_top_clientes = plot_top_clientes(df_sales_filtered, data['dim_customers'])
    if fig_top_clientes:
        st.plotly_chart(fig_top_clientes, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar top clientes en el período seleccionado")

col1, col2 = st.columns(2)

with col1:
    fig_frecuencia = plot_frecuencia_compra(df_sales_filtered)
    if fig_frecuencia:
        st.plotly_chart(fig_frecuencia, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar frecuencia de compra en el período seleccionado")

with col2:
    # GRÁFICO IMPLEMENTADO: Clientes nuevos vs recurrentes
    if not df_sales_filtered.empty and 'date' in df_sales_filtered.columns:
        # Calcular primera compra de cada cliente (usando datos completos)
        primera_compra_total = data['fact_sales'].groupby('sk_customer')['date'].min().reset_index()
        primera_compra_total.columns = ['sk_customer', 'primera_compra']
        
        # Identificar clientes en el período filtrado
        clientes_en_periodo = df_sales_filtered['sk_customer'].unique()
        
        # Clasificar
        nuevos = []
        recurrentes = []
        
        for cliente in clientes_en_periodo:
            fecha_primera = primera_compra_total[primera_compra_total['sk_customer'] == cliente]['primera_compra'].iloc[0]
            if fecha_primera >= pd.Timestamp(start_date) and fecha_primera <= pd.Timestamp(end_date):
                nuevos.append(cliente)
            else:
                recurrentes.append(cliente)
        
        # Crear gráfico
        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Bar(name='Clientes', x=['Nuevos', 'Recurrentes'], y=[len(nuevos), len(recurrentes)], 
                   marker_color=['#2ECC71', '#3498DB'])
        ])
        fig.update_layout(
            title='Clientes Nuevos vs Recurrentes en el Período',
            yaxis_title='Número de Clientes',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar clientes nuevos vs recurrentes")