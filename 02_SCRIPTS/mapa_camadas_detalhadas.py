"""
Mapa Interativo com Camadas Separadas por Tipo de Estabelecimento
- Farmácias, Consultórios, Clínicas, Laboratórios, Hospitais, etc.
- Controle de camadas (LayerControl) para mostrar/ocultar cada tipo
"""

import pandas as pd
import folium
from folium import plugins
import os
try:
    import geopandas as gpd
    from shapely.ops import voronoi_diagram
    from shapely.geometry import MultiPoint, Point
    GEOPANDAS_DISPONIVEL = True
except ImportError:
    GEOPANDAS_DISPONIVEL = False
    print("⚠️ GeoPandas não disponível - Voronoi desabilitado")

# Configurações
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRO_CONCORDIA = [-27.2335, -52.0238]

def carregar_dados():
    """Carrega TODOS os estabelecimentos do Excel"""
    print("📂 Carregando base completa (418 estabelecimentos)...")
    
    df = pd.read_excel(os.path.join(ROOT_DIR, 'Tabela_estado_SC.xlsx'))
    df_conc = df[df['CO_MUNICIPIO_GESTOR'] == 420430].copy()
    
    # Padronizar colunas
    df_conc = df_conc.rename(columns={
        'NO_FANTASIA': 'NOME',
        'NO_LOGRADOURO': 'ENDERECO',
        'NO_BAIRRO': 'BAIRRO',
        'CO_CEP': 'CEP',
        'NU_LATITUDE': 'LAT',
        'NU_LONGITUDE': 'LON',
        'TP_UNIDADE': 'TIPO_UNIDADE',
        'NO_RAZAO_SOCIAL': 'RAZAO_SOCIAL'
    })
    
    # Converter coordenadas
    df_conc['LAT'] = pd.to_numeric(df_conc['LAT'], errors='coerce')
    df_conc['LON'] = pd.to_numeric(df_conc['LON'], errors='coerce')
    df_conc = df_conc.dropna(subset=['LAT', 'LON'])
    
    print(f"   → {len(df_conc)} estabelecimentos antes do filtro espacial")
    
    # === FILTRO ESPACIAL RIGOROSO (REMOVER ESTABELECIMENTOS FORA DO MUNICÍPIO) ===
    try:
        import geopandas as gpd
        
        # Converter para GeoDataFrame
        df_geo = gpd.GeoDataFrame(
            df_conc,
            geometry=gpd.points_from_xy(df_conc['LON'], df_conc['LAT']),
            crs='EPSG:4326'
        )
        
        # Carregar shapefile do município
        shp_path = os.path.join(ROOT_DIR, 'SC_Municipios_2024', 'SC_Municipios_2024.shp')
        if os.path.exists(shp_path):
            shp_municipio = gpd.read_file(shp_path)
            if shp_municipio.crs != 'EPSG:4326':
                shp_municipio = shp_municipio.to_crs('EPSG:4326')
            
            # Filtrar apenas Concórdia
            for col in shp_municipio.columns:
                if 'CD_MUN' in str(col).upper() or 'GEOCODIGO' in str(col).upper():
                    shp_municipio = shp_municipio[shp_municipio[col].astype(str).str.contains('420430|4204301')]
                    break
            
            if not shp_municipio.empty:
                # Aplicar filtro espacial: apenas estabelecimentos DENTRO do município
                df_dentro = gpd.sjoin(df_geo, shp_municipio, how='inner', predicate='within')
                
                # Identificar estabelecimentos removidos
                ids_removidos = set(df_geo.index) - set(df_dentro.index)
                if ids_removidos:
                    print(f"   ⚠️ {len(ids_removidos)} estabelecimentos FORA do município (removidos):")
                    for idx in list(ids_removidos)[:10]:  # Mostrar até 10
                        nome = df_geo.loc[idx, 'NOME'] if 'NOME' in df_geo.columns else 'N/D'
                        lat = df_geo.loc[idx, 'LAT']
                        lon = df_geo.loc[idx, 'LON']
                        print(f"      • {nome} ({lat:.6f}, {lon:.6f})")
                    if len(ids_removidos) > 10:
                        print(f"      ... e mais {len(ids_removidos) - 10} estabelecimentos")
                
                # Converter de volta para DataFrame
                df_conc = pd.DataFrame(df_dentro.drop(columns='geometry'))
                df_conc = df_conc.reset_index(drop=True)
                
                print(f"   ✅ Filtro espacial aplicado: {len(df_conc)} estabelecimentos DENTRO do município")
        else:
            print("   ⚠️ Shapefile não encontrado, usando filtro básico")
            # Fallback: filtro por coordenadas
            df_conc = df_conc[
                (df_conc['LAT'] >= -27.5) & (df_conc['LAT'] <= -27.0) &
                (df_conc['LON'] >= -52.3) & (df_conc['LON'] <= -51.8)
            ]
            print(f"   ✅ {len(df_conc)} estabelecimentos (filtro por coordenadas)")
    
    except Exception as e:
        print(f"   ⚠️ Erro no filtro espacial: {e}")
        # Fallback: filtro por coordenadas
        df_conc = df_conc[
            (df_conc['LAT'] >= -27.5) & (df_conc['LAT'] <= -27.0) &
            (df_conc['LON'] >= -52.3) & (df_conc['LON'] <= -51.8)
        ]
        print(f"   ✅ {len(df_conc)} estabelecimentos (filtro básico)")
    
    return df_conc

