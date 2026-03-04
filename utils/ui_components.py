import streamlit as st
from datetime import date
import pandas as pd

def hide_auto_navigation():
    """CSS para ocultar la navegación automática de Streamlit"""
    st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(page_type="global", data=None):
    """Sidebar con filtros dinámicos por página"""
    
    # Definir fechas mínima y máxima
    min_date = date(2025, 1, 1)
    max_date = date(2025, 12, 31)
    
    # --- CORRECCIÓN: Inicializar date_range en session_state si no existe ---
    if 'date_range' not in st.session_state:
        st.session_state['date_range'] = (min_date, max_date)
    
    # Callback para limpiar filtros
    def clear_filters():
        # Valores por defecto según el tipo de página
        if page_type == "ventas":
            st.session_state['cat_filter'] = []
        elif page_type == "clientes":
            st.session_state['estado_cliente_filter'] = "Todos"
        elif page_type == "inventario":
            st.session_state['stock_bajo_filter'] = False
            st.session_state['mov_filter'] = "Todos"
        elif page_type == "compras":
            st.session_state['prov_filter'] = []
        elif page_type == "logistica":
            st.session_state['ship_filter'] = []
        
        # Restablecer fechas al año completo
        st.session_state['date_range'] = (min_date, max_date)
    
    with st.sidebar:
        st.title("📊 Northwind Traders")
        st.markdown("---")
        
        st.subheader("📌 Navegación")
        
        # Navegación principal

        st.page_link('app.py', label="🏠 Inicio", use_container_width=True)
        st.page_link("pages/1_ventas.py", label="📈 Ventas", use_container_width=True)
        st.page_link("pages/3_inventario.py", label="📦 Inventario", use_container_width=True)

        st.page_link("pages/2_clientes.py", label="👥 Clientes", use_container_width=True)
        st.page_link("pages/4_compras.py", label="🛒 Compras", use_container_width=True)
        st.page_link("pages/5_logistica.py", label="🚚 Logística", use_container_width=True)

        st.markdown("---")

        st.subheader("📅 Filtro de Período (2025)")
        
        # --- CORRECCIÓN: Usar el valor de session_state sin duplicar default ---
        selected_dates = st.date_input(
            "Selecciona rango de fechas",
            value=st.session_state.date_range,  # Usar el valor de session_state
            min_value=min_date,
            max_value=max_date,
            key="date_range",
            help="Solo se permiten fechas del año 2025"
        )

        st.subheader("🔍 Filtros Específicos")
        
        filtros = {}
        
        # Filtros adicionales según el área
        if page_type == "ventas" and data is not None and 'dim_products' in data:
            categorias_disponibles = data['dim_products']['category'].dropna().unique().tolist()
            # Inicializar en session_state si no existe
            if 'cat_filter' not in st.session_state:
                st.session_state['cat_filter'] = []
                
            filtros['categoria'] = st.multiselect(
                "Categoría de Producto",
                options=sorted(categorias_disponibles),
                key="cat_filter",
                help="Filtrar ventas por categoría de producto"
            )
            
        elif page_type == "clientes":
            opciones_actividad = ["Todos", "Activos", "Inactivos"]
            # Inicializar en session_state si no existe
            if 'estado_cliente_filter' not in st.session_state:
                st.session_state['estado_cliente_filter'] = "Todos"
                
            filtros['estado_cliente'] = st.selectbox(
                "Estado del Cliente",
                options=opciones_actividad,
                key="estado_cliente_filter",
                help="Filtrar por actividad de compra"
            )
            
        elif page_type == "inventario":
            # Inicializar en session_state si no existe
            if 'stock_bajo_filter' not in st.session_state:
                st.session_state['stock_bajo_filter'] = False
            if 'mov_filter' not in st.session_state:
                st.session_state['mov_filter'] = "Todos"
                
            filtros['stock_bajo'] = st.checkbox(
                "Ver solo productos con stock bajo",
                key="stock_bajo_filter",
                help="Mostrar productos con menos de 20 unidades (requiere implementación)"
            )
            filtros['tipo_movimiento'] = st.selectbox(
                "Tipo de Movimiento",
                options=["Todos", "Compras", "Ventas", "Ajustes"],
                key="mov_filter",
                help="Filtrar movimientos por tipo"
            )
            
        elif page_type == "compras" and data is not None and 'dim_suppliers' in data:
            proveedores_list = data['dim_suppliers']['company'].dropna().unique().tolist()
            # Inicializar en session_state si no existe
            if 'prov_filter' not in st.session_state:
                st.session_state['prov_filter'] = []
                
            filtros['proveedor'] = st.multiselect(
                "Proveedor(es)",
                options=sorted(proveedores_list),
                key="prov_filter",
                help="Selecciona uno o más proveedores. Vacío = Todos"
            )
            
        elif page_type == "logistica":
            transportistas_list = ["Speedy Express", "United Package", "Federal Shipping"]
            # Inicializar en session_state si no existe
            if 'ship_filter' not in st.session_state:
                st.session_state['ship_filter'] = []
                
            filtros['transportista'] = st.multiselect(
                "Transportista(s)",
                options=transportistas_list,
                key="ship_filter",
                help="Selecciona uno o más transportistas. Vacío = Todos"
            )
        
        # Botón para limpiar filtros con callback
        st.button(
            "🧹 Limpiar Filtros", 
            use_container_width=True, 
            key="clear_filters_btn",
            on_click=clear_filters,
            type="secondary"
        )
        
        st.markdown("---")
        st.caption("© 2025 - Northwind Traders Dashboard")
        st.caption(f"Página actual: {page_type.capitalize()}")
        
        return selected_dates, filtros

def plot_productos_backorder(df_inventory, df_products):
    """Productos con Backorders - Tabla + indicador"""
    if df_inventory.empty:
        return pd.DataFrame(), 0
    
    if 'is_backorder' not in df_inventory.columns:
        return pd.DataFrame(), 0
    
    backorders = df_inventory[df_inventory['is_backorder'] == True]
    productos_backorder = backorders['sk_product'].nunique()
    
    if not backorders.empty and not df_products.empty:
        backorders_detail = backorders.groupby('sk_product')['quantity'].sum().reset_index()
        backorders_detail = backorders_detail.merge(
            df_products[['sk_product', 'product_name']], 
            on='sk_product'
        )
        backorders_detail = backorders_detail.sort_values('quantity', ascending=False)
        return backorders_detail[['product_name', 'quantity']], productos_backorder
    else:
        return pd.DataFrame(), productos_backorder