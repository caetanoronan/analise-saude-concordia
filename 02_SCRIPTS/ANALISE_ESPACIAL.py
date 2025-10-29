import matplotlib.pyplot as plt
import numpy as np

# Análise de distribuição geográfica
coordenadas = df[['Field39', 'Field40']].values

plt.figure(figsize=(15, 5))

# Subplot 1: Distribuição de latitudes
plt.subplot(1, 3, 1)
plt.hist(df['Field39'], bins=10, color='lightblue', edgecolor='black')
plt.title('Distribuição - Latitude')
plt.xlabel('Latitude')
plt.ylabel('Frequência')

# Subplot 2: Distribuição de longitudes
plt.subplot(1, 3, 2)
plt.hist(df['Field40'], bins=10, color='lightgreen', edgecolor='black')
plt.title('Distribuição - Longitude')
plt.xlabel('Longitude')

# Subplot 3: Dispersão geográfica
plt.subplot(1, 3, 3)
cores = ['green' if 'ESF' in tipo else 'blue' for tipo in df['Field7']]
plt.scatter(df['Field40'], df['Field39'], c=cores, alpha=0.6, s=50)
plt.title('Dispersão Geográfica')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.tight_layout()
plt.savefig('analise_espacial_concordia.png', dpi=300, bbox_inches='tight')
plt.show()

# Estatísticas de dispersão
print("\n" + "="*50)
print("ESTATÍSTICAS ESPACIAIS:")
print("="*50)
print(f"Extensão Norte-Sul: {df['Field39'].max() - df['Field39'].min():.3f} graus")
print(f"Extensão Leste-Oeste: {df['Field40'].max() - df['Field40'].min():.3f} graus")
print(f"Coordenada mais ao Norte: {df['Field39'].max():.6f}")
print(f"Coordenada mais ao Sul: {df['Field39'].min():.6f}")