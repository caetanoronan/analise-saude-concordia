"""
Script para atualizar o mapa mapa_unidades_saude_concordia.html com as seguintes características:
- Limite Municipal: Polígono de Concórdia destacado em azul tracejado
- Marcadores Vermelhos: Estabelecimentos públicos (ESF/PS)
- Centro Urbano: Marcador preto de referência
- Círculos de Análise: 5km (verde) e 10km (laranja)
- Título: "Estabelecimentos de Saúde - Concórdia/SC (Filtrado)"
- Rodapé: Créditos e fontes profissionais
"""

import pandas as pd
import folium
import os
from math import radians, cos, sin, asin, sqrt
try:
    import geopandas as gpd
    GEOPANDAS_DISPONIVEL = True
except ImportError:
    GEOPANDAS_DISPONIVEL = False
    print("⚠️ GeoPandas não disponível. Filtro espacial rigoroso desabilitado.")

# Configurações
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRO_CONCORDIA = [-27.2335, -52.0238]  # Centro urbano de referência

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula distância entre duas coordenadas usando Haversine"""
    R = 6371  # Raio da Terra em km
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    
    return R * c

def eh_estabelecimento_publico(nome_fantasia, tipo_unidade, razao_social=''):
    """Verifica se é estabelecimento público (ESF/PS)"""
    if pd.isna(nome_fantasia):
        nome_fantasia = ''
    
    nome = str(nome_fantasia).upper()
    razao = str(razao_social).upper()
    
    # Critérios para identificar estabelecimentos públicos
    criterios_publicos = [
        'ESF' in nome,
        'PS ' in nome,
        'POSTO DE SAUDE' in nome,
        'UNIDADE BASICA' in nome,
        'UBS' in nome,
        'CENTRO DE SAUDE' in nome,
        'ESTRATEGIA SAUDE DA FAMILIA' in nome,
        'MUNICIPIO' in razao,
        'PREFEITURA' in razao,
        'SECRETARIA' in razao
    ]
    
    # Tipos de unidade pública (2=ESF, 1=Posto, 4=Policlínica, 70=Centro de Saúde)
    if str(tipo_unidade) in ['1', '2', '4', '70', '81']:
        return True
    
    return any(criterios_publicos)

def classificar_estabelecimento(nome, razao_social, tipo_unidade):
    """
    Classifica estabelecimento e retorna descrição do tipo.
    Retorna: ('PÚBLICO' ou 'PRIVADO', descrição do tipo, cor do marcador)
    """
    nome_upper = str(nome).upper()
    razao_upper = str(razao_social).upper() if pd.notna(razao_social) else ""
    tipo_str = str(tipo_unidade)
    
    # === ESTABELECIMENTOS PÚBLICOS ===
    # Tipos CNES públicos: 1=Posto, 2=ESF, 4=Policlínica, 70=Centro Saúde, 81=Móvel
    criterios_publicos = [
        'ESF' in nome_upper,
        'ESTRATEGIA SAUDE FAMILIA' in nome_upper,
        'UNIDADE BASICA' in nome_upper,
        'UNIDADE SAUDE' in nome_upper,
        'UBS' in nome_upper,
        'POSTO SAUDE' in nome_upper or 'POSTO DE SAUDE' in nome_upper,
        'PS ' in nome_upper,
        'MUNICIPIO' in razao_upper or 'PREFEITURA' in razao_upper,
        tipo_str in ['1', '2', '4', '70', '81']  # Tipos públicos CNES
    ]
    
    if any(criterios_publicos):
        # Determinar descrição específica
        if tipo_str == '2' or 'ESF' in nome_upper:
            return ('PÚBLICO', 'ESF - Estratégia Saúde da Família', 'red')
        elif tipo_str == '1' or 'POSTO' in nome_upper:
            return ('PÚBLICO', 'PS - Posto de Saúde', 'red')
        elif tipo_str == '4':
            return ('PÚBLICO', 'Policlínica', 'red')
        elif tipo_str == '70':
            return ('PÚBLICO', 'Centro de Saúde', 'red')
        elif tipo_str == '81':
            return ('PÚBLICO', 'Unidade Móvel', 'red')
        else:
            return ('PÚBLICO', 'Unidade Pública de Saúde', 'red')
    
    # === ESTABELECIMENTOS PRIVADOS ===
    # Tipos CNES privados: 22=Consultório, 36=Clínica, 39=Laboratório, 43=Serviço Apoio, etc.
    else:
        if tipo_str == '22':
            return ('PRIVADO', 'Consultório Médico/Odontológico', 'blue')
        elif tipo_str == '36':
            return ('PRIVADO', 'Clínica/Centro Especialidades', 'blue')
        elif tipo_str == '39':
            return ('PRIVADO', 'Laboratório de Análises Clínicas', 'blue')
        elif tipo_str == '43':
            return ('PRIVADO', 'Serviço de Apoio Diagnóstico', 'blue')
        elif tipo_str == '5':
            return ('PRIVADO', 'Hospital Geral/Especializado', 'blue')
        elif tipo_str == '42':
            return ('PRIVADO', 'Unidade de Apoio Diagnose/Terapia', 'blue')
        else:
            return ('PRIVADO', 'Estabelecimento Privado de Saúde', 'blue')

def carregar_dados():
    """Carrega TODOS os estabelecimentos de saúde (públicos + privados)"""
    print("📂 Carregando TODOS os estabelecimentos (públicos + privados)...")
    
    # Tentar carregar da base completa primeiro
    try:
        # === CARREGAR BASE COMPLETA (418 ESTABELECIMENTOS) ===
        # 1. Tentar Tabela_estado_SC.xlsx (fonte primária com TODOS os estabelecimentos)
        caminho_xlsx = os.path.join(ROOT_DIR, 'Tabela_estado_SC.xlsx')
        caminho_csv = os.path.join(ROOT_DIR, '01_DADOS', 'originais', 'Tabela_estado_SC.csv')
        
        if os.path.exists(caminho_xlsx):
            print("   → Carregando base completa SC (Excel)...")
            df_sc = pd.read_excel(caminho_xlsx)
            
            # Filtrar apenas Concórdia (código IBGE 420430)
            df = df_sc[df_sc['CO_MUNICIPIO_GESTOR'] == 420430].copy()
            
            # Padronizar nomes de colunas
            df = df.rename(columns={
                'NO_FANTASIA': 'NOME',
                'NO_LOGRADOURO': 'ENDERECO',
                'NO_BAIRRO': 'BAIRRO',
                'CO_CEP': 'CEP',
                'NU_LATITUDE': 'LAT',
                'NU_LONGITUDE': 'LON',
                'TP_UNIDADE': 'TIPO_UNIDADE',
                'NO_RAZAO_SOCIAL': 'RAZAO_SOCIAL'
            })
            
            print(f"   ✅ Base completa carregada: {len(df)} estabelecimentos totais")
        elif os.path.exists(caminho_csv):
            print("   → Carregando base completa SC (CSV)...")
            df_sc = pd.read_csv(caminho_csv, sep=';', low_memory=False, encoding='latin1')
            
            # Filtrar apenas Concórdia (código IBGE 420430)
            df = df_sc[df_sc['CO_MUNICIPIO_GESTOR'] == 420430].copy()
            
            # Padronizar nomes de colunas
            df = df.rename(columns={
                'NO_FANTASIA': 'NOME',
                'NO_LOGRADOURO': 'ENDERECO',
                'NO_BAIRRO': 'BAIRRO',
                'CO_CEP': 'CEP',
                'NU_LATITUDE': 'LAT',
                'NU_LONGITUDE': 'LON',
                'TP_UNIDADE': 'TIPO_UNIDADE',
                'NO_RAZAO_SOCIAL': 'RAZAO_SOCIAL'
            })
            
            print(f"   ✅ Base completa carregada: {len(df)} estabelecimentos totais")
        else:
            raise FileNotFoundError("Base completa não encontrada")
    
    except Exception as e:
        print(f"   ⚠️ Base completa não disponível: {e}")
        print("   → Tentando CSV processado...")
        
        try:
            caminho_csv = os.path.join(ROOT_DIR, '01_DADOS', 'processados', 'concordia_saude_simples.csv')
            df = pd.read_csv(caminho_csv)
            print("   ✅ CSV processado carregado")
        except Exception as e2:
            print(f"   ❌ Erro ao carregar CSV processado: {e2}")
            return None
    
    # Garantir tipos numéricos
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    
    # Remover coordenadas inválidas
    df = df.dropna(subset=['LAT', 'LON'])
    
    print(f"   → {len(df)} estabelecimentos antes do filtro espacial")
    
    # === FILTRO ESPACIAL RIGOROSO (REMOVE PS SAO PAULO E ESF ESTADOS) ===
    if GEOPANDAS_DISPONIVEL:
        try:
            print("   → Aplicando filtro espacial rigoroso...")
            
            # Converter DataFrame para GeoDataFrame
            df_geo = gpd.GeoDataFrame(
                df, 
                geometry=gpd.points_from_xy(df['LON'], df['LAT']), 
                crs='EPSG:4326'
            )
            
            # Carregar limite municipal para filtro espacial
            shp_municipio = None
            shp_paths = [
                os.path.join(ROOT_DIR, 'SC_Municipios_2024', 'SC_Municipios_2024.shp'),
                os.path.join(ROOT_DIR, 'SC_municipios_regiao_concordia.shp')
            ]
            
            for shp_path in shp_paths:
                if os.path.exists(shp_path):
                    shp_municipio = gpd.read_file(shp_path)
                    if shp_municipio.crs != 'EPSG:4326':
                        shp_municipio = shp_municipio.to_crs('EPSG:4326')
                    
                    # Filtrar apenas Concórdia
                    for col in shp_municipio.columns:
                        col_upper = str(col).upper()
                        if 'CD_MUN' in col_upper or 'GEOCODIGO' in col_upper:
                            shp_municipio = shp_municipio[shp_municipio[col].astype(str).str.contains('420430|4204301')]
                            break
                        elif 'NM_MUN' in col_upper or 'NOME' in col_upper:
                            shp_municipio = shp_municipio[shp_municipio[col].str.contains('Concórdia', case=False, na=False)]
                            break
                    
                    if not shp_municipio.empty:
                        print(f"   ✓ Shapefile encontrado: {os.path.basename(shp_path)}")
                        break
            
            if shp_municipio is not None and not shp_municipio.empty:
                # Aplicar filtro espacial: apenas estabelecimentos DENTRO do município
                df_dentro = gpd.sjoin(df_geo, shp_municipio, how='inner', predicate='within')
                
                # Identificar estabelecimentos removidos
                ids_removidos = set(df_geo.index) - set(df_dentro.index)
                if ids_removidos:
                    print(f"   ⚠️ {len(ids_removidos)} estabelecimentos FORA do município (removidos):")
                    for idx in ids_removidos:
                        nome = df_geo.loc[idx, 'NOME'] if 'NOME' in df_geo.columns else 'N/D'
                        lat = df_geo.loc[idx, 'LAT']
                        lon = df_geo.loc[idx, 'LON']
                        print(f"      • {nome} ({lat:.6f}, {lon:.6f})")
                
                # Converter de volta para DataFrame
                df = pd.DataFrame(df_dentro.drop(columns='geometry'))
                df = df.reset_index(drop=True)
                
                print(f"   ✅ Filtro espacial aplicado: {len(df)} estabelecimentos DENTRO do município")
            else:
                print("   ⚠️ Shapefile de limite não encontrado, usando filtro de coordenadas")
                # Fallback: filtro por coordenadas
                df = df[
                    (df['LAT'] >= -27.5) & (df['LAT'] <= -27.0) &
                    (df['LON'] >= -52.3) & (df['LON'] <= -51.8)
                ]
                print(f"   ✅ {len(df)} estabelecimentos (filtro por coordenadas)")
        
        except Exception as e:
            print(f"   ⚠️ Erro no filtro espacial: {e}")
            # Fallback: filtro por coordenadas
            df = df[
                (df['LAT'] >= -27.5) & (df['LAT'] <= -27.0) &
                (df['LON'] >= -52.3) & (df['LON'] <= -51.8)
            ]
            print(f"   ✅ {len(df)} estabelecimentos (filtro por coordenadas - fallback)")
    else:
        # Se GeoPandas não disponível: filtro simples por coordenadas
        df = df[
            (df['LAT'] >= -27.5) & (df['LAT'] <= -27.0) &
            (df['LON'] >= -52.3) & (df['LON'] <= -51.8)
        ]
        print(f"   ✅ {len(df)} estabelecimentos (filtro por coordenadas)")
    
    return df

def carregar_limite_municipal():
    """Carrega polígono do limite municipal de Concórdia"""
    print("🗺️ Carregando limite municipal...")
    
    try:
        import geopandas as gpd
        
        # Tentar carregar shapefile de Concórdia
        shp_path = os.path.join(ROOT_DIR, '03_RESULTADOS', 'shapefiles', 'Concordia_sencitario.shp')
        
        if os.path.exists(shp_path):
            gdf = gpd.read_file(shp_path)
            
            # Garantir CRS WGS84
            if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)
            
            print("✅ Limite municipal carregado")
            return gdf
        else:
            print("⚠️ Shapefile não encontrado, tentando fonte alternativa...")
            
            # Tentar SC_municipios_regiao_concordia.shp
            shp_alt = os.path.join(ROOT_DIR, 'SC_municipios_regiao_concordia.shp')
            if os.path.exists(shp_alt):
                gdf = gpd.read_file(shp_alt)
                if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                    gdf = gdf.to_crs(epsg=4326)
                
                # Filtrar apenas Concórdia
                for col in gdf.columns:
                    if 'NM_MUN' in col.upper() or 'NOME' in col.upper():
                        gdf = gdf[gdf[col].str.contains('Concórdia', case=False, na=False)]
                        break
                
                if not gdf.empty:
                    print("✅ Limite municipal carregado (fonte alternativa)")
                    return gdf
    
    except Exception as e:
        print(f"⚠️ Erro ao carregar limite: {e}")
    
    return None

def criar_mapa_atualizado(df, gdf_municipio):
    """Cria mapa com as especificações solicitadas"""
    print("\n🗺️ Criando mapa atualizado...")
    
    # Criar mapa base centrado em Concórdia com limites de zoom
    mapa = folium.Map(
        location=CENTRO_CONCORDIA,
        zoom_start=12,
        min_zoom=10,      # Limite de zoom expansão (mais afastado)
        max_zoom=18,      # Limite de zoom aproximação (mais próximo)
        tiles='OpenStreetMap',
        control_scale=True,
        prefer_canvas=True
    )
    
    # === 1. LIMITE MUNICIPAL (Azul tracejado) ===
    if gdf_municipio is not None and not gdf_municipio.empty:
        print("   → Adicionando limite municipal (azul tracejado)")
        
        folium.GeoJson(
            data=gdf_municipio.__geo_interface__,
            name='🔵 Limite Municipal - Concórdia/SC',
            style_function=lambda x: {
                'color': '#0066cc',           # Azul
                'weight': 3,
                'fillColor': '#cce5ff',       # Azul claro
                'fillOpacity': 0.1,
                'dashArray': '10, 5',         # Tracejado
                'lineJoin': 'round'
            },
            highlight_function=lambda x: {
                'weight': 4,
                'fillOpacity': 0.2
            },
            tooltip=folium.Tooltip('Limite Municipal de Concórdia'),
            popup=folium.Popup(
                '<b>Município de Concórdia/SC</b><br>'
                'Código IBGE: 420430<br>'
                'Área: ~799 km²<br>'
                'Fonte: IBGE',
                max_width=250
            )
        ).add_to(mapa)
    
    # === 2. CÍRCULOS DE ANÁLISE (5km verde, 10km laranja) ===
    print("   → Adicionando círculos de análise (5km e 10km)")
    
    # Círculo de 5km (verde)
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=5000,  # 5km em metros
        color='#228b22',        # Verde floresta
        fillColor='#90ee90',    # Verde claro
        fillOpacity=0.15,
        weight=2,
        dashArray='5, 3',
        popup=folium.Popup('<b>Raio: 5 km</b><br>Área urbana central', max_width=200),
        tooltip='Raio 5km - Zona Urbana'
    ).add_to(mapa)
    
    # Círculo de 10km (laranja)
    folium.Circle(
        location=CENTRO_CONCORDIA,
        radius=10000,  # 10km em metros
        color='#ff8c00',        # Laranja escuro
        fillColor='#ffa500',    # Laranja
        fillOpacity=0.1,
        weight=2,
        dashArray='5, 3',
        popup=folium.Popup('<b>Raio: 10 km</b><br>Área periurbana', max_width=200),
        tooltip='Raio 10km - Zona Periurbana'
    ).add_to(mapa)
    
    # === 3. CENTRO URBANO (Marcador preto) ===
    print("   → Adicionando marcador do centro urbano")
    
    folium.Marker(
        location=CENTRO_CONCORDIA,
        popup=folium.Popup(
            '<b>🏛️ Centro Urbano de Concórdia</b><br>'
            f'Coordenadas: {CENTRO_CONCORDIA[0]:.6f}, {CENTRO_CONCORDIA[1]:.6f}<br>'
            'Ponto de referência para análise espacial',
            max_width=300
        ),
        tooltip='Centro Urbano (Referência)',
        icon=folium.Icon(color='black', icon='home', prefix='glyphicon')
    ).add_to(mapa)
    
    # === 4. ESTABELECIMENTOS PÚBLICOS E PRIVADOS ===
    print("   → Adicionando TODOS os estabelecimentos (públicos + privados)")
    
    count_publicos = 0
    count_privados = 0
    
    for idx, row in df.iterrows():
        # Classificar estabelecimento (retorna: categoria, descrição, cor)
        categoria, descricao_tipo, cor = classificar_estabelecimento(
            row.get('NOME', ''),
            row.get('RAZAO_SOCIAL', ''),
            row.get('TIPO_UNIDADE', '')
        )
        
        # Calcular distância ao centro
        distancia = calcular_distancia(
            CENTRO_CONCORDIA[0], CENTRO_CONCORDIA[1],
            row['LAT'], row['LON']
        )
        
        # Determinar ícone baseado na categoria
        if categoria == 'PÚBLICO':
            icone = 'plus'
            count_publicos += 1
        else:
            icone = 'info-sign'
            count_privados += 1
        
        # Classificar por distância
        if distancia <= 5:
            zona = 'Urbana (< 5km)'
        elif distancia <= 10:
            zona = 'Periurbana (5-10km)'
        else:
            zona = 'Rural (> 10km)'
        
        # Criar popup com informações detalhadas
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: {'#cc0000' if categoria == 'PÚBLICO' else '#0066cc'};">
                {row.get('NOME', 'N/D')}
            </h4>
            <table style="width: 100%; font-size: 12px;">
                <tr>
                    <td><b>Categoria:</b></td>
                    <td><span style="color: {'#cc0000' if categoria == 'PÚBLICO' else '#0066cc'}; font-weight: bold;">{categoria}</span></td>
                </tr>
                <tr>
                    <td><b>Tipo:</b></td>
                    <td>{descricao_tipo}</td>
                </tr>
                <tr>
                    <td><b>Endereço:</b></td>
                    <td>{row.get('ENDERECO', 'N/D')}</td>
                </tr>
                <tr>
                    <td><b>Bairro:</b></td>
                    <td>{row.get('BAIRRO', 'N/D')}</td>
                </tr>
                <tr>
                    <td><b>Distância:</b></td>
                    <td>{distancia:.2f} km</td>
                </tr>
                <tr>
                    <td><b>Zona:</b></td>
                    <td>{zona}</td>
                </tr>
            </table>
        </div>
        """
        
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{row.get('NOME', 'N/D')} ({categoria})",
            icon=folium.Icon(color=cor, icon=icone, prefix='glyphicon')
        ).add_to(mapa)
    
    print(f"   ✅ {count_publicos} estabelecimentos PÚBLICOS (vermelho)")
    print(f"   ✅ {count_privados} estabelecimentos PRIVADOS (azul)")
    
    # === 5. TÍTULO ===
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
        <h2 style="margin: 0; 
                   color: #0066cc; 
                   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                   font-size: 22px;
                   font-weight: 600;
                   letter-spacing: 0.5px;">
            🏥 TODOS os Estabelecimentos de Saúde - Concórdia/SC
        </h2>
        <p style="margin: 5px 0 0 0;
                  color: #666;
                  font-size: 13px;
                  font-weight: normal;">
            Públicos (Vermelho) + Privados (Azul) | Análise Espacial com Limite Municipal
        </p>
    </div>
    '''
    
    # === 6. RODAPÉ ===
    rodape_html = '''
    <div style="position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%;
                background: linear-gradient(to top, rgba(0, 102, 204, 0.92), rgba(0, 102, 204, 0.85));
                padding: 12px 20px;
                z-index: 9999;
                text-align: center;
                border-top: 3px solid #004080;
                box-shadow: 0 -4px 12px rgba(0,0,0,0.3);">
        <div style="color: white; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 13px;
                    line-height: 1.6;">
            <strong style="font-size: 14px; letter-spacing: 0.5px;">📊 Fontes:</strong> 
            <span style="opacity: 0.95;">CNES/DataSUS | IBGE | Município de Concórdia</span>
            <span style="margin: 0 15px; opacity: 0.7;">|</span>
            <strong style="font-size: 14px; letter-spacing: 0.5px;">👨‍🎓 Autor:</strong> 
            <span style="opacity: 0.95;">Ronan Armando Caetano</span>
            <span style="margin: 0 10px; opacity: 0.7;">•</span>
            <span style="opacity: 0.95;">Graduando em Ciências Biológicas UFSC</span>
            <span style="margin: 0 10px; opacity: 0.7;">•</span>
            <span style="opacity: 0.95;">Técnico em Geoprocessamento IFSC</span>
        </div>
    </div>
    '''
    
    # Adicionar título e rodapé ao mapa
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    mapa.get_root().html.add_child(folium.Element(rodape_html))
    
    # === 7. LEGENDA ===
    legenda_html = '''
    <div style="position: fixed; 
                top: 120px; 
                right: 10px; 
                width: 240px;
                background-color: white;
                border: 2px solid #0066cc;
                border-radius: 8px;
                z-index: 9998;
                padding: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                font-family: Arial, sans-serif;
                font-size: 12px;">
        <h4 style="margin: 0 0 10px 0; 
                   color: #0066cc; 
                   font-size: 14px;
                   border-bottom: 2px solid #0066cc;
                   padding-bottom: 5px;">
            📍 Legenda
        </h4>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 12px; 
                         height: 12px; 
                         background-color: #cc0000; 
                         border-radius: 50%;
                         margin-right: 8px;"></span>
            <b>Público</b> (ESF, PS, UBS)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 12px; 
                         height: 12px; 
                         background-color: #0066cc; 
                         border-radius: 50%;
                         margin-right: 8px;"></span>
            <b>Privado</b> (Consultórios, Clínicas, Labs)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 12px; 
                         height: 12px; 
                         background-color: #000; 
                         border-radius: 50%;
                         margin-right: 8px;"></span>
            Centro Urbano (Referência)
        </div>
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 20px; 
                         height: 2px; 
                         background-color: #228b22; 
                         margin-right: 8px;
                         border: 1px dashed #228b22;"></span>
            Raio 5 km (Urbano)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 20px; 
                         height: 2px; 
                         background-color: #ff8c00; 
                         margin-right: 8px;
                         border: 1px dashed #ff8c00;"></span>
            Raio 10 km (Periurbano)
        </div>
        <div style="margin: 8px 0;">
            <span style="display: inline-block; 
                         width: 20px; 
                         height: 2px; 
                         background-color: #0066cc; 
                         margin-right: 8px;
                         border: 2px dashed #0066cc;"></span>
            Limite Municipal
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    # Adicionar controle de camadas
    folium.LayerControl(collapsed=False, position='topleft').add_to(mapa)
    
    return mapa

