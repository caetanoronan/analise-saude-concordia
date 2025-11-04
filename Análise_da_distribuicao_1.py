import pandas as pd
import folium
from folium.plugins import HeatMap
from math import radians, sin, cos, sqrt, atan2

# Carregar os dados
df = pd.read_csv('Tabela_estado_SC.csv', sep=';', encoding='utf-8', low_memory=False)

# Filtrar apenas Concórdia (código IBGE 420430)
df_concordia = df[df['CO_MUNICIPIO_GESTOR'] == 420430]

print(f"Total de unidades em Concórdia: {len(df_concordia)}")

# Filtrar unidades com coordenadas válidas
df_geo = df_concordia.dropna(subset=['NU_LATITUDE', 'NU_LONGITUDE'])
print(f"Unidades com coordenadas válidas: {len(df_geo)}")

# Mostrar as unidades encontradas
print("\nUnidades de saúde em Concórdia:")
for idx, row in df_geo.iterrows():
    print(f"- {row['NO_FANTASIA']} | {row['TP_UNIDADE']} | Lat: {row['NU_LATITUDE']}, Lon: {row['NU_LONGITUDE']}")

# Função para calcular distância
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ANÁLISE DA DISTRIBUIÇÃO EM CONCÓRDIA
print("\n" + "="*50)
print("ANÁLISE DA DISTRIBUIÇÃO EM CONCÓRDIA")
print("="*50)

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

# Centro de Concórdia
centro_concordia = [-27.2335, -52.0238]

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

# Análise por bairros
print(f"\nBairros com unidades de saúde:")
bairros_contagem = df_geo['NO_BAIRRO'].value_counts()
for bairro, count in bairros_contagem.head(10).items():  # Top 10 bairros
    print(f"- {bairro}: {count} unidades")

# CRIAR MAPA
print("\nCriando mapa...")

# Criar mapa focado em Concórdia
mapa_concordia = folium.Map(location=centro_concordia, zoom_start=13)

# Adicionar marcadores coloridos por tipo de unidade
cores = {
    '1': 'green',    # Posto de Saúde
    '2': 'blue',     # Centro de Saúde
    '4': 'red',      # Policlínica
    '5': 'orange',   # Hospital
    '7': 'purple',   # Unidade Mista
    '22': 'lightblue' # Consultório
}

for idx, row in df_geo.iterrows():
    tipo_unidade = str(row['TP_UNIDADE'])
    cor = cores.get(tipo_unidade, 'gray')
    
    # Calcular distância do centro
    dist_centro = calcular_distancia(centro_concordia[0], centro_concordia[1], 
                                   row['NU_LATITUDE'], row['NU_LONGITUDE'])
    
    folium.Marker(
        location=[row['NU_LATITUDE'], row['NU_LONGITUDE']],
        popup=f"""
        <b>{row['NO_FANTASIA']}</b><br>
        Tipo: {row['TP_UNIDADE']}<br>
        Endereço: {row['NO_LOGRADOURO']}, {row['NU_ENDERECO']}<br>
        Bairro: {row['NO_BAIRRO']}<br>
        Distância do centro: {dist_centro:.1f} km
        """,
        tooltip=f"{row['NO_FANTASIA']} ({dist_centro:.1f} km)",
        icon=folium.Icon(color=cor, icon='plus')
    ).add_to(mapa_concordia)

# Adicionar mapa de calor
heat_data = [[row['NU_LATITUDE'], row['NU_LONGITUDE']] for idx, row in df_geo.iterrows()]
HeatMap(heat_data, radius=20, blur=15, max_zoom=13).add_to(mapa_concordia)

# Adicionar marcador do centro da cidade
folium.Marker(
    centro_concordia,
    popup='<b>Centro de Concórdia</b>',
    tooltip='Centro',
    icon=folium.Icon(color='black', icon='star')
).add_to(mapa_concordia)

# Adicionar círculo de 5km do centro
folium.Circle(
    centro_concordia,
    radius=5000,  # 5km em metros
    color='red',
    fill=True,
    fill_opacity=0.2,
    popup='Raio de 5km do centro'
).add_to(mapa_concordia)

# Salvar mapa
mapa_concordia.save("mapa_unidades_saude_concordia_detalhado.html")

print("\nMapa gerado: 'mapa_unidades_saude_concordia_detalhado.html'")
print("\nAnálise concluída!")