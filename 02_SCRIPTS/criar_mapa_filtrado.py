"""
Script para atualizar mapas HTML com estabelecimentos filtrados (apenas dentro de Concórdia).
Remove estabelecimentos fora do limite municipal e adiciona camada do polígono municipal.

Autor: Ronan Armando Caetano
Data: Novembro 2025
Instituição: UFSC
"""

import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import os

# Diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def criar_mapa_filtrado():
    """
    Cria mapas atualizados com apenas estabelecimentos dentro do limite municipal.
    """
    print("🗺️  Carregando dados filtrados...")
    
    # Caminhos
    arquivo_filtrado = os.path.join(ROOT_DIR, '01_DADOS', 'processados', 'concordia_saude_filtrado.csv')
    shapefile_municipios = os.path.join(ROOT_DIR, 'SC_Municipios_2024', 'SC_Municipios_2024.shp')
    
    # Carregar dados filtrados
    df = pd.read_csv(arquivo_filtrado)
    print(f"✅ {len(df)} estabelecimentos carregados")
    
    # Carregar limite municipal
    municipios_gdf = gpd.read_file(shapefile_municipios)
    concordia_gdf = municipios_gdf[municipios_gdf['CD_MUN'].astype(str).str.contains('420430')]
    concordia_gdf = concordia_gdf.to_crs('EPSG:4326')  # Converter para WGS84
    
    print(f"✅ Limite municipal de Concórdia carregado")
    
    # Centro do mapa (coordenadas de Concórdia)
    centro_lat = -27.2335
    centro_lon = -52.0238
    
    # Criar mapa base
    print("\n🎨 Criando mapa atualizado...")
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=11,
            min_zoom=10,      # Limite de zoom expansão
            max_zoom=18,      # Limite de zoom aproximação
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Adicionar limite municipal como camada
    folium.GeoJson(
        concordia_gdf,
        name='Limite Municipal de Concórdia',
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#2c5aa0',
            'weight': 3,
            'dashArray': '5, 5',
            'fillOpacity': 0.1
        },
        tooltip='Limite Municipal de Concórdia/SC'
    ).add_to(mapa)
    
    # Adicionar marcador do centro
    folium.Marker(
        location=[centro_lat, centro_lon],
        popup='<b>Centro de Concórdia</b><br>Referência geográfica',
        icon=folium.Icon(color='black', icon='info-sign'),
        tooltip='Centro Urbano'
    ).add_to(mapa)
    
    # Separar estabelecimentos públicos e privados
    def eh_publico(row):
        nome = str(row['NOME']).upper()
        tipo = str(row['TIPO']).upper()
        return 'ESF' in nome or 'PS ' in nome or tipo in ['ESF', 'PS']
    
    df['PUBLICO'] = df.apply(eh_publico, axis=1)
    
    publicos = df[df['PUBLICO'] == True]
    privados = df[df['PUBLICO'] == False]
    
    print(f"   📍 {len(publicos)} estabelecimentos públicos")
    print(f"   📍 {len(privados)} estabelecimentos privados")
    
    # Adicionar marcadores de estabelecimentos públicos
    for idx, row in publicos.iterrows():
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px;">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">🏥 {row['NOME']}</h4>
            <p style="margin: 5px 0;"><b>Tipo:</b> {row['TIPO']}</p>
            <p style="margin: 5px 0;"><b>Endereço:</b> {row['ENDERECO']}</p>
            <p style="margin: 5px 0;"><b>Bairro:</b> {row['BAIRRO']}</p>
            <p style="margin: 5px 0;"><b>CEP:</b> {row['CEP']}</p>
            <p style="margin: 5px 0;"><b>Coordenadas:</b> {row['LAT']:.6f}, {row['LON']:.6f}</p>
            <p style="margin: 5px 0; color: #d32f2f;"><b>✅ PÚBLICO</b></p>
        </div>
        """
        
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='red', icon='plus-sign', prefix='glyphicon'),
            tooltip=row['NOME']
        ).add_to(mapa)
    
    # Adicionar marcadores de estabelecimentos privados
    for idx, row in privados.iterrows():
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px;">
            <h4 style="color: #1976d2; margin: 0 0 10px 0;">🏥 {row['NOME']}</h4>
            <p style="margin: 5px 0;"><b>Tipo:</b> {row['TIPO']}</p>
            <p style="margin: 5px 0;"><b>Endereço:</b> {row['ENDERECO']}</p>
            <p style="margin: 5px 0;"><b>Bairro:</b> {row['BAIRRO']}</p>
            <p style="margin: 5px 0;"><b>CEP:</b> {row['CEP']}</p>
            <p style="margin: 5px 0;"><b>Coordenadas:</b> {row['LAT']:.6f}, {row['LON']:.6f}</p>
            <p style="margin: 5px 0; color: #1976d2;"><b>🔵 PRIVADO</b></p>
        </div>
        """
        
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='blue', icon='home', prefix='glyphicon'),
            tooltip=row['NOME']
        ).add_to(mapa)
    
    # Adicionar círculos de referência (5km, 10km)
    folium.Circle(
        location=[centro_lat, centro_lon],
        radius=5000,
        color='green',
        fill=True,
        fillOpacity=0.1,
        popup='Raio de 5 km',
        tooltip='Área Urbana (5 km)'
    ).add_to(mapa)
    
    folium.Circle(
        location=[centro_lat, centro_lon],
        radius=10000,
        color='orange',
        fill=True,
        fillOpacity=0.1,
        popup='Raio de 10 km',
        tooltip='Área Periurbana (10 km)'
    ).add_to(mapa)
    
    # Adicionar controle de camadas
    folium.LayerControl(collapsed=False, position='topleft').add_to(mapa)
    
    # Adicionar título
    titulo_html = """
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: rgba(255, 255, 255, 0.95);
                padding: 15px 30px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                z-index: 9999;
                text-align: center;
                max-width: 90%;
                border-left: 5px solid #2c5aa0;">
        <h2 style="margin: 0; 
                   color: #2c5aa0; 
                   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                   font-size: 22px;
                   font-weight: 600;">
            🏥 Estabelecimentos de Saúde - Concórdia/SC (Filtrado)
        </h2>
        <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
            ✅ Apenas estabelecimentos dentro do limite municipal
        </p>
    </div>
    """
    
    # Adicionar rodapé
    rodape_html = """
    <div style="position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%;
                background: linear-gradient(to top, rgba(44, 90, 160, 0.92), rgba(44, 90, 160, 0.85));
                padding: 12px 20px;
                z-index: 9999;
                text-align: center;
                border-top: 3px solid #1e3a5f;
                box-shadow: 0 -4px 12px rgba(0,0,0,0.3);">
        <div style="color: white; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 13px;
                    line-height: 1.6;">
            <strong>📊 Fonte:</strong> CNES/DataSUS | IBGE | 
            <strong>👨‍🎓 Autor:</strong> Ronan Armando Caetano, UFSC/IFSC
        </div>
    </div>
    """
    
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    mapa.get_root().html.add_child(folium.Element(rodape_html))
    
    # === ROSA DOS VENTOS ===
    rosa_ventos_html = '''
    <div id="rosa-ventos-unica" style="
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 75px;
        height: 75px;
        z-index: 10001;
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #2c5aa0;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;">
        <svg width="70" height="70" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="48" fill="white" stroke="#2c5aa0" stroke-width="2"/>
            <!-- Seta Norte (Vermelha) -->
            <path d="M 50 10 L 55 40 L 50 35 L 45 40 Z" fill="#cc0000"/>
            <!-- Seta Sul -->
            <path d="M 50 90 L 55 60 L 50 65 L 45 60 Z" fill="#666"/>
            <!-- Seta Leste -->
            <path d="M 90 50 L 60 55 L 65 50 L 60 45 Z" fill="#666"/>
            <!-- Seta Oeste -->
            <path d="M 10 50 L 40 55 L 35 50 L 40 45 Z" fill="#666"/>
            <!-- Letras -->
            <text x="50" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#cc0000">N</text>
            <text x="50" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">S</text>
            <text x="85" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">L</text>
            <text x="15" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">O</text>
        </svg>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(rosa_ventos_html))
    
    # Salvar mapa
    # Salvar em docs/ (para GitHub Pages)
    arquivo_saida = os.path.join(ROOT_DIR, 'docs', 'mapa_estabelecimentos_filtrado.html')
    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    mapa.save(arquivo_saida)
    
    print(f"\n✅ Mapa atualizado salvo em: {arquivo_saida}")
    print(f"   Total de estabelecimentos: {len(df)}")
    print(f"   Públicos: {len(publicos)} | Privados: {len(privados)}")
    
    return mapa

if __name__ == "__main__":
    print("=" * 80)
    print("🗺️  CRIAR MAPA COM ESTABELECIMENTOS FILTRADOS")
    print("=" * 80)
    print()
    
    try:
        mapa = criar_mapa_filtrado()
        
        print()
        print("=" * 80)
        print("✨ Mapa criado com sucesso!")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