def classificar_estabelecimento(tipo_unidade, nome):
    """
    Classifica estabelecimento por categoria detalhada
    Retorna: (categoria, cor, ícone, descrição)
    """
    tipo = str(tipo_unidade)
    nome_upper = str(nome).upper()
    
    # === PÚBLICOS ===
    if tipo in ['1', '2', '4', '70', '81']:
        if tipo == '2':
            return ('🏥 Públicos - ESF', 'red', 'plus', 'ESF - Estratégia Saúde da Família')
        elif tipo == '1':
            return ('🏥 Públicos - Postos', 'red', 'plus', 'Posto de Saúde')
        elif tipo == '4':
            return ('🏥 Públicos - Policlínicas', 'red', 'plus', 'Policlínica')
        elif tipo == '70':
            return ('🏥 Públicos - Centros de Saúde', 'red', 'plus', 'Centro de Saúde')
        else:
            return ('🏥 Públicos - Outros', 'red', 'plus', 'Unidade Pública')
    
    # === FARMÁCIAS ===
    elif tipo == '43' or 'FARMACIA' in nome_upper:
        return ('💊 Farmácias', 'green', 'shopping-cart', 'Farmácia')
    
    # === CONSULTÓRIOS ===
    elif tipo == '22':
        if 'ODONTO' in nome_upper or 'DENT' in nome_upper:
            return ('🦷 Consultórios - Odontologia', 'lightblue', 'heart', 'Consultório Odontológico')
        else:
            return ('🩺 Consultórios - Médicos', 'blue', 'user', 'Consultório Médico')
    
    # === CLÍNICAS ESPECIALIZADAS ===
    elif tipo == '36':
        return ('🏨 Clínicas Especializadas', 'purple', 'briefcase', 'Clínica Especializada')
    
    # === LABORATÓRIOS ===
    elif tipo == '39':
        if 'PROTESE' in nome_upper or 'DENT' in nome_upper:
            return ('🔬 Laboratórios - Prótese Dentária', 'orange', 'flask', 'Laboratório de Prótese Dentária')
        else:
            return ('🔬 Laboratórios - Análises', 'orange', 'flask', 'Laboratório de Análises')
    
    # === HOSPITAIS ===
    elif tipo in ['5', '62']:
        return ('🏥 Hospitais', 'pink', 'home', 'Hospital')
    
    # === EMERGÊNCIA (SAMU, Bombeiros) ===
    elif tipo == '42':
        return ('🚑 Emergência', 'darkred', 'flash', 'SAMU/Bombeiros')
    
    # === GESTÃO E OUTROS ===
    else:
        return ('🏢 Gestão/Outros', 'gray', 'cog', 'Gestão/Outros')

