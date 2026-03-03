import streamlit as st

def hide_auto_navigation():
    """CSS para ocultar la navegación automática de Streamlit"""
    st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] { display: none !important; }
        [data-testid="stSidebarHeader"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Sidebar personalizado compartido entre todas las páginas"""
    with st.sidebar:
        st.title("📊 Northwind Traders")
        st.markdown("---")
        
        st.subheader("Navegación")
        st.page_link('app.py', label="🏠 Inicio", use_container_width=True)
        st.page_link("pages/1_ventas.py", label="📈 Ventas", use_container_width=True)
        st.page_link("pages/2_clientes.py", label="👥 Clientes", use_container_width=True)
        st.page_link("pages/3_inventario.py", label="📦 Inventario", use_container_width=True)
        st.page_link("pages/4_compras.py", label="🛒 Compras", use_container_width=True)
        st.page_link("pages/5_logistica.py", label="🚚 Logística", use_container_width=True)
        
        st.markdown("---")