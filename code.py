# Cargar el nuevo archivo
file_path = "/mnt/data/Crime_Incidents_in_2025.csv"
df = pd.read_csv(file_path)

# Filtrar columnas necesarias
df_filtered = df[['SHIFT', 'METHOD', 'DISTRICT']].dropna()

# Calcular incidentes por distrito
incidents_per_district = df_filtered.groupby('DISTRICT').size().reset_index(name='incidents')

# Crear población simulada por distrito (ejemplo)
unique_districts = sorted(df_filtered['DISTRICT'].dropna().unique())
fake_population = {
    d: pop for d, pop in zip(unique_districts, 
                             [90000, 85000, 87000, 91000, 88000, 92000, 89500])
}

# Añadir población y calcular tasa por 10,000 hab.
incidents_per_district['population'] = incidents_per_district['DISTRICT'].map(fake_population)
incidents_per_district['incidents_per_10k'] = (
    incidents_per_district['incidents'] / incidents_per_district['population'] * 10000
)

# Agrupar por SHIFT y DISTRICT
combined = df_filtered.groupby(['SHIFT', 'DISTRICT']).size().reset_index(name='count')
combined = combined.merge(incidents_per_district[['DISTRICT', 'population']], on='DISTRICT')
combined['normalized'] = combined['count'] / combined['population'] * 10000

# Tabla para heatmap
pivot_normalized = combined.pivot_table(index='SHIFT', columns='DISTRICT', values='normalized', fill_value=0)

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_normalized, annot=True, fmt=".1f", cmap="Reds")
plt.title("Incidentes por Turno y Distrito (Normalizados por Población)")
plt.ylabel("Turno (SHIFT)")
plt.xlabel("Distrito")
plt.tight_layout()
plt.show()