def criar_mapa_camadas(df):
    """Cria mapa com camadas separadas por tipo"""
    print("\n🗺️ Criando mapa com camadas detalhadas...")
    
    # Mapa base
    mapa = folium.Map(
        location=CENTRO_CONCORDIA,
        zoom_start=12,
        max_zoom=18,
        min_zoom=10,
        tiles='OpenStreetMap'
    )
    
    # === ADICIONAR DIAGRAMA DE VORONOI ===
    if GEOPANDAS_DISPONIVEL:
        try:
            import geopandas as gpd
            from shapely.ops import voronoi_diagram
            from shapely.geometry import MultiPoint
            
            print("   → Criando diagrama de Voronoi...")
            
            # Criar GeoDataFrame com pontos dos estabelecimentos
            gdf_pontos = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df['LON'], df['LAT']),
                crs='EPSG:4326'
            )
            
            # Reprojetar para UTM (melhor para cálculos de distância)
            gdf_utm = gdf_pontos.to_crs('EPSG:31982')  # SIRGAS 2000 UTM 22S
            
            # Criar MultiPoint com todos os pontos
            multipoint = MultiPoint(list(gdf_utm.geometry))
            
            # Gerar diagrama de Voronoi
            voronoi = voronoi_diagram(multipoint)
            
            # Converter para GeoDataFrame
            voronoi_polys = []
            for geom in voronoi.geoms:
                voronoi_polys.append(geom)
            
            gdf_voronoi = gpd.GeoDataFrame(geometry=voronoi_polys, crs='EPSG:31982')
            
            # Carregar limite municipal para cortar Voronoi
            shp_path = os.path.join(ROOT_DIR, 'SC_Municipios_2024', 'SC_Municipios_2024.shp')
            if os.path.exists(shp_path):
                shp_municipio = gpd.read_file(shp_path)
                shp_municipio = shp_municipio.to_crs('EPSG:31982')
                
                # Filtrar Concórdia
                for col in shp_municipio.columns:
                    if 'CD_MUN' in str(col).upper():
                        shp_municipio = shp_municipio[shp_municipio[col].astype(str).str.contains('420430')]
                        break
                
                if not shp_municipio.empty:
                    # Cortar Voronoi pelo limite municipal
                    gdf_voronoi = gpd.overlay(gdf_voronoi, shp_municipio, how='intersection')
            
            # Simplificar geometria (reduz tamanho do arquivo)
            gdf_voronoi['geometry'] = gdf_voronoi.geometry.simplify(100)  # 100 metros
            
            # Voltar para WGS84
            gdf_voronoi = gdf_voronoi.to_crs('EPSG:4326')
            
            # Criar camada Voronoi COLORIDA
            camada_voronoi = folium.FeatureGroup(name='📐 Diagrama de Voronoi (Áreas de Influência)', show=False)
            
            # Paleta de cores para os polígonos
            cores_voronoi = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                            '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#52BE80']
            
            for idx, (_, row) in enumerate(gdf_voronoi.iterrows()):
                cor = cores_voronoi[idx % len(cores_voronoi)]
                folium.GeoJson(
                    row.geometry,
                    style_function=lambda x, c=cor: {
                        'fillColor': c,
                        'color': '#9400D3',  # Borda roxa
                        'weight': 1.5,
                        'fillOpacity': 0.3,
                        'opacity': 0.7
                    },
                    tooltip=f'Área de Influência {idx + 1}'
                ).add_to(camada_voronoi)
            
            camada_voronoi.add_to(mapa)
            print(f"   ✓ Diagrama de Voronoi criado ({len(gdf_voronoi)} polígonos)")
        
        except Exception as e:
            print(f"   ⚠️ Erro ao criar Voronoi: {e}")
    
    # === ADICIONAR SETORES CENSITÁRIOS (SUBDIVISÕES) ===
    if GEOPANDAS_DISPONIVEL:
        try:
            import geopandas as gpd
            
            # Tentar carregar setores censitários
            shp_setores = os.path.join(ROOT_DIR, 'Concordia_sencitario.shp')
            if not os.path.exists(shp_setores):
                shp_setores = os.path.join(ROOT_DIR, '03_RESULTADOS', 'shapefiles', 'Concordia_sencitario.shp')
            
            if os.path.exists(shp_setores):
                print("   → Carregando setores censitários (subdivisões)...")
                gdf_setores = gpd.read_file(shp_setores)
                
                if gdf_setores.crs != 'EPSG:4326':
                    gdf_setores = gdf_setores.to_crs('EPSG:4326')
                
                # Simplificar geometria
                gdf_setores['geometry'] = gdf_setores.geometry.simplify(0.0001)
                
                # Criar camada de setores
                camada_setores = folium.FeatureGroup(name='🗺️ Setores Censitários (Subdivisões)', show=False)
                
                folium.GeoJson(
                    gdf_setores.geometry,
                    style_function=lambda x: {
                        'fillColor': 'transparent',
                        'color': '#FF6347',  # Vermelho tomate
                        'weight': 1,
                        'dashArray': '3, 3',
                        'fillOpacity': 0,
                        'opacity': 0.6
                    },
                    tooltip='Setor Censitário'
                ).add_to(camada_setores)
                
                camada_setores.add_to(mapa)
                print(f"   ✓ Setores censitários adicionados ({len(gdf_setores)} setores)")
        
        except Exception as e:
            print(f"   ⚠️ Setores censitários não carregados: {e}")
    
    # === ADICIONAR LIMITE MUNICIPAL ===
    try:
        import geopandas as gpd
        shp_path = os.path.join(ROOT_DIR, 'SC_Municipios_2024', 'SC_Municipios_2024.shp')
        if os.path.exists(shp_path):
            gdf = gpd.read_file(shp_path)
            gdf = gdf.to_crs('EPSG:4326')
            
            # Filtrar Concórdia
            for col in gdf.columns:
                if 'CD_MUN' in str(col).upper():
                    gdf = gdf[gdf[col].astype(str).str.contains('420430')]
                    break
            
            if not gdf.empty:
                folium.GeoJson(
                    gdf.geometry,
                    name='🗺️ Limite Municipal',
                    style_function=lambda x: {
                        'fillColor': 'transparent',
                        'color': '#0066cc',
                        'weight': 3,
                        'dashArray': '10, 5',
                        'fillOpacity': 0
                    }
                ).add_to(mapa)
                print("   ✓ Limite municipal adicionado")
    except Exception as e:
        print(f"   ⚠️ Limite municipal não carregado: {e}")
    
    # === CÍRCULOS DE ANÁLISE ===
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=5000,
        color='#228b22',
        fillColor='#90ee90',
        fillOpacity=0.1,
        weight=2,
        dashArray='5, 3',
        name='📏 Raio 5km',
        popup='Raio 5km - Zona Urbana'
    ).add_to(mapa)
    
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=10000,
        color='#ff8c00',
        fillColor='#ffa500',
        fillOpacity=0.05,
        weight=2,
        dashArray='5, 3',
        name='📏 Raio 10km',
        popup='Raio 10km - Zona Periurbana'
    ).add_to(mapa)
    
    # === CENTRO URBANO ===
    folium.Marker(
        location=CENTRO_CONCORDIA,
        popup='<b>Centro Urbano</b><br>Ponto de Referência',
        tooltip='Centro Urbano',
        icon=folium.Icon(color='black', icon='home', prefix='glyphicon')
    ).add_to(mapa)
    
    # === CRIAR FEATURE GROUPS PARA CADA CATEGORIA ===
    grupos = {}
    contadores = {}
    count_publicos = 0
    count_privados = 0
    
    for idx, row in df.iterrows():
        categoria, cor, icone, descricao = classificar_estabelecimento(
            row['TIPO_UNIDADE'], 
            row.get('NOME', '')
        )
        
        # Contar públicos vs privados
        if 'Públicos' in categoria:
            count_publicos += 1
        else:
            count_privados += 1
        
        # Criar grupo se não existir
        if categoria not in grupos:
            grupos[categoria] = folium.FeatureGroup(name=categoria)
            contadores[categoria] = 0
        
        contadores[categoria] += 1
        
        # Criar popup
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: {cor};">
                {row.get('NOME', 'N/D')}
            </h4>
            <table style="font-size: 12px;">
                <tr><td><b>Tipo:</b></td><td>{descricao}</td></tr>
                <tr><td><b>Endereço:</b></td><td>{row.get('ENDERECO', 'N/D')}</td></tr>
                <tr><td><b>Bairro:</b></td><td>{row.get('BAIRRO', 'N/D')}</td></tr>
            </table>
        </div>
        """
        
        # Adicionar marcador ao grupo
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row.get('NOME', 'N/D')} ({descricao})",
            icon=folium.Icon(color=cor, icon=icone, prefix='glyphicon')
        ).add_to(grupos[categoria])
    
    # Adicionar todos os grupos ao mapa
    for categoria, grupo in grupos.items():
        grupo.add_to(mapa)
        print(f"   ✓ {categoria}: {contadores[categoria]} estabelecimentos")
    
    # === CONTROLE DE CAMADAS (RETRÁTIL - LADO ESQUERDO) ===
    folium.LayerControl(
        position='topleft',  # ESQUERDA para não sobrepor legenda
        collapsed=True,  # RETRÁTIL!
        autoZIndex=True
    ).add_to(mapa)
    
    # === TÍTULO ===
    titulo_html = '''
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                background: white;
                padding: 15px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 9999;
                text-align: center;
                border-left: 5px solid #0066cc;">
        <h2 style="margin: 0; color: #0066cc; font-size: 20px;">
            🏥 Estabelecimentos de Saúde - Concórdia/SC
        </h2>
        <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">
            Classificação Detalhada por Tipo | Controle de Camadas Ativo
        </p>
    </div>
    '''
    
    # === RODAPÉ ===
    rodape_html = '''
    <div style="position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%;
                background: linear-gradient(to top, rgba(0, 102, 204, 0.92), rgba(0, 102, 204, 0.85));
                padding: 10px;
                z-index: 9999;
                text-align: center;
                color: white;
                font-size: 12px;">
        <strong>📊 Fontes:</strong> CNES/DataSUS | IBGE | 
        <strong>👨‍🎓 Autor:</strong> Ronan Armando Caetano - UFSC/IFSC
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    mapa.get_root().html.add_child(folium.Element(rodape_html))
    
    # === LEGENDA COMPLETA ===
    legenda_html = f'''
    <div style="position: fixed; 
                top: 90px; 
                right: 10px; 
                width: 280px;
                background: white;
                border: 2px solid #0066cc;
                border-radius: 8px;
                z-index: 9998;
                padding: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                font-family: Arial, sans-serif;
                font-size: 11px;
                max-height: 70vh;
                overflow-y: auto;">
        <h4 style="margin: 0 0 10px 0; 
                   color: #0066cc; 
                   font-size: 14px;
                   border-bottom: 2px solid #0066cc;
                   padding-bottom: 5px;
                   font-weight: bold;">
            📋 LEGENDA DO MAPA
        </h4>
        
        <div style="margin-bottom: 10px;">
            <strong style="color: #cc0000; font-size: 12px;">🏥 Estabelecimentos Públicos ({count_publicos}):</strong><br>
            <div style="margin-left: 10px; margin-top: 3px;">
                <span style="color: #cc0000;">●</span> ESF/UBS/Postos<br>
            </div>
        </div>
        
        <div style="margin-bottom: 10px;">
            <strong style="color: #0066cc; font-size: 12px;">🏨 Estabelecimentos Privados ({count_privados}):</strong><br>
            <div style="margin-left: 10px; margin-top: 3px;">
                <span style="color: #0066ff;">●</span> Consultórios Médicos<br>
                <span style="color: #87CEEB;">●</span> Consultórios Odontológicos<br>
                <span style="color: #9370DB;">●</span> Clínicas Especializadas<br>
                <span style="color: #32CD32;">●</span> Farmácias<br>
                <span style="color: #FFA500;">●</span> Laboratórios<br>
                <span style="color: #FF69B4;">●</span> Hospitais<br>
                <span style="color: #8B0000;">●</span> Emergência (SAMU)<br>
            </div>
        </div>
        
        <div style="margin-bottom: 10px;">
            <strong style="color: #9400D3; font-size: 12px;">📐 Análises Espaciais:</strong><br>
            <div style="margin-left: 10px; margin-top: 3px;">
                <span style="display: inline-block; width: 15px; height: 8px; background: linear-gradient(to right, #FF6B6B, #4ECDC4); border: 1px solid #9400D3; margin-right: 5px;"></span> Polígonos de Voronoi<br>
                <span style="display: inline-block; width: 15px; height: 2px; background: #FF6347; border: 1px dashed #FF6347; margin-right: 5px;"></span> Setores Censitários<br>
                <span style="display: inline-block; width: 15px; height: 2px; background: #228b22; border: 1px dashed #228b22; margin-right: 5px;"></span> Raio 5km (Urbano)<br>
                <span style="display: inline-block; width: 15px; height: 2px; background: #ff8c00; border: 1px dashed #ff8c00; margin-right: 5px;"></span> Raio 10km (Periurbano)<br>
            </div>
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong style="color: #0066cc; font-size: 12px;">🗺️ Limites:</strong><br>
            <div style="margin-left: 10px; margin-top: 3px;">
                <span style="display: inline-block; width: 20px; height: 2px; background: #0066cc; border: 2px dashed #0066cc; margin-right: 5px;"></span> Município de Concórdia<br>
            </div>
        </div>
        
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        
        <div style="text-align: center; font-size: 11px; color: #666;">
            <strong>Total: {len(df)} estabelecimentos</strong><br>
            Dentro do município de Concórdia
        </div>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    # === ROSA DOS VENTOS (N, S, L, O) ===
    rosa_html = '''
    <div style="position: fixed; 
                bottom: 70px; 
                left: 10px; 
                z-index: 9999;
                background: white;
                border-radius: 50%;
                padding: 5px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
        <svg width="80" height="80">
            <circle cx="40" cy="40" r="35" fill="white" stroke="#0066cc" stroke-width="2" opacity="0.95"/>
            <line x1="40" y1="10" x2="40" y2="70" stroke="#cc0000" stroke-width="2.5"/>
            <line x1="10" y1="40" x2="70" y2="40" stroke="#0066cc" stroke-width="2"/>
            <text x="40" y="18" text-anchor="middle" font-weight="bold" font-size="16" fill="#cc0000">N</text>
            <text x="40" y="75" text-anchor="middle" font-weight="bold" font-size="14" fill="#666">S</text>
            <text x="75" y="45" text-anchor="middle" font-weight="bold" font-size="14" fill="#0066cc">L</text>
            <text x="5" y="45" text-anchor="middle" font-weight="bold" font-size="14" fill="#0066cc">O</text>
        </svg>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(rosa_html))
    
    print("   ✓ Rosa dos ventos adicionada (N, S, L, O)")
    
    return mapa

def main():
    print("=" * 70)
    print("🗺️ MAPA INTERATIVO COM CAMADAS DETALHADAS")
    print("=" * 70)
    
    # Carregar dados
    df = carregar_dados()
    
    # Criar mapa
    mapa = criar_mapa_camadas(df)
    
    # Salvar
    output_path = os.path.join(ROOT_DIR, 'docs', 'mapa_camadas_detalhadas.html')
    mapa.save(output_path)
    
    # Copiar para 03_RESULTADOS
    output_path2 = os.path.join(ROOT_DIR, '03_RESULTADOS', 'mapas', 'mapa_camadas_detalhadas.html')
    mapa.save(output_path2)
    
    print(f"\n✅ Mapa salvo em:")
    print(f"   • {output_path}")
    print(f"   • {output_path2}")
    
    print("\n" + "=" * 70)
    print("✅ CONCLUÍDO!")
    print("=" * 70)
    print("\n💡 Use o controle de camadas (canto superior direito) para:")
    print("   • Mostrar/ocultar cada tipo de estabelecimento")
    print("   • Visualizar apenas farmácias, consultórios, etc.")
    print("   • Comparar distribuições espaciais por categoria")

if __name__ == '__main__':
    main()
