import pandas as pd
import matplotlib.pyplot as plt
import folium
import numpy as np

# Carregar dados
df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')

print("=== ANÁLISE ESPACIAL DOS ESTABELECIMENTOS DE SAÚDE - CONCÓRDIA/SC ===")

# Análise de distribuição geográfica
coordenadas = df[['Field39', 'Field40']].values

# Criar figura para análise espacial
plt.figure(figsize=(15, 5))

# Subplot 1: Distribuição de latitudes
plt.subplot(1, 3, 1)
plt.hist(df['Field39'], bins=10, color='lightblue', edgecolor='black')
plt.title('Distribuição - Latitude')
plt.xlabel('Latitude')
plt.ylabel('Frequência')
plt.grid(True, alpha=0.3)

# Subplot 2: Distribuição de longitudes
plt.subplot(1, 3, 2)
plt.hist(df['Field40'], bins=10, color='lightgreen', edgecolor='black')
plt.title('Distribuição - Longitude')
plt.xlabel('Longitude')
plt.grid(True, alpha=0.3)

# Subplot 3: Dispersão geográfica
plt.subplot(1, 3, 3)
cores = ['green' if 'ESF' in str(tipo) else 'blue' for tipo in df['Field7']]
plt.scatter(df['Field40'], df['Field39'], c=cores, alpha=0.7, s=60)
plt.title('Dispersão Geográfica dos Estabelecimentos')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True, alpha=0.3)

# Adicionar legenda
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', label='ESF'),
    Patch(facecolor='blue', label='PS')
]
plt.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('analise_espacial_concordia.png', dpi=300, bbox_inches='tight')
plt.show()

# Estatísticas de dispersão
print("\n" + "="*50)
print("ESTATÍSTICAS ESPACIAIS:")
print("="*50)
print(f"Total de estabelecimentos: {len(df)}")
print(f"Extensão Norte-Sul: {df['Field39'].max() - df['Field39'].min():.3f} graus")
print(f"Extensão Leste-Oeste: {df['Field40'].max() - df['Field40'].min():.3f} graus")
print(f"Coordenada mais ao Norte: {df['Field39'].max():.6f}")
print(f"Coordenada mais ao Sul: {df['Field39'].min():.6f}")
print(f"Coordenada mais a Leste: {df['Field40'].max():.6f}")
print(f"Coordenada mais a Oeste: {df['Field40'].min():.6f}")

# Calcular centro geográfico
centro_lat = df['Field39'].mean()
centro_lon = df['Field40'].mean()
print(f"Centro geográfico: [{centro_lat:.6f}, {centro_lon:.6f}]")

# Análise por tipo
esf_coords = df[df['Field7'].str.contains('ESF', na=False)][['Field39', 'Field40']]
ps_coords = df[df['Field7'].str.contains('PS', na=False)][['Field39', 'Field40']]

print(f"\nESF: {len(esf_coords)} estabelecimentos")
print(f"PS: {len(ps_coords)} estabelecimentos")

# Criar mapa interativo
print("\nCriando mapa interativo...")
mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=12)

# Adicionar limite estadual
try:
    import geopandas as gpd
    limite_estado = gpd.read_file("SC_setores_CD2022.gpkg")
    limite_estado = limite_estado.to_crs(epsg=4326)
    folium.GeoJson(
        limite_estado,
        name="Limite Estadual",
        style_function=lambda x: {
            'color': '#444',
            'weight': 1,
            'fill': True,
            'fillColor': '#444',
            'fillOpacity': 0.04
        }
    ).add_to(mapa)
except Exception as e:
    print(f"⚠️ Falha ao adicionar limite estadual: {e}")

# Configurar limites de zoom e navegação
bounds = [[df['Field39'].min(), df['Field40'].min()], [df['Field39'].max(), df['Field40'].max()]]
mapa.fit_bounds(bounds)
mapa.options['maxBounds'] = bounds
mapa.options['minZoom'] = 10
mapa.options['maxZoom'] = 16

# Adicionar marcadores para ESF (verde) e PS (azul)
for idx, row in df.iterrows():
    # Definir cor baseada no tipo
    if 'ESF' in str(row['Field7']):
        cor = 'green'
        icone = 'plus'
    elif 'PS' in str(row['Field7']):
        cor = 'blue'
        icone = 'info-sign'
    else:
        cor = 'red'
        icone = 'star'
    
    # Criar popup com informações
    popup_text = f"""
    <b>{row['Field7']}</b><br>
    <b>Endereço:</b> {row['Field8']}, {row['Field9']}<br>
    <b>Bairro:</b> {row['Field11']}<br>
    <b>CEP:</b> {row['Field12']}<br>
    <b>Tipo:</b> {row['Field7'].split()[0]}
    """
    
    folium.Marker(
        location=[row['Field39'], row['Field40']],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=row['Field7'],
        icon=folium.Icon(color=cor, icon=icone, prefix='glyphicon')
    ).add_to(mapa)

# Adicionar marcador do centro
folium.Marker(
    location=[centro_lat, centro_lon],
    popup='<b>Centro Geográfico</b><br>Média das coordenadas',
    tooltip='Centro Geográfico',
    icon=folium.Icon(color='red', icon='flag')
).add_to(mapa)

# Salvar mapa
mapa.save('mapa_estabelecimentos_concordia.html')
print("Mapa salvo como 'mapa_estabelecimentos_concordia.html'")

print("\n" + "="*50)
print("ANÁLISE CONCLUÍDA!")
print("="*50)
print("Arquivos gerados:")
print("1. analise_espacial_concordia.png - Gráficos de distribuição")
print("2. mapa_estabelecimentos_concordia.html - Mapa interativo")