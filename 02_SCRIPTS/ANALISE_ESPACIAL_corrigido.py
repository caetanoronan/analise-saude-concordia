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

# === CARREGAR LIMITES VIA API IBGE ===
def carregar_limites_ibge():
    """Carrega limites do IBGE com fallbacks"""
    import requests
    try:
        import geopandas as gpd
    except:
        print("⚠️ GeoPandas não disponível")
        return None, None
    
    print("📥 Carregando limites IBGE...")
    
    # URLs da API
    url_estado = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/42?formato=application/vnd.geo+json"
    url_municipio = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/420430?formato=application/vnd.geo+json"
    url_alt = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-42-mun.json"
    
    gdf_estado = None
    gdf_municipio = None
    
    try:
        # Limite estadual
        resp = requests.get(url_estado, timeout=30)
        if resp.status_code == 200:
            gdf_estado = gpd.GeoDataFrame.from_features(resp.json()['features'])
            gdf_estado.crs = "EPSG:4326"
            print("   ✅ Limite estadual carregado")
    except Exception as e:
        print(f"   ⚠️ Erro estado: {e}")
    
    try:
        # Limite municipal
        resp = requests.get(url_municipio, timeout=30)
        if resp.status_code == 200:
            gdf_municipio = gpd.GeoDataFrame.from_features(resp.json()['features'])
            gdf_municipio.crs = "EPSG:4326"
            print("   ✅ Limite municipal carregado")
        else:
            # Fallback fonte alternativa
            print(f"   → Tentando fonte alternativa...")
            resp = requests.get(url_alt, timeout=30)
            if resp.status_code == 200:
                gdf_sc = gpd.GeoDataFrame.from_features(resp.json()['features'])
                gdf_sc.crs = "EPSG:4326"
                for col in gdf_sc.columns:
                    if 'id' in col.lower() or 'cod' in col.lower():
                        gdf_municipio = gdf_sc[gdf_sc[col].astype(str).str.contains('420430', na=False)]
                        if not gdf_municipio.empty:
                            print("   ✅ Limite municipal (fonte alternativa)")
                            break
    except Exception as e:
        print(f"   ⚠️ Erro município: {e}")
    
    # Fallback arquivo local
    if gdf_municipio is None or gdf_municipio.empty:
        try:
            print("   → Tentando shapefile local...")
            gdf_municipio = gpd.read_file("Concordia_sencitario.shp")
            if gdf_municipio.crs is None or gdf_municipio.crs.to_epsg() != 4326:
                gdf_municipio = gdf_municipio.to_crs(epsg=4326)
            gdf_municipio = gdf_municipio.dissolve().reset_index(drop=True)
            print("   ✅ Limite municipal (local)")
        except Exception as e:
            print(f"   ⚠️ Arquivo local não disponível: {e}")
    
    return gdf_estado, gdf_municipio

# Carregar limites
gdf_estado, gdf_municipio = carregar_limites_ibge()

# === FILTRO ESPACIAL: Remover estabelecimentos fora do limite municipal ===
if gdf_municipio is not None and not gdf_municipio.empty:
    try:
        import geopandas as gpd
        from shapely.geometry import Point
        
        print("🔍 Aplicando filtro espacial...")
        
        # Criar GeoDataFrame com os estabelecimentos
        geometry = [Point(xy) for xy in zip(df['Field40'], df['Field39'])]
        gdf_estabelecimentos = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
        
        # Spatial join para manter apenas estabelecimentos dentro do município
        gdf_dentro = gpd.sjoin(gdf_estabelecimentos, gdf_municipio, how='inner', predicate='within')
        
        # Remover colunas duplicadas do join
        cols_to_drop = [col for col in gdf_dentro.columns if col.startswith('index_')]
        gdf_dentro = gdf_dentro.drop(columns=cols_to_drop, errors='ignore')
        
        n_original = len(df)
        n_filtrado = len(gdf_dentro)
        n_removido = n_original - n_filtrado
        
        if n_removido > 0:
            print(f"   ⚠️ {n_removido} estabelecimentos removidos (fora do limite municipal)")
            # Identificar quais foram removidos
            ids_dentro = set(gdf_dentro.index)
            ids_fora = set(df.index) - ids_dentro
            for idx in ids_fora:
                nome = df.loc[idx, 'Field7'] if idx in df.index else 'N/A'
                print(f"      ❌ {nome}")
        
        # Atualizar dataframe
        df = gdf_dentro.drop(columns=['geometry'], errors='ignore')
        print(f"   ✅ Filtro aplicado: {n_filtrado} estabelecimentos dentro do município")
        
        # Recalcular centro geográfico após filtro
        centro_lat = df['Field39'].mean()
        centro_lon = df['Field40'].mean()
        print(f"   → Novo centro geográfico: [{centro_lat:.6f}, {centro_lon:.6f}]")
        
    except Exception as e:
        print(f"   ⚠️ Erro ao aplicar filtro espacial: {e}")
        print(f"   → Continuando com todos os estabelecimentos ({len(df)})")
