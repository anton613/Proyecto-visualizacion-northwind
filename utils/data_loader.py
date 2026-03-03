import pandas as pd
import os

def load_all_data(data_path='datos/'):
    """
    Carga todos los archivos CSV del directorio datos/
    """
    data = {}
    
    # Mapeo de archivos a nombres descriptivos
    files = {
        'dim_customers.csv': 'dim_customers',
        'dim_date.csv': 'dim_date',
        'dim_employees.csv': 'dim_employees',
        'dim_products.csv': 'dim_products',
        'dim_shippers.csv': 'dim_shippers',
        'dim_suppliers.csv': 'dim_suppliers',
        'fact_inventory_movements.csv': 'fact_inventory',
        'fact_purchases.csv': 'fact_purchases',
        'fact_sales.csv': 'fact_sales'
    }
    
    for filename, key in files.items():
        filepath = os.path.join(data_path, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                data[key] = df
                print(f"✅ Cargado: {filename} - {len(df)} registros")
            except Exception as e:
                print(f"❌ Error cargando {filename}: {e}")
                data[key] = pd.DataFrame()
        else:
            print(f"⚠️ Archivo no encontrado: {filepath}")
            data[key] = pd.DataFrame()
    
    # Procesar fechas en fact_sales si existe
    if 'fact_sales' in data and not data['fact_sales'].empty:
        data['fact_sales']['date'] = pd.to_datetime(
            data['fact_sales']['sk_date'].astype(str), 
            format='%Y%m%d', 
            errors='coerce'
        )
        data['fact_sales']['year_month'] = data['fact_sales']['date'].dt.to_period('M')
    
    # Procesar fechas en fact_purchases
    if 'fact_purchases' in data and not data['fact_purchases'].empty and 'sk_date' in data['fact_purchases'].columns:
        data['fact_purchases']['date'] = pd.to_datetime(
            data['fact_purchases']['sk_date'].astype(str), 
            format='%Y%m%d', 
            errors='coerce'
        )
    
    return data

def get_date_filtered_data(data, start_date, end_date):
    """
    Filtra los datos por rango de fechas
    """
    filtered_data = {}
    
    for key, df in data.items():
        if 'date' in df.columns:
            filtered_data[key] = df[
                (df['date'] >= pd.Timestamp(start_date)) & 
                (df['date'] <= pd.Timestamp(end_date))
            ]
        else:
            filtered_data[key] = df.copy()
    
    return filtered_data