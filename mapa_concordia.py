import folium
import pandas as pd

# Carregar dados
df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')

# Criar mapa centrado em Concórdia
centro_lat = df['Field39'].mean()
centro_lon = df['Field40'].mean()

mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=12)

# Cores para diferentes tipos
def cor_tipo(tipo):
    if 'ESF' in tipo:
        return 'green'
    elif 'PS' in tipo:
        return 'blue'
    else:
        return 'red'

# Adicionar marcadores
for idx, row in df.iterrows():
    popup_text = f"""
    <b>{row['Field7']}</b><br>
    <b>Endereço:</b> {row['Field8']}, {row['Field9']}<br>
    <b>Bairro:</b> {row['Field11']}<br>
    <b>CEP:</b> {row['Field12']}<br>
    <b>Tipo:</b> {row['Field7']}
    """
    
    folium.Marker(
        location=[row['Field39'], row['Field40']],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=row['Field7'],
        icon=folium.Icon(color=cor_tipo(row['Field7']), icon='plus')
    ).add_to(mapa)

# Salvar mapa
mapa.save('mapa_estabelecimentos_concordia.html')
print("Mapa salvo como 'mapa_estabelecimentos_concordia.html'")