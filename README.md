# 📊 Northwind Traders - Dashboard Interactivo

Dashboard interactivo de análisis de datos de Northwind Traders desarrollado con Streamlit.

## 🔗 Proyecto Base

Este proyecto es la continuación de [proyecto-northwind](https://github.com/anton613/proyecto-northwind), donde se realizó el análisis y modelado de datos de la base de datos Northwind.

## 🌐 Demo en Vivo

Puedes probar el dashboard desplegado en:
**[https://proyecto-visualizacion-northwind-casani.streamlit.app/](https://proyecto-visualizacion-northwind-casani.streamlit.app/)**

## 📋 Descripción

Este proyecto implementa un dashboard completo para visualizar y analizar los datos de Northwind Traders, una empresa ficticia de comercio de alimentos. El dashboard permite explorar diferentes aspectos del negocio a través de visualizaciones interactivas y métricas clave.

## ✨ Características

El dashboard incluye las siguientes secciones de análisis:

- **📈 Ventas**: Análisis de tendencias, categorías, productos estrella y performance de vendedores
- **👥 Clientes**: Análisis de cartera, distribución geográfica y frecuencia de compra
- **📦 Inventario**: Niveles de stock, backorders y rotación de productos
- **🛒 Compras**: Análisis de proveedores, costos y órdenes pendientes
- **🚚 Logística**: Análisis de transportistas, costos de envío y órdenes sin asignar

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Streamlit**: Framework principal para el dashboard
- **Pandas**: Manipulación y análisis de datos
- **Plotly**: Visualizaciones interactivas
- **Altair**: Gráficos estadísticos

## 📦 Requisitos

- Python 3.8 o superior
- pip o uv (gestor de paquetes)

## 🚀 Instalación

### Opción 1: Usando pip

1. Clona el repositorio:
```bash
git clone https://github.com/[tu-usuario]/Proyecto-visualizacion-northwind.git
cd Proyecto-visualizacion-northwind
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
   - **Windows (PowerShell)**:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   - **Windows (CMD)**:
   ```cmd
   .venv\Scripts\activate.bat
   ```
   - **Linux/Mac**:
   ```bash
   source .venv/bin/activate
   ```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Opción 2: Usando uv

1. Clona el repositorio:
```bash
git clone https://github.com/[tu-usuario]/Proyecto-visualizacion-northwind.git
cd Proyecto-visualizacion-northwind
```

2. Instala las dependencias con uv:
```bash
uv sync
```

## ▶️ Uso

1. Asegúrate de que el entorno virtual esté activado

2. Ejecuta la aplicación:
```bash
streamlit run app.py
```

3. Abre tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
Proyecto-visualizacion-northwind/
├── app.py                 # Aplicación principal
├── pages/                 # Páginas del dashboard
│   ├── 1_ventas.py
│   ├── 2_clientes.py
│   ├── 3_inventario.py
│   ├── 4_compras.py
│   └── 5_logistica.py
├── utils/                 # Módulos utilitarios
│   ├── __init__.py
│   ├── charts.py         # Funciones para gráficos
│   ├── data_loader.py    # Carga de datos
│   └── ui_components.py  # Componentes de UI
├── consultas solo BD/     # Consultas SQL equivalentes sobre la BD operacional
│   ├── Consultas para la pag Ventas.sql
│   ├── Consultas para la pag Clientes.sql
│   ├── Consultas para la pag Inventario.sql
│   ├── Consultas para la pag Compras.sql
│   └── Consultas para la pag Logistica.sql
├── datos/                 # Archivos de datos (modelo dimensional)
├── .streamlit/           # Configuración de Streamlit
│   └── config.toml
├── requirements.txt      # Dependencias del proyecto
├── pyproject.toml        # Configuración del proyecto
└── README.md
```

## 📊 Datos

Los datos utilizados provienen del proyecto base de análisis Northwind y están almacenados en la carpeta `datos/`. El dashboard carga automáticamente estos datos al iniciar.

## 🔍 Consultas SQL sobre la BD Operacional (Northwind Original)

En la carpeta `consultas solo BD/` se incluyen las consultas SQL equivalentes que obtienen los mismos resultados directamente desde la **base de datos operacional (transaccional)** de Northwind. Esto permite comparar ambos enfoques de análisis:

### Enfoque Analítico (Este Dashboard)
- Utiliza un **modelo dimensional** (estrella) con tablas de hechos (`fact_sales`, `fact_purchases`, `fact_inventory_movements`) y dimensiones (`dim_customers`, `dim_products`, `dim_employees`, etc.).
- Los datos fueron previamente transformados (ETL) y se cargan desde archivos CSV.
- Las operaciones de análisis se realizan con **Python (Pandas)**: joins, agrupaciones, cálculos de métricas y KPIs se ejecutan en memoria.
- Optimizado para **consultas de lectura y análisis** de grandes volúmenes de datos.

### Enfoque Operacional (Consultas SQL Directas)
- Las consultas se ejecutan sobre el **esquema transaccional original** de Northwind (`orders`, `order_details`, `products`, `customers`, etc.).
- Requiere múltiples `JOIN` entre tablas normalizadas para obtener la información consolidada.
- Diseñado para soportar las **operaciones del día a día** (insertar pedidos, actualizar inventario, registrar clientes).
- Las consultas analíticas son más complejas y costosas al ejecutarse sobre un modelo no optimizado para análisis.

### Archivos de Consultas SQL

```
consultas solo BD/
├── Consultas para la pag Ventas.sql       # KPIs, tendencias, categorías, top productos, ventas por empleado/estado
├── Consultas para la pag Clientes.sql     # Cartera, distribución geográfica, frecuencia, clientes nuevos vs recurrentes
├── Consultas para la pag Inventario.sql   # Stock por categoría, backorders, rotación, entradas vs salidas
├── Consultas para la pag Compras.sql      # Costos, proveedores, tendencias, órdenes pendientes
└── Consultas para la pag Logistica.sql    # Transportistas, costos de envío, órdenes sin asignar
```

> **Nota**: Estas consultas están escritas en SQL (compatible con MySQL) y sirven como referencia comparativa. Demuestran cómo las mismas preguntas de negocio se resuelven de forma diferente según el modelo de datos utilizado.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir:

1. Haz fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Proyecto desarrollado como continuación del análisis de datos Northwind.

---

**Nota**: Este dashboard está desplegado y disponible públicamente en Streamlit Cloud para pruebas y demostración.