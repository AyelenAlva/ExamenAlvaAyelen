import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
# 1. Importación del Dataset
df = pd.read_csv('C:/Users/ayeal/OneDrive/Documentos/Examen_Alva_Ayelen/votaciones.csv')
# 2. Exploración Inicial de los Datos
print("Primeras filas:")
print(df.head())

print("\nÚltimas filas:")
print(df.tail())

print("\nInformación general:")
print(df.info())

print("\nConteo de valores nulos por columna:")
print(df.isnull().sum())

# 3. Limpieza y Normalización de los Datos

# 3.1 Eliminar filas con demasiados nulos (más de 3 nulos por fila)
df = df[df.isnull().sum(axis=1) <= 3]

# Rellenar valores faltantes
df['nombre'] = df['nombre'].fillna(df['nombre'].mode()[0])
df['apellido'] = df['apellido'].fillna(df['apellido'].mode()[0])
df['dni'] = df['dni'].fillna(df['dni'].median())
df['provincia'] = df['provincia'].fillna(df['provincia'].mode()[0])
df['voto'] = df['voto'].fillna(df['voto'].mode()[0])
df['fecha_votacion'] = df['fecha_votacion'].fillna(df['fecha_votacion'].mode()[0])

# 3.2 Convertir fecha a tipo datetime
#df['fecha_votacion'] = pd.to_datetime(df['fecha_votacion'], errors='coerce', dayfirst=True)

# 3.3 Corregir mayúsculas en nombre y apellido
df['nombre'] = df['nombre'].str.title()
df['apellido'] = df['apellido'].str.title()

# 3.4 Convertir votos a mayúsculas
df['voto'] = df['voto'].str.upper()

# 3.5 Asegurar que DNI sea tipo int
df['dni'] = df['dni'].astype(int)

print("\n[OK] Limpieza y normalización completadas.")

# 4. Obtención de Estadísticas Descriptivas

# 4.1 Estadísticas generales
print("\nEstadísticas descriptivas generales:")
print(df.describe())

# 4.2 Estadísticas específicas por grupo (provincia y voto)
print("\nEstadísticas por grupo (provincia, voto):")
print(df.groupby(['provincia', 'voto'])['dni'].count())

# 5. Visualización de los Datos con Matplotlib

# Ejemplo: Gráfico de barras - cantidad de votos por provincia
votos_por_provincia = df['provincia'].value_counts()
votos_por_provincia.plot(kind='bar', figsize=(10,6))
plt.title('Cantidad de votos por provincia')
plt.xlabel('Provincia')
plt.ylabel('Cantidad de votos')
plt.tight_layout()
plt.show()

# 6. Exportación a Archivo SQLite

# Crear conexión
conn = sqlite3.connect('votaciones.db')

# Exportar DataFrame a SQLite
df.to_sql('votaciones', conn, if_exists='replace', index=False)

# Verificar cargado
query = pd.read_sql('SELECT * FROM votaciones LIMIT 5', conn)
print("\nConsulta de verificación en SQLite:")
print(query)

# Cerrar conexión
conn.close()

print("\n[OK] Exportación a SQLite completada.")