def main():
    print("="*60)
    print("🗺️ ATUALIZAÇÃO DO MAPA DE UNIDADES DE SAÚDE - CONCÓRDIA/SC")
    print("="*60)
    
    # 1. Carregar dados
    df = carregar_dados()
    if df is None:
        print("❌ Falha ao carregar dados. Abortando.")
        return
    
    # 2. Carregar limite municipal
    gdf_municipio = carregar_limite_municipal()
    
    # 3. Criar mapa atualizado
    mapa = criar_mapa_atualizado(df, gdf_municipio)
    
    # 4. Salvar mapa no diretório docs/
    output_path = os.path.join(ROOT_DIR, 'docs', 'mapa_unidades_saude_concordia.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    mapa.save(output_path)
    
    print(f"\n✅ Mapa atualizado salvo em:")
    print(f"   {output_path}")
    
    print("\n" + "="*60)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📌 Características aplicadas:")
    print("   ✓ Limite Municipal: Polígono azul tracejado")
    print("   ✓ Marcadores Vermelhos: Estabelecimentos públicos (ESF/PS)")
    print("   ✓ Centro Urbano: Marcador preto de referência")
    print("   ✓ Círculos de Análise: 5km (verde) e 10km (laranja)")
    print("   ✓ Título: 'Estabelecimentos de Saúde - Concórdia/SC (Filtrado)'")
    print("   ✓ Rodapé: Créditos e fontes profissionais")
    print("   ✓ Legenda: Explicação dos elementos visuais")

if __name__ == '__main__':
    main()
