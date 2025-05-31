import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Parámetros de conexión
usuario = 'root'
contraseña = ''
host = 'localhost'
puerto = '3306'
base_datos = 'superstoredb'

# Crear engine
engine = create_engine(f'mysql+mysqlconnector://{usuario}:{contraseña}@{host}:{puerto}/{base_datos}')

# Leer CSV
ruta_csv = r'C:\Users\denni\Downloads\superstore_final_dataset (1).csv'
df = pd.read_csv(ruta_csv, encoding='latin1')
df.columns = df.columns.str.strip()  # Limpiar encabezados

# Eliminar columna 'id' si existe
if 'id' in df.columns:
    df.drop(columns=['id'], inplace=True)

# Convertir fechas a formato datetime para evitar errores
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce', dayfirst=True)
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce', dayfirst=True)

# Reemplazar NaNs por None para compatibilidad con MySQL
df = df.where(pd.notnull(df), None)

batch_size = 500
try:
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch.to_sql(name='superstore_data', con=connection, if_exists='append', index=False)
                print(f"✅ Batch {i//batch_size + 1} insertado.")
            trans.commit()
            print("✅ Todos los datos han sido insertados correctamente.")
        except Exception as e:
            trans.rollback()
            print("❌ Error al insertar datos:")
            print(e)
except SQLAlchemyError as outer_error:
    print("⚠️ Error general de conexión o transacción:")
    print(outer_error)