else:
    print("⚠️ Limite municipal não disponível, pulando filtro espacial")

# Adicionar limite estadual
if gdf_estado is not None and not gdf_estado.empty:
    folium.GeoJson(
        data=gdf_estado.__geo_interface__,
        name='Limite Estadual (SC)',
        style_function=lambda x: {
            'color': '#2c7fb8',
            'weight': 2.5,
            'fillColor': 'transparent',
            'fillOpacity': 0,
            'dashArray': '5, 5'
        },
        tooltip=folium.Tooltip('Estado de Santa Catarina'),
        popup=folium.Popup('<b>Estado de Santa Catarina</b><br>Área: ~95.730 km²<br>Fonte: IBGE', max_width=250)
    ).add_to(mapa)

# Adicionar limite municipal
if gdf_municipio is not None and not gdf_municipio.empty:
    folium.GeoJson(
        data=gdf_municipio.__geo_interface__,
        name='Limite Municipal (Concórdia)',
        style_function=lambda x: {
            'color': '#238b45',
            'weight': 3.5,
            'fillColor': '#66c2a4',
            'fillOpacity': 0.15,
            'dashArray': None
        },
        highlight_function=lambda x: {
            'weight': 5,
            'color': '#00441b',
            'fillOpacity': 0.25
        },
        tooltip=folium.Tooltip('Município de Concórdia'),
        popup=folium.Popup('<b>Município de Concórdia/SC</b><br>Código IBGE: 420430<br>Área: ~799 km²<br>Fonte: IBGE', max_width=250)
    ).add_to(mapa)

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

# === ADICIONAR TÍTULO E RODAPÉ ===
titulo_html = '''
<div style="position: fixed; 
            top: 10px; 
            left: 50%; 
            transform: translateX(-50%);
            width: auto;
            max-width: 90%;
            height: auto;
            background-color: white;
            border: 3px solid #238b45;
            border-radius: 10px;
            z-index: 9999;
            padding: 15px 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            text-align: center;
            font-family: 'Arial', sans-serif;">
    <h2 style="margin: 0; 
               padding: 0; 
               font-size: 22px; 
               font-weight: bold; 
               color: #00441b;
               line-height: 1.3;">
        🏥 ANÁLISE ESPACIAL DOS ESTABELECIMENTOS DE SAÚDE
    </h2>
    <p style="margin: 5px 0 0 0; 
              padding: 0; 
              font-size: 16px; 
              color: #238b45;
              font-weight: 600;">
        Município de Concórdia/SC
    </p>
</div>
'''

rodape_html = '''
<div style="position: fixed; 
            bottom: 10px; 
            left: 50%; 
            transform: translateX(-50%);
            width: auto;
            max-width: 95%;
            height: auto;
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #238b45;
            border-radius: 8px;
            z-index: 9999;
            padding: 10px 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            text-align: center;
            font-family: 'Arial', sans-serif;">
    <p style="margin: 0; 
              padding: 0; 
              font-size: 12px; 
              color: #333;
              line-height: 1.6;">
        <b>Fonte:</b> CNES/DataSUS | IBGE | 
        <b>Autor:</b> Ronan Armando Caetano, Graduando em Ciências Biológicas UFSC e Técnico em Geoprocessamento IFSC
    </p>
</div>
'''

mapa.get_root().html.add_child(folium.Element(titulo_html))
mapa.get_root().html.add_child(folium.Element(rodape_html))

# Salvar mapa
mapa.save('mapa_estabelecimentos_concordia.html')
print("Mapa salvo como 'mapa_estabelecimentos_concordia.html'")

print("\n" + "="*50)
print("ANÁLISE CONCLUÍDA!")
print("="*50)
print("Arquivos gerados:")
print("1. analise_espacial_concordia.png - Gráficos de distribuição")
print("2. mapa_estabelecimentos_concordia.html - Mapa interativo")