# Análise estatística da distribuição
print("\n=== ANÁLISE DA DISTRIBUIÇÃO EM CONCÓRDIA ===")
print(f"Total de unidades mapeadas: {len(df_geo)}")

# Contagem por tipo de unidade
print("\nDistribuição por tipo de unidade:")
tipo_contagem = df_geo['TP_UNIDADE'].value_counts()
for tipo, count in tipo_contagem.items():
    print(f"Tipo {tipo}: {count} unidades")

# Análise de coordenadas
print(f"\nCoordenadas extremas:")
print(f"Latitude: {df_geo['NU_LATITUDE'].min():.4f} a {df_geo['NU_LATITUDE'].max():.4f}")
print(f"Longitude: {df_geo['NU_LONGITUDE'].min():.4f} a {df_geo['NU_LONGITUDE'].max():.4f}")

# Calcular distâncias aproximadas do centro
from math import radians, sin, cos, sqrt, atan2

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Calcular distâncias do centro
distancias = []
for idx, row in df_geo.iterrows():
    dist = calcular_distancia(centro_concordia[0], centro_concordia[1], 
                            row['NU_LATITUDE'], row['NU_LONGITUDE'])
    distancias.append(dist)

print(f"\nDistância média do centro: {sum(distancias)/len(distancias):.2f} km")
print(f"Unidade mais próxima do centro: {min(distancias):.2f} km")
print(f"Unidade mais distante do centro: {max(distancias):.2f} km")

# Identificar unidades em raio de 5km do centro
unidades_proximas = sum(1 for d in distancias if d <= 5)
print(f"\nUnidades dentro de 5km do centro: {unidades_proximas}/{len(distancias)}")