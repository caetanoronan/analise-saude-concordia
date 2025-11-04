import geopandas as gpd

# Carregar municípios de SC
gdf = gpd.read_file('SC_Municipios_2024/SC_Municipios_2024.shp')

# Filtrar Concórdia
concordia = gdf[gdf['CD_MUN'] == '420430']

print(f'Concórdia encontrada: {not concordia.empty}')
if not concordia.empty:
    print(concordia[['CD_MUN', 'NM_MUN', 'AREA_KM2']])
    
    # Salvar limite de Concórdia
    concordia.to_file('Concordia_municipio_limpo.shp')
    print('✅ Limite de Concórdia salvo')

# Filtrar municípios vizinhos (num raio aproximado)
centro_concordia = (-27.2335, -52.0238)
from shapely.geometry import Point
ponto_centro = Point(centro_concordia[1], centro_concordia[0])

# Municípios num raio de ~50km
gdf_4326 = gdf.to_crs(epsg=4326)
distancias = gdf_4326.geometry.distance(ponto_centro)
vizinhos = gdf_4326[distancias < 0.5]  # ~50km em graus decimais

print(f'\n{len(vizinhos)} municípios próximos encontrados:')
print(vizinhos[['NM_MUN', 'AREA_KM2']])

vizinhos.to_file('SC_municipios_regiao_concordia.shp')
print('✅ Municípios da região salvos')
