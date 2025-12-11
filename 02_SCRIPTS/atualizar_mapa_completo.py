"""
Script para extrair TODOS os estabelecimentos do mapa HTML e recriar com:
- Limite Municipal (azul tracejado)
- Marcadores Vermelhos para públicos (ESF/PS)
- Marcadores Cinza para privados/outros
- Centro Urbano (preto)
- Círculos 5km (verde) e 10km (laranja)
- Limites de zoom
"""

import re
import json
import folium
import os
from math import radians, cos, sin, asin, sqrt

# Configurações
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRO_CONCORDIA = [-27.2335, -52.0238]

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula distância Haversine"""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def eh_publico(nome, tipo):
    """Verifica se é estabelecimento público"""
    nome_upper = str(nome).upper()
    tipo_str = str(tipo)
    
    # ESFs e Postos de Saúde são públicos
    criterios = [
        'ESF' in nome_upper,
        'PS ' in nome_upper,
        'POSTO' in nome_upper,
        'UBS' in nome_upper,
        'CENTRO DE SAUDE' in nome_upper,
        tipo_str in ['1', '2', '4', '70', '81', '68']  # Tipos públicos do CNES
    ]
    
    return any(criterios)

def extrair_dados_html():
    """Extrai dados do mapa HTML existente"""
    print("📥 Extraindo dados do mapa HTML...")
    
    html_path = os.path.join(ROOT_DIR, '03_RESULTADOS', 'mapas', 'mapa_concordia_analise.html')
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar o array de unidades
    match = re.search(r'var unidades = (\[.*?\]);', content, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        # Limpar para JSON válido
        json_str = json_str.replace("'", '"')
        unidades = json.loads(json_str)
        print(f"✅ {len(unidades)} estabelecimentos extraídos")
        return unidades
    
    print("❌ Não foi possível extrair dados")
    return []

def carregar_limite_municipal():
    """Carrega polígono do limite municipal"""
    try:
        import geopandas as gpd
        
        shp_path = os.path.join(ROOT_DIR, '03_RESULTADOS', 'shapefiles', 'Concordia_sencitario.shp')
        
        if os.path.exists(shp_path):
            gdf = gpd.read_file(shp_path)
            if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)
            return gdf
    except:
        pass
    
    return None

def filtrar_estabelecimentos_dentro_limite(unidades, gdf_municipio):
    """Filtra apenas estabelecimentos dentro do limite municipal"""
    if gdf_municipio is None or gdf_municipio.empty:
        print("⚠️ Limite municipal não disponível, retornando todos os estabelecimentos")
        return unidades
    
    try:
        from shapely.geometry import Point
        import geopandas as gpd
        
        print("\n🔍 Aplicando filtro espacial...")
        print(f"   → Total antes do filtro: {len(unidades)} estabelecimentos")
        
        # Criar lista de estabelecimentos dentro do limite
        unidades_filtradas = []
        removidos = []
        
        # Pegar o polígono do município (união de todas as geometrias)
        poligono_municipio = gdf_municipio.unary_union
        
        for unidade in unidades:
            ponto = Point(unidade['lon'], unidade['lat'])
            
            if poligono_municipio.contains(ponto):
                unidades_filtradas.append(unidade)
            else:
                removidos.append(unidade)
        
        print(f"   ✅ Dentro do município: {len(unidades_filtradas)} estabelecimentos")
        print(f"   ❌ Removidos (fora do limite): {len(removidos)} estabelecimentos")
        
        if removidos:
            print(f"\n   📋 Estabelecimentos removidos (fora de Concórdia):")
            for est in removidos[:10]:  # Mostrar até 10
                dist = calcular_distancia(CENTRO_CONCORDIA[0], CENTRO_CONCORDIA[1], est['lat'], est['lon'])
                print(f"      • {est['nome'][:50]:50s} | {dist:6.2f} km | {est.get('bairro', 'N/D')}")
            if len(removidos) > 10:
                print(f"      ... e mais {len(removidos) - 10} estabelecimentos")
        
        return unidades_filtradas
        
    except Exception as e:
        print(f"⚠️ Erro ao filtrar: {e}")
        print("   → Retornando todos os estabelecimentos")
        return unidades

def criar_mapa_completo(unidades, gdf_municipio):
    """Cria mapa com TODOS os estabelecimentos"""
    print("\n🗺️ Criando mapa completo...")
    
    # Criar mapa com limites de zoom
    mapa = folium.Map(
        location=CENTRO_CONCORDIA,
        zoom_start=12,
        min_zoom=10,      # Limite expansão
        max_zoom=18,      # Limite aproximação  
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # 1. Limite Municipal (azul tracejado)
    if gdf_municipio is not None and not gdf_municipio.empty:
        folium.GeoJson(
            data=gdf_municipio.__geo_interface__,
            name='🔵 Limite Municipal - Concórdia/SC',
            style_function=lambda x: {
                'color': '#0066cc',
                'weight': 3,
                'fillColor': '#cce5ff',
                'fillOpacity': 0.1,
                'dashArray': '10, 5'
            },
            tooltip='Limite Municipal de Concórdia',
            popup=folium.Popup('<b>Município de Concórdia/SC</b><br>Código IBGE: 420430', max_width=250)
        ).add_to(mapa)
    
    # 2. Círculos de análise
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=5000,
        color='#228b22',
        fillColor='#90ee90',
        fillOpacity=0.15,
        weight=2,
        dashArray='5, 3',
        popup='<b>Raio: 5 km</b><br>Área urbana central',
        tooltip='Raio 5km - Zona Urbana'
    ).add_to(mapa)
    
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=10000,
        color='#ff8c00',
        fillColor='#ffa500',
        fillOpacity=0.1,
        weight=2,
        dashArray='5, 3',
        popup='<b>Raio: 10 km</b><br>Área periurbana',
        tooltip='Raio 10km - Zona Periurbana'
    ).add_to(mapa)
    
    # 3. Centro Urbano (preto)
    folium.Marker(
        location=CENTRO_CONCORDIA,
        popup=folium.Popup(
            f'<b>🏛️ Centro Urbano de Concórdia</b><br>Coordenadas: {CENTRO_CONCORDIA[0]:.6f}, {CENTRO_CONCORDIA[1]:.6f}',
            max_width=300
        ),
        tooltip='Centro Urbano (Referência)',
        icon=folium.Icon(color='black', icon='home', prefix='glyphicon')
    ).add_to(mapa)
    
    # 4. Estabelecimentos
    count_publicos = 0
    count_outros = 0
    
    for unidade in unidades:
        nome = unidade['nome']
        lat = unidade['lat']
        lon = unidade['lon']
        endereco = unidade.get('endereco', 'N/D')
        bairro = unidade.get('bairro', 'N/D')
        tipo = unidade.get('tipo', '')
        
        # Calcular distância
        distancia = calcular_distancia(CENTRO_CONCORDIA[0], CENTRO_CONCORDIA[1], lat, lon)
        
        # Classificar estabelecimento
        publico = eh_publico(nome, tipo)
        
        if publico:
            cor = 'red'
            icone = 'plus'
            categoria = 'PÚBLICO'
            count_publicos += 1
        else:
            cor = 'lightgray'
            icone = 'info-sign'
            categoria = 'Privado/Outros'
            count_outros += 1
        
        # Classificar por distância
        if distancia <= 5:
            zona = 'Urbana (< 5km)'
        elif distancia <= 10:
            zona = 'Periurbana (5-10km)'
        else:
            zona = 'Rural (> 10km)'
        
        # Criar popup
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: {'#cc0000' if publico else '#666'};">{nome}</h4>
            <table style="font-size: 12px;">
                <tr><td><b>Categoria:</b></td><td style="color: {'#cc0000' if publico else '#666'};"><b>{categoria}</b></td></tr>
                <tr><td><b>Tipo:</b></td><td>{tipo}</td></tr>
                <tr><td><b>Endereço:</b></td><td>{endereco}</td></tr>
                <tr><td><b>Bairro:</b></td><td>{bairro}</td></tr>
                <tr><td><b>Distância:</b></td><td>{distancia:.2f} km</td></tr>
                <tr><td><b>Zona:</b></td><td>{zona}</td></tr>
            </table>
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{nome} ({categoria})",
            icon=folium.Icon(color=cor, icon=icone, prefix='glyphicon')
        ).add_to(mapa)
    
    print(f"   ✅ {count_publicos} estabelecimentos públicos (vermelho)")
    print(f"   ✅ {count_outros} outros estabelecimentos (cinza)")
    
    # Título
    titulo_html = '''
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: rgba(255, 255, 255, 0.95);
                padding: 15px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 9999;
                text-align: center;
                max-width: 90%;
                border-left: 5px solid #0066cc;">
        <h2 style="margin: 0; color: #0066cc; font-size: 22px; font-weight: 600;">
            🏥 Estabelecimentos de Saúde - Concórdia/SC (Filtrado)
        </h2>
        <p style="margin: 5px 0 0 0; color: #666; font-size: 13px;">
            Análise Espacial com Limite Municipal e Raios de Cobertura
        </p>
    </div>
    '''
    
    # Rodapé
    rodape_html = '''
    <div style="position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%;
                background: linear-gradient(to top, rgba(0, 102, 204, 0.92), rgba(0, 102, 204, 0.85));
                padding: 12px 20px;
                z-index: 9999;
                text-align: center;
                border-top: 3px solid #004080;">
        <div style="color: white; font-size: 13px; line-height: 1.6;">
            <strong>📊 Fontes:</strong> CNES/DataSUS | IBGE | Município de Concórdia
            <span style="margin: 0 15px;">|</span>
            <strong>👨‍🎓 Autor:</strong> Ronan Armando Caetano • 
            Graduando em Ciências Biológicas UFSC • 
            Técnico em Geoprocessamento IFSC
        </div>
    </div>
    '''
    
    # Legenda
    legenda_html = '''
    <div style="position: fixed; 
                top: 120px; 
                right: 10px; 
                width: 220px;
                background-color: white;
                border: 2px solid #0066cc;
                border-radius: 8px;
                z-index: 9998;
                padding: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                font-size: 12px;">
        <h4 style="margin: 0 0 10px 0; color: #0066cc; font-size: 14px; border-bottom: 2px solid #0066cc; padding-bottom: 5px;">
            📍 Legenda
        </h4>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: #cc0000; border-radius: 50%; margin-right: 8px;"></span>
            <b>Estabelecimento Público</b> (ESF/PS)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: #d3d3d3; border-radius: 50%; margin-right: 8px;"></span>
            Outros Estabelecimentos
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: #000; border-radius: 50%; margin-right: 8px;"></span>
            Centro Urbano
        </div>
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 20px; height: 2px; background-color: #228b22; margin-right: 8px; border: 1px dashed #228b22;"></span>
            Raio 5 km (Urbano)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 20px; height: 2px; background-color: #ff8c00; margin-right: 8px; border: 1px dashed #ff8c00;"></span>
            Raio 10 km (Periurbano)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; width: 20px; height: 2px; background-color: #0066cc; margin-right: 8px; border: 2px dashed #0066cc;"></span>
            Limite Municipal
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    mapa.get_root().html.add_child(folium.Element(rodape_html))
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    folium.LayerControl(collapsed=False, position='topleft').add_to(mapa)
    
    return mapa

def main():
    print("="*60)
    print("🗺️ CRIAÇÃO DO MAPA COMPLETO DE UNIDADES DE SAÚDE")
    print("="*60)
    
    # 1. Extrair dados
    unidades = extrair_dados_html()
    
    if not unidades:
        print("❌ Falha ao extrair dados")
        return
    
    # 2. Carregar limite
    gdf_municipio = carregar_limite_municipal()
    
    # 3. Filtrar estabelecimentos dentro do limite municipal
    unidades_filtradas = filtrar_estabelecimentos_dentro_limite(unidades, gdf_municipio)
    
    # 4. Criar mapa
    mapa = criar_mapa_completo(unidades_filtradas, gdf_municipio)
    
    # 4. Salvar
    output_path = os.path.join(ROOT_DIR, 'docs', 'mapa_unidades_saude_concordia.html')
    mapa.save(output_path)
    
    print(f"\n✅ Mapa salvo em:\n   {output_path}")
    print("\n" + "="*60)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📌 Características aplicadas:")
    print("   ✓ Limite Municipal: Polígono azul tracejado")
    print("   ✓ Marcadores Vermelhos: Estabelecimentos públicos (ESF/PS)")
    print("   ✓ Marcadores Cinza: Outros estabelecimentos")
    print("   ✓ Centro Urbano: Marcador preto")
    print("   ✓ Círculos: 5km (verde) e 10km (laranja)")
    print("   ✓ Limites de Zoom: min=10, max=18")
    print("   ✓ Título, Rodapé e Legenda profissionais")

if __name__ == '__main__':
    main()
