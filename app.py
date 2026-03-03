import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
from utils.ui_components import hide_auto_navigation, render_sidebar

# Configuración de la página
st.set_page_config(
    page_title="Northwind Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_auto_navigation()

# Cargar datos
@st.cache_data
def load_data():
    return load_all_data('datos/')

def main():
    # Título principal
    st.title("📊 Northwind Traders - Dashboard Interactivo")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        data = load_data()
   
    render_sidebar()
    
    # Métricas generales del dashboard
    st.header("📈 Resumen Ejecutivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ventas = data['fact_sales']['line_total'].sum() if 'fact_sales' in data else 0
        st.metric("Ventas Totales", f"${total_ventas:,.0f}")
    
    with col2:
        num_clientes = data['dim_customers']['customer_id'].nunique() if 'dim_customers' in data else 0
        st.metric("Clientes Activos", num_clientes)
    
    with col3:
        num_productos = data['dim_products']['product_id'].nunique() if 'dim_products' in data else 0
        st.metric("Productos", num_productos)
    
    with col4:
        num_ordenes = data['fact_sales']['order_id'].nunique() if 'fact_sales' in data else 0
        st.metric("Órdenes Totales", num_ordenes)
    
    st.markdown("---")
    
    # Navegación a las páginas específicas
    st.header("📋 Análisis por Área")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.info("📈 **Ventas**\n\nTendencias, categorías, productos estrella y performance de vendedores.")
        st.page_link("pages/1_ventas.py", label="Ir a Ventas →")
    
    with col2:
        st.info("👥 **Clientes**\n\nAnálisis de cartera, distribución geográfica y frecuencia de compra.")
        st.page_link("pages/2_clientes.py", label="Ir a Clientes →")
    
    with col3:
        st.info("📦 **Inventario**\n\nNiveles de stock, backorders y rotación de productos.")
        st.page_link("pages/3_inventario.py", label="Ir a Inventario →")
    
    with col4:
        st.info("🛒 **Compras**\n\nAnálisis de proveedores, costos y órdenes pendientes.")
        st.page_link("pages/4_compras.py", label="Ir a Compras →")
    
    with col5:
        st.info("🚚 **Logística**\n\nTransportistas, costos de envío y órdenes sin asignar.")
        st.page_link("pages/5_logistica.py", label="Ir a Logística →")

if __name__ == "__main__":
    main()