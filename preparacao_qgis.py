# CÓDIGO: Exportar para Shapefile e CSV otimizado
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Carregar dados
df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')

# Criar geometria
geometry = [Point(xy) for xy in zip(df['Field40'], df['Field39'])]

# Criar GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

# Salvar como Shapefile
gdf.to_file('estabelecimentos_saude_concordia.shp', encoding='utf-8')

# Salvar como CSV com WKT para QGIS
df['WKT'] = [f"POINT ({lon} {lat})" for lon, lat in zip(df['Field40'], df['Field39'])]
df.to_csv('estabelecimentos_saude_concordia.csv', index=False, encoding='utf-8')

# Salvar como KML para visualização rápida
gdf.to_file('estabelecimentos_saude_concordia.kml', driver='KML')

print("Arquivos exportados para QGIS!")
print("✓ estabelecimentos_saude_concordia.shp")
print("✓ estabelecimentos_saude_concordia.csv") 
print("✓ estabelecimentos_saude_concordia.kml")