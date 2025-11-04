import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns

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

# Coordenadas aproximadas do centro de Concórdia
centro_concordia = [-27.2335, -52.0238]

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
    
    folium.Marker(
        location=[row['NU_LATITUDE'], row['NU_LONGITUDE']],
        popup=f"""
        <b>{row['NO_FANTASIA']}</b><br>
        Tipo: {row['TP_UNIDADE']}<br>
        Endereço: {row['NO_LOGRADOURO']}, {row['NU_ENDERECO']}<br>
        Bairro: {row['NO_BAIRRO']}
        """,
        tooltip=row['NO_FANTASIA'],
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

# Salvar mapa
mapa_concordia.save("mapa_unidades_saude_concordia.html")

print("\nMapa gerado: 'mapa_unidades_saude_concordia.html'")