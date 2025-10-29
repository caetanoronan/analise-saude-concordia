#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Avançado Simplificado - Análise Espacial Estabelecimentos de Saúde Concórdia/SC
Aplicando ColorBrewer palettes e TreeLayerControl do Folium

Autor: Caetano Ronan
Instituição: UFSC
Data: Outubro 2025
"""

import os
import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from math import radians, sin, cos, sqrt, atan2
import warnings
warnings.filterwarnings('ignore')

# Caminhos do projeto (independentes do diretório atual)
SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
OUTPUT_DIR = os.path.join(ROOT_DIR, '03_RESULTADOS')
MAPAS_DIR = os.path.join(OUTPUT_DIR, 'mapas')
os.makedirs(MAPAS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configurações ColorBrewer
COLORBREWER_SEQUENTIAL = {
    'BuGn_3': ['#ccece6', '#66c2a4', '#238b45'],
    'BuGn_5': ['#edf8fb', '#ccece6', '#99d8c9', '#66c2a4', '#238b45'],
    'YlOrRd_3': ['#ffeda0', '#feb24c', '#f03b20'],
    'Blues_5': ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c'],
    'Reds_5': ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15']
}

COLORBREWER_QUALITATIVE = {
    'Set1_8': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf'],
    'Dark2_8': ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666'],
    'Accent_8': ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
}

def carregar_dados():
    print("\n" + "="*70)
    print("🏥 INICIANDO PROCESSAMENTO DE DADOS")
    print("="*70)
    print("⏳ [1/6] Carregando dados dos estabelecimentos de saúde...")
    
    try:
        df_concordia = pd.read_csv(os.path.join(ROOT_DIR, 'concordia_saude_simples.csv'))
        print(f"   ✅ Dados processados carregados: {len(df_concordia)} estabelecimentos")
        
    except FileNotFoundError:
        try:
            df_sc = pd.read_csv(os.path.join(ROOT_DIR, 'Tabela_estado_SC.csv'), sep=';', encoding='utf-8', low_memory=False)
            df_concordia = df_sc[df_sc['CO_MUNICIPIO_GESTOR'] == 420430].copy()
            print(f"   ✅ Base SC carregada: {len(df_concordia)} estabelecimentos")
            
        except FileNotFoundError:
            print("   ⚠️ Criando dados sintéticos para demonstração...")
            df_concordia = criar_dados_sinteticos()
    
    print("⏳ [2/6] Filtrando estabelecimentos excluídos...")
    inicial = len(df_concordia)
    nome_col = None
    for col in ['NO_FANTASIA', 'NOME']:
        if col in df_concordia.columns:
            nome_col = col
            break
    
    if nome_col:
        mascara_excluir = (
            df_concordia[nome_col].str.contains('PS SAO PAULO', case=False, na=False) |
            df_concordia[nome_col].str.contains('PS SÃO PAULO', case=False, na=False) |
            df_concordia[nome_col].str.contains('ESF ESTADOS', case=False, na=False)
        )
        removidos = df_concordia[mascara_excluir][nome_col].tolist()
        if removidos:
            print(f"   🗑️ Removendo: {', '.join(removidos)}")
        df_concordia = df_concordia[~mascara_excluir].copy()
        excluidos = inicial - len(df_concordia)
        if excluidos > 0:
            print(f"   ✅ Removidos {excluidos} estabelecimentos")
        else:
            print(f"   ℹ️ Nenhum estabelecimento excluído encontrado")
    else:
        print(f"   ⚠️ Coluna de nome não encontrada - filtro não aplicado")
    
    print("⏳ [3/6] Processando coordenadas geográficas...")
    df_geo = processar_coordenadas(df_concordia)
    
    print("⏳ [4/6] Calculando distâncias ao centro urbano...")
    df_geo = calcular_distancias(df_geo)
    
    print("⏳ [5/6] Classificando estabelecimentos (público/privado)...")
    df_geo = classificar_estabelecimentos(df_geo)
    
    print("⏳ [6/6] Adicionando categorias de análise...")
    df_geo = adicionar_categorias_analise(df_geo)
    
    print("\n✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"📊 Total final: {len(df_geo)} estabelecimentos processados")
    print("="*70 + "\n")
    
    return df_geo

def criar_dados_sinteticos():
    np.random.seed(42)
    centro_lat, centro_lon = -27.2335, -52.0238
    tipos_estabelecimentos = {
        1: "Posto de Saúde",
        2: "Centro de Saúde/ESF", 
        4: "Policlínica",
        5: "Hospital Geral",
        22: "Consultório Médico",
        39: "Laboratório de Análises",
        70: "CAPS",
        81: "UPA"
    }
    dados = []
    for i in range(150):
        raio = np.random.exponential(0.02)
        angulo = np.random.uniform(0, 2*np.pi)
        lat = centro_lat + raio * np.cos(angulo)
        lon = centro_lon + raio * np.sin(angulo)
        tipo_weights = [0.15, 0.20, 0.05, 0.03, 0.35, 0.15, 0.04, 0.03]
        tipo = np.random.choice(list(tipos_estabelecimentos.keys()), p=tipo_weights)
        nomes_base = [
            "ESF", "PS", "Centro de Saúde", "UBS", "Clínica", "Hospital", 
            "Laboratório", "CAPS", "Consultório", "Ambulatório"
        ]
        bairros = [
            "Centro", "São Cristóvão", "Salete", "Glória", "Industrial",
            "Petrópolis", "Vila Rica", "São Paulo", "Jardim do Cedro", "Alto Alegre"
        ]
        nome = f"{np.random.choice(nomes_base)} {np.random.choice(['Central', 'Municipal', bairros[i%10]])}"
        dados.append({
            'NO_FANTASIA': nome,
            'NU_LATITUDE': lat,
            'NU_LONGITUDE': lon,
            'TP_UNIDADE': tipo,
            'NO_BAIRRO': bairros[i % len(bairros)],
            'NO_LOGRADOURO': f"Rua {np.random.choice(['das Flores', 'Principal', 'Central', 'da Saúde'])}, {np.random.randint(1, 999)}",
            'NO_RAZAO_SOCIAL': f"Estabelecimento {i+1}",
            'tipo_descricao': tipos_estabelecimentos[tipo]
        })
    return pd.DataFrame(dados)

def processar_coordenadas(df):
    """Processa e limpa coordenadas geográficas"""
    
    # Identificar colunas de coordenadas
    lat_cols = [col for col in df.columns if 'LAT' in col.upper()]
    lon_cols = [col for col in df.columns if 'LON' in col.upper()]
    
    if lat_cols and lon_cols:
        lat_col, lon_col = lat_cols[0], lon_cols[0]
    else:
        return df
    
    # Converter para numérico
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    
    # Filtrar coordenadas válidas para região de Concórdia
    mask_valido = (
        (df[lat_col].between(-28, -26)) & 
        (df[lon_col].between(-53, -51)) &
        df[lat_col].notna() & 
        df[lon_col].notna()
    )
    
    df_clean = df[mask_valido].copy()
    print(f"   ✅ {len(df_clean)}/{len(df)} coordenadas válidas")
    
    return df_clean

def calcular_distancias(df):
    """Calcula distâncias usando fórmula de Haversine"""
    
    centro_concordia = (-27.2335, -52.0238)
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Raio da Terra em km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    # Identificar colunas de coordenadas
    lat_cols = [col for col in df.columns if 'LAT' in col.upper()]
    lon_cols = [col for col in df.columns if 'LON' in col.upper()]
    
    if lat_cols and lon_cols:
        lat_col, lon_col = lat_cols[0], lon_cols[0]
        df['dist_centro'] = df.apply(
            lambda row: haversine(centro_concordia[0], centro_concordia[1], 
                                row[lat_col], row[lon_col]), axis=1
        )
    
    print(f"   ✅ Distância média calculada: {df['dist_centro'].mean():.2f}km")
    return df

def classificar_estabelecimentos(df):
    """Classifica estabelecimentos como público/privado"""
    
    def eh_publico(nome, tipo, razao):
        nome_str = str(nome).upper() if pd.notna(nome) else ""
        razao_str = str(razao).upper() if pd.notna(razao) else ""
        tipo_str = str(tipo).upper() if pd.notna(tipo) else ""
        
        criterios_publicos = [
            'ESF' in nome_str,
            'PS ' in nome_str,
            'UBS' in nome_str,
            'CAPS' in nome_str,
            'SAMU' in nome_str,
            'MUNICIPIO' in razao_str,
            'PREFEITURA' in razao_str,
            'SECRETARIA' in razao_str,
            'ESF' in tipo_str,
            'PS' in tipo_str,
            'UBS' in tipo_str
        ]
        
        # Critérios adicionais para código de tipo
        if 'TP_UNIDADE' in df.columns:
            tipo_codigo = str(df.get('TP_UNIDADE', ''))
            criterios_publicos.append(tipo_codigo in ['1', '2', '70', '81'])
        
        return any(criterios_publicos)
    
    # Adaptar nomes das colunas
    nome_col = 'NO_FANTASIA' if 'NO_FANTASIA' in df.columns else 'NOME'
    tipo_col = 'TP_UNIDADE' if 'TP_UNIDADE' in df.columns else 'TIPO'
    razao_col = 'NO_RAZAO_SOCIAL' if 'NO_RAZAO_SOCIAL' in df.columns else None
    
    df['eh_publico'] = df.apply(
        lambda row: eh_publico(
            row.get(nome_col, ''),
            row.get(tipo_col, ''),
            row.get(razao_col, '') if razao_col else ''
        ), axis=1
    )
    
    publicos = df['eh_publico'].sum()
    print(f"   ✅ {publicos} públicos / {len(df)} total ({publicos/len(df)*100:.1f}%)")
    
    return df

def adicionar_categorias_analise(df):
    """Adiciona categorias para análise espacial"""
    
    # Categorias por distância
    df['categoria_distancia'] = pd.cut(
        df['dist_centro'],
        bins=[0, 2, 5, 10, 20, float('inf')],
        labels=['Muito Próximo (≤2km)', 'Próximo (2-5km)', 'Moderado (5-10km)', 
                'Distante (10-20km)', 'Muito Distante (>20km)']
    )
    
    # Adaptar para diferentes estruturas de dados
    if 'TP_UNIDADE' in df.columns:
        # Dados CNES completos
        tipos_principais = {
            '1': 'Posto de Saúde',
            '2': 'ESF/Centro de Saúde', 
            '4': 'Policlínica',
            '5': 'Hospital',
            '22': 'Consultório',
            '39': 'Laboratório',
            '70': 'CAPS',
            '81': 'UPA'
        }
        df['tipo_descricao'] = df['TP_UNIDADE'].astype(str).map(tipos_principais).fillna('Outros')
    elif 'TIPO' in df.columns:
        # Dados simplificados
        df['tipo_descricao'] = df['TIPO']
    else:
        # Fallback
        df['tipo_descricao'] = 'Estabelecimento de Saúde'
    
    # Setor (público/privado)
    df['setor'] = df['eh_publico'].map({True: 'Público', False: 'Privado'})
    
    # Identificar colunas de coordenadas
    lat_cols = [col for col in df.columns if 'LAT' in col.upper()]
    lon_cols = [col for col in df.columns if 'LON' in col.upper()]
    
    if lat_cols and lon_cols:
        lat_col, lon_col = lat_cols[0], lon_cols[0]
        
        # Densidade por área (simulada por quadrantes)
        lat_quartis = df[lat_col].quantile([0.25, 0.5, 0.75])
        lon_quartis = df[lon_col].quantile([0.25, 0.5, 0.75])
        
        def classificar_quadrante(lat, lon):
            if lat <= lat_quartis[0.5] and lon <= lon_quartis[0.5]:
                return 'SW'
            elif lat <= lat_quartis[0.5] and lon > lon_quartis[0.5]:
                return 'SE' 
            elif lat > lat_quartis[0.5] and lon <= lon_quartis[0.5]:
                return 'NW'
            else:
                return 'NE'
        
        df['quadrante'] = df.apply(lambda row: classificar_quadrante(row[lat_col], row[lon_col]), axis=1)
    else:
        df['quadrante'] = 'N/A'
    
    print("   ✅ Categorias adicionadas")
    return df

def criar_mapa_avancado_colorbrewer(df):
    """Cria mapa avançado com paletas ColorBrewer e camadas organizadas"""
    print("\n" + "="*70)
    print("🗺️ CRIANDO MAPA INTERATIVO")
    print("="*70)
    print("⏳ [1/5] Configurando mapa base...")
    
    centro_concordia = [-27.2335, -52.0238]
    
    # Identificar colunas de coordenadas
    lat_cols = [col for col in df.columns if 'LAT' in col.upper()]
    lon_cols = [col for col in df.columns if 'LON' in col.upper()]
    
    if not lat_cols or not lon_cols:
        print("❌ Erro: Coordenadas não encontradas")
        return None
        
    lat_col, lon_col = lat_cols[0], lon_cols[0]
    
    # Mapa base
    mapa = folium.Map(
        location=centro_concordia,
        zoom_start=12,
        tiles='OpenStreetMap',
        min_zoom=10,      # Limite mínimo de zoom (menos zoom = visão mais ampla)
        max_zoom=18,      # Limite máximo de zoom (mais zoom = visão mais próxima)
        max_bounds=True   # Limita o arrasto para a área visível
    )
    
    # === CAMADA POR SETOR (Público/Privado) - ColorBrewer Set1 ===
    cores_setor = {'Público': COLORBREWER_QUALITATIVE['Set1_8'][0], 
                   'Privado': COLORBREWER_QUALITATIVE['Set1_8'][1]}
    
    # Grupo principal para controle de camadas
    grupo_principal = folium.FeatureGroup(name="📊 Análise por Setor")
    
    for setor in df['setor'].unique():
        df_setor = df[df['setor'] == setor]
        
        for idx, row in df_setor.iterrows():
            # Adaptar nomes de colunas
            nome_col = 'NO_FANTASIA' if 'NO_FANTASIA' in df.columns else 'NOME'
            endereco_col = 'NO_LOGRADOURO' if 'NO_LOGRADOURO' in df.columns else 'ENDERECO'
            bairro_col = 'NO_BAIRRO' if 'NO_BAIRRO' in df.columns else 'BAIRRO'
            
            popup_html = f"""
            <div style="width: 320px; font-family: Arial; line-height: 1.4;">
                <h4 style="color: {cores_setor[setor]}; margin-bottom: 10px; border-bottom: 2px solid {cores_setor[setor]};">
                    <b>{row.get(nome_col, 'N/A')}</b>
                </h4>
                <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                    <tr style="background-color: #f5f5f5;"><td style="padding: 4px;"><b>🏥 Tipo:</b></td><td style="padding: 4px;">{row.get('tipo_descricao', 'N/A')}</td></tr>
                    <tr><td style="padding: 4px;"><b>🏛️ Setor:</b></td><td style="padding: 4px; color: {cores_setor[setor]}; font-weight: bold;">{setor}</td></tr>
                    <tr style="background-color: #f5f5f5;"><td style="padding: 4px;"><b>📍 Endereço:</b></td><td style="padding: 4px;">{row.get(endereco_col, 'N/A')}</td></tr>
                    <tr><td style="padding: 4px;"><b>🏘️ Bairro:</b></td><td style="padding: 4px;">{row.get(bairro_col, 'N/A')}</td></tr>
                    <tr style="background-color: #f5f5f5;"><td style="padding: 4px;"><b>📏 Distância:</b></td><td style="padding: 4px;">{row.get('dist_centro', 0):.1f} km do centro</td></tr>
                    <tr><td style="padding: 4px;"><b>🗺️ Quadrante:</b></td><td style="padding: 4px;">{row.get('quadrante', 'N/A')}</td></tr>
                </table>
            </div>
            """
            
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{row.get(nome_col, 'N/A')} - {setor}",
                icon=folium.Icon(
                    color='red' if setor == 'Público' else 'blue',
                    icon='plus' if setor == 'Público' else 'info-sign'
                )
            ).add_to(grupo_principal)
    
    grupo_principal.add_to(mapa)
    print("   ✅ Camada por setor criada")
    
    # === CAMADA POR TIPO - ColorBrewer Dark2 ===
    print("⏳ [2/5] Adicionando camada por tipo de estabelecimento...")
    grupo_tipo = folium.FeatureGroup(name="🏥 Análise por Tipo", show=False)
    tipos_unicos = df['tipo_descricao'].unique()
    cores_tipo = {tipo: COLORBREWER_QUALITATIVE['Dark2_8'][i % 8] 
                  for i, tipo in enumerate(tipos_unicos)}
    
    for tipo in tipos_unicos:
        df_tipo = df[df['tipo_descricao'] == tipo]
        
        for idx, row in df_tipo.iterrows():
            nome_col = 'NO_FANTASIA' if 'NO_FANTASIA' in df.columns else 'NOME'
            
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=8,
                popup=f"<b>{row.get(nome_col, 'N/A')}</b><br>{tipo}<br>{row.get('dist_centro', 0):.1f}km",
                tooltip=f"{tipo}: {row.get(nome_col, 'N/A')}",
                color='black',
                fillColor=cores_tipo[tipo],
                fillOpacity=0.8,
                weight=2
            ).add_to(grupo_tipo)
    
    grupo_tipo.add_to(mapa)
    print("   ✅ Camada por tipo criada")
    
    # === CAMADA POR DISTÂNCIA - ColorBrewer BuGn ===
    print("⏳ [3/5] Adicionando camada por distância do centro...")
    grupo_distancia = folium.FeatureGroup(name="📏 Análise por Distância", show=False)
    categorias_dist = df['categoria_distancia'].dropna().unique()
    cores_distancia = {cat: COLORBREWER_SEQUENTIAL['BuGn_5'][i % 5] 
                      for i, cat in enumerate(categorias_dist)}
    
    for categoria in categorias_dist:
        df_dist = df[df['categoria_distancia'] == categoria]
        
        for idx, row in df_dist.iterrows():
            nome_col = 'NO_FANTASIA' if 'NO_FANTASIA' in df.columns else 'NOME'
            
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=6,
                popup=f"<b>{row.get(nome_col, 'N/A')}</b><br>{categoria}<br>{row.get('dist_centro', 0):.1f}km",
                tooltip=f"{categoria}",
                color='darkblue',
                fillColor=cores_distancia[categoria],
                fillOpacity=0.7,
                weight=1
            ).add_to(grupo_distancia)
    
    grupo_distancia.add_to(mapa)
    print("   ✅ Camada por distância criada")
    
    # === CAMADA DE CALOR ===
    print("⏳ [4/5] Gerando mapa de calor (densidade espacial)...")
    grupo_calor = folium.FeatureGroup(name="🔥 Mapa de Calor", show=False)
    
    # Mapa de calor geral
    heat_data = [[row[lat_col], row[lon_col], 1] 
                 for idx, row in df.iterrows()]
    
    HeatMap(
        heat_data,
        radius=20,
        blur=15,
        max_zoom=15,
        min_opacity=0.3
    ).add_to(grupo_calor)
    
    grupo_calor.add_to(mapa)
    print("   ✅ Mapa de calor criado")
    
    # === CAMADA DE REFERÊNCIAS ===
    print("⏳ [5/5] Adicionando referências geográficas (centro e raios)...")
    grupo_ref = folium.FeatureGroup(name="📍 Referências", show=True)
    
    # Centro da cidade
    folium.Marker(
        location=centro_concordia,
        popup='<b>🏛️ Centro de Concórdia</b><br>Ponto de referência da análise',
        tooltip='Centro da Cidade',
        icon=folium.Icon(color='black', icon='star', prefix='glyphicon')
    ).add_to(grupo_ref)
    
    # Círculos de distância com cores ColorBrewer
    raios_cores = [
        (2000, COLORBREWER_SEQUENTIAL['BuGn_5'][1], '2km'),
        (5000, COLORBREWER_SEQUENTIAL['BuGn_5'][2], '5km'),
        (10000, COLORBREWER_SEQUENTIAL['BuGn_5'][3], '10km'),
        (20000, COLORBREWER_SEQUENTIAL['BuGn_5'][4], '20km')
    ]
    
    for raio, cor, label in raios_cores:
        folium.Circle(
            centro_concordia,
            radius=raio,
            color=cor,
            fill=True,
            fillOpacity=0.1,
            weight=2,
            popup=f'Raio de {label}',
            tooltip=f'Área de {label} do centro'
        ).add_to(grupo_ref)
    
    grupo_ref.add_to(mapa)
    
    # === CONTROLE DE CAMADAS ===
    folium.LayerControl(collapsed=True, position='topleft').add_to(mapa)
    
    # === LEGENDAS CUSTOMIZADAS (múltiplas simultâneas com container) ===
    # Container fixo no topo-direito para empilhar as legendas, evitando sobreposição
    container_legendas_inicio = '''
    <div id="legendas-container" style="position: fixed; top: 10px; right: 10px; z-index: 10000;
         display: flex; flex-direction: column; gap: 10px; align-items: flex-end;">
    '''

    # LEGENDA 1: Setor
    legenda_setor_html = f'''
    <div id="legenda-setor" style="width: 200px; height: auto; 
                background-color: white; border:2px solid grey; 
                font-size:12px; padding: 15px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.3); display: none;">
    <h4 style="margin-top: 0; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 8px;">🏛️ Setor dos Estabelecimentos</h4>
    <div style="display: flex; align-items: center; margin: 10px 0;">
        <div style="width: 18px; height: 18px; background-color: {cores_setor['Público']}; margin-right: 10px; border-radius: 3px;"></div>
        <span style="font-weight: bold;">Público ({len(df[df['setor'] == 'Público'])})</span>
    </div>
    <div style="display: flex; align-items: center; margin: 10px 0;">
        <div style="width: 18px; height: 18px; background-color: {cores_setor['Privado']}; margin-right: 10px; border-radius: 3px;"></div>
        <span style="font-weight: bold;">Privado ({len(df[df['setor'] == 'Privado'])})</span>
    </div>
    <hr style="margin: 12px 0;">
    <div style="text-align: center; font-size: 11px; color: #666;">
        <b>Total:</b> {len(df)} estabelecimentos<br>
        <b>Dist. Média:</b> {df['dist_centro'].mean():.1f}km<br>
        <small style="color: #999;">ColorBrewer 2.0 | UFSC 2025</small>
    </div>
    </div>
    '''

    # LEGENDA 2: Tipos de Estabelecimentos
    legenda_tipo_items = ""
    for tipo in sorted(tipos_unicos):
        count = len(df[df['tipo_descricao'] == tipo])
        cor = cores_tipo[tipo]
        legenda_tipo_items += f'''
        <div style="display: flex; align-items: center; margin: 6px 0;">
            <div style="width: 16px; height: 16px; background-color: {cor}; margin-right: 8px; border-radius: 50%; border: 2px solid black;"></div>
            <span style="font-size: 11px;"><b>{tipo}</b> ({count})</span>
        </div>
        '''

    legenda_tipo_html = f'''
    <div id="legenda-tipo" style="width: 260px; height: auto; max-height: 85vh; overflow-y: auto;
                background-color: white; border:2px solid #7570b3; 
                font-size:12px; padding: 15px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
                display: none;">
    <h4 style="margin-top: 0; color: #7570b3; border-bottom: 2px solid #7570b3; padding-bottom: 8px;">🏥 Tipos de Estabelecimentos</h4>
    
    <div style="background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin-bottom: 10px; font-size: 10px;">
        <div style="margin-bottom: 4px;"><b>📖 Glossário:</b></div>
        <div style="margin-left: 5px; line-height: 1.4;">
            <b>ESF</b> = Estratégia de Saúde da Família<br>
            <small style="color: #555;">Equipes que atuam em áreas específicas</small>
        </div>
        <div style="margin-left: 5px; line-height: 1.4; margin-top: 3px;">
            <b>PS</b> = Posto de Saúde<br>
            <small style="color: #555;">Unidades básicas de atendimento</small>
        </div>
    </div>
    
    {legenda_tipo_items}
    <hr style="margin: 12px 0;">
    <div style="text-align: center; font-size: 11px; color: #666;">
        <small style="color: #999;">Clique nos marcadores para mais detalhes</small>
    </div>
    </div>
    '''

    # LEGENDA 3: Distância do Centro
    categorias_dist_sorted = sorted(df['categoria_distancia'].dropna().unique())
    legenda_dist_items = ""
    for cat in categorias_dist_sorted:
        count = len(df[df['categoria_distancia'] == cat])
        cor = cores_distancia[cat]
        legenda_dist_items += f'''
        <div style="display: flex; align-items: center; margin: 6px 0;">
            <div style="width: 16px; height: 16px; background-color: {cor}; margin-right: 8px; border-radius: 50%; border: 2px solid darkblue;"></div>
            <span style="font-size: 11px;"><b>{cat}</b> ({count})</span>
        </div>
        '''

    legenda_dist_html = f'''
    <div id="legenda-distancia" style="width: 220px; height: auto; 
                background-color: white; border:2px solid #238b45; 
                font-size:12px; padding: 15px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
                display: none;">
    <h4 style="margin-top: 0; color: #238b45; border-bottom: 2px solid #238b45; padding-bottom: 8px;">📏 Distância do Centro</h4>
    {legenda_dist_items}
    <hr style="margin: 12px 0;">
    <div style="text-align: center; font-size: 11px; color: #666;">
        <small style="color: #999;">Círculos de referência no mapa</small>
    </div>
    </div>
    '''

    container_legendas_fim = '</div>'

    # Script JavaScript para mostrar múltiplas legendas conforme overlays ativos
    script_legendas = '''
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        function atualizarLegendas() {
            var container = document.querySelector('.leaflet-control-layers-overlays');
            var checkboxes = container ? container.querySelectorAll('input.leaflet-control-layers-selector') : [];
            var labels = container ? container.querySelectorAll('label span') : [];

            var ativos = { setor: false, tipo: false, distancia: false };

            checkboxes.forEach(function(cb, i){
                if (!labels[i]) return;
                var texto = labels[i].textContent.trim();
                if (cb.checked) {
                    if (texto.includes('Tipo')) { ativos.tipo = true; }
                    if (texto.includes('Distância') || texto.includes('Distancia')) { ativos.distancia = true; }
                    if (texto.includes('Setor')) { ativos.setor = true; }
                }
            });

            var elSetor = document.getElementById('legenda-setor');
            var elTipo = document.getElementById('legenda-tipo');
            var elDist = document.getElementById('legenda-distancia');

            // Se nenhuma camada estiver ativa, mostrar Setor como padrão
            var nenhumAtivo = !ativos.setor && !ativos.tipo && !ativos.distancia;
            if (elSetor) elSetor.style.display = (ativos.setor || nenhumAtivo) ? 'block' : 'none';
            if (elTipo) elTipo.style.display = ativos.tipo ? 'block' : 'none';
            if (elDist) elDist.style.display = ativos.distancia ? 'block' : 'none';
        }

        // Rodar após montagem inicial
        setTimeout(atualizarLegendas, 500);

        // Listeners para mudanças
        var container = document.querySelector('.leaflet-control-layers-overlays');
        if (container) {
            container.addEventListener('change', function(){ setTimeout(atualizarLegendas, 50); });
            container.addEventListener('click', function(){ setTimeout(atualizarLegendas, 50); });
        }

        if (window.MutationObserver) {
            var ctrl = document.querySelector('.leaflet-control-layers');
            if (ctrl) {
                var obs = new MutationObserver(function(){ setTimeout(atualizarLegendas, 50); });
                obs.observe(ctrl, { childList: true, subtree: true, attributes: true });
            }
        }
    });
    </script>
    '''

    # Injetar container e legendas
    mapa.get_root().html.add_child(folium.Element(
        container_legendas_inicio + legenda_setor_html + legenda_tipo_html + legenda_dist_html + container_legendas_fim
    ))
    mapa.get_root().html.add_child(folium.Element(script_legendas))
    
    # === PLUGINS ADICIONAIS ===
    # Controle de medidas
    plugins.MeasureControl(position='topleft').add_to(mapa)
    
    # Fullscreen
    plugins.Fullscreen().add_to(mapa)
    
    # Mini mapa
    plugins.MiniMap(toggle_display=True).add_to(mapa)
    
    print("\n✅ MAPA INTERATIVO CONCLUÍDO!")
    print(f"   📊 {len(df)} estabelecimentos mapeados")
    print(f"   🎨 Paletas ColorBrewer aplicadas (BuGn, Set1, Dark2)")
    print(f"   🗺️ Camadas: Setor, Tipo, Distância, Calor, Referências")
    print("="*70 + "\n")
    
    return mapa

def gerar_dashboard_visual_simplificado(df):
    """Gera dashboard visual simplificado com matplotlib"""
    print("\n" + "="*70)
    print("📊 CRIANDO DASHBOARD VISUAL")
    print("="*70)
    print("⏳ Configurando gráficos...")
    
    # Configurar estilo
    plt.style.use('default')
    
    # Paletas ColorBrewer
    cores_sequencial = COLORBREWER_SEQUENTIAL['BuGn_5']
    cores_qualitativa = COLORBREWER_QUALITATIVE['Set1_8']
    
    # Criar figura principal
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('🏥 DASHBOARD COLORBREWER - ANÁLISE ESPACIAL ESTABELECIMENTOS DE SAÚDE\nConcórdia/SC', 
                 fontsize=18, fontweight='bold', y=0.96)
    
    # === GRÁFICO 1: Distribuição por Setor ===
    setor_counts = df['setor'].value_counts()
    colors_setor = [cores_qualitativa[i] for i in range(len(setor_counts))]
    
    explode = [0.05] + [0]*(len(setor_counts)-1) if len(setor_counts) > 0 else None
    wedges, texts, autotexts = axes[0,0].pie(
        setor_counts.values, 
        labels=setor_counts.index,
        colors=colors_setor,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode
    )
    axes[0,0].set_title('📊 Distribuição por Setor', fontsize=14, fontweight='bold')
    
    # === GRÁFICO 2: Tipos de Estabelecimentos ===
    tipo_counts = df['tipo_descricao'].value_counts().head(6)
    bars = axes[0,1].bar(range(len(tipo_counts)), tipo_counts.values, color=cores_qualitativa[:len(tipo_counts)])
    axes[0,1].set_title('🏥 Tipos de Estabelecimentos (Top 6)', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('Tipo de Estabelecimento')
    axes[0,1].set_ylabel('Quantidade')
    axes[0,1].set_xticks(range(len(tipo_counts)))
    axes[0,1].set_xticklabels(tipo_counts.index, rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for i, (bar, value) in enumerate(zip(bars, tipo_counts.values)):
        axes[0,1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # === GRÁFICO 3: Histograma de Distâncias ===
    # Histograma com cores sequenciais
    n, bins, patches = axes[0,2].hist(df['dist_centro'], bins=20, edgecolor='black', alpha=0.8)
    
    # Aplicar gradiente de cores
    fracs = n / n.max()
    for thisfrac, thispatch in zip(fracs, patches):
        color_idx = int(thisfrac * (len(cores_sequencial) - 1))
        thispatch.set_facecolor(cores_sequencial[color_idx])
    
    dist_media = df['dist_centro'].mean()
    axes[0,2].axvline(dist_media, color='red', linestyle='--', linewidth=2, 
                label=f'Média: {dist_media:.1f}km')
    axes[0,2].set_title('📏 Distribuição das Distâncias', fontsize=14, fontweight='bold')
    axes[0,2].set_xlabel('Distância (km)')
    axes[0,2].set_ylabel('Frequência')
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)
    
    # === GRÁFICO 4: Scatter Plot Geográfico ===
    # Identificar colunas de coordenadas
    lat_cols = [col for col in df.columns if 'LAT' in col.upper()]
    lon_cols = [col for col in df.columns if 'LON' in col.upper()]
    
    if lat_cols and lon_cols:
        lat_col, lon_col = lat_cols[0], lon_cols[0]
        
        # Scatter por setor
        for i, setor in enumerate(df['setor'].unique()):
            df_setor = df[df['setor'] == setor]
            axes[1,0].scatter(df_setor[lon_col], df_setor[lat_col], 
                           c=cores_qualitativa[i], label=setor, alpha=0.7, s=60)
        
        # Centro
        axes[1,0].scatter(-52.0238, -27.2335, c='black', marker='*', s=300, 
                   label='Centro', edgecolors='white', linewidth=2)
        
        axes[1,0].set_title('📍 Distribuição Geográfica', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Longitude')
        axes[1,0].set_ylabel('Latitude')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
    
    # === GRÁFICO 5: Categorias por Distância ===
    cat_dist_counts = df['categoria_distancia'].value_counts()
    bars = axes[1,1].barh(range(len(cat_dist_counts)), cat_dist_counts.values, 
                    color=cores_sequencial[:len(cat_dist_counts)])
    
    axes[1,1].set_title('📏 Categorias de Distância', fontsize=14, fontweight='bold')
    axes[1,1].set_xlabel('Quantidade')
    axes[1,1].set_yticks(range(len(cat_dist_counts)))
    axes[1,1].set_yticklabels(cat_dist_counts.index)
    
    for i, (bar, value) in enumerate(zip(bars, cat_dist_counts.values)):
        axes[1,1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2.,
                f'{value}', ha='left', va='center', fontweight='bold')
    
    # === GRÁFICO 6: Estatísticas Resumo ===
    axes[1,2].axis('off')
    
    # Calcular estatísticas
    total_est = len(df)
    publicos = len(df[df['eh_publico']])
    privados = total_est - publicos
    dist_media = df['dist_centro'].mean()
    mais_proximo = df['dist_centro'].min()
    mais_distante = df['dist_centro'].max()
    dentro_5km = len(df[df['dist_centro'] <= 5])
    
    stats_text = f'''ESTATÍSTICAS GERAIS

📊 Total: {total_est} estabelecimentos
🏛️ Públicos: {publicos} ({publicos/total_est*100:.1f}%)
🏢 Privados: {privados} ({privados/total_est*100:.1f}%)

📏 DISTÂNCIAS DO CENTRO
🎯 Média: {dist_media:.2f} km
📍 Mínima: {mais_proximo:.2f} km  
🚁 Máxima: {mais_distante:.2f} km
⭕ ≤ 5km: {dentro_5km} ({dentro_5km/total_est*100:.1f}%)

🎨 PALETAS COLORBREWER
• BuGn: Análise de distâncias
• Set1: Setor público/privado
• Dark2: Tipos de estabelecimentos

🗓️ Atualizado: Outubro 2025
'''
    
    axes[1,2].text(0.05, 0.95, stats_text, transform=axes[1,2].transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    
    # Salvar dashboard
    plt.savefig(os.path.join(OUTPUT_DIR, 'dashboard_colorbrewer_simplificado.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    
    print("✅ Dashboard visual simplificado gerado e salvo")
    return fig

def main():
    """Função principal do dashboard avançado"""
    print("\n" + "="*70)
    print("🚀 DASHBOARD AVANÇADO COM COLORBREWER E TREELAYERCONTROL")
    print("="*70)
    print("📅 Data: Outubro 2025 | 👤 Autor: Caetano Ronan | 🏫 Instituição: UFSC")
    print("="*70 + "\n")
    
    # 1. Carregar e processar dados
    df = carregar_dados()
    
    if df is None or len(df) == 0:
        print("❌ ERRO: Não foi possível carregar os dados")
        return None, None
    
    # 2. Gerar mapa avançado com ColorBrewer
    mapa_avancado = criar_mapa_avancado_colorbrewer(df)
    
    if mapa_avancado:
        print("💾 Salvando mapa interativo...")
        # Salvar mapa
    saida_mapa = os.path.join(MAPAS_DIR, 'mapa_avancado_colorbrewer.html')
    mapa_avancado.save(saida_mapa)
    print(f"   ✅ Mapa salvo: {saida_mapa}")
    
    # 3. Gerar dashboard visual simplificado
    print("\n⏳ Gerando visualizações gráficas...")
    try:
        fig_dashboard = gerar_dashboard_visual_simplificado(df)
        print("   ✅ Dashboard visual criado")
        plt.show()
    except Exception as e:
        print(f"   ⚠️ Aviso: Erro ao gerar dashboard visual: {e}")
    
    # 4. Salvar dados processados
    print("\n💾 Salvando dados processados...")
    saida_csv = os.path.join(OUTPUT_DIR, 'dados_processados_colorbrewer.csv')
    df.to_csv(saida_csv, index=False, encoding='utf-8')
    print(f"   ✅ Arquivo CSV salvo: {saida_csv}")
    
    # 5. Resumo final
    print("\n" + "="*70)
    print("✅ DASHBOARD CONCLUÍDO COM SUCESSO!")
    print("="*70)
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   • Total de estabelecimentos: {len(df)}")
    print(f"   • Estabelecimentos públicos: {len(df[df['eh_publico']])} ({len(df[df['eh_publico']])/len(df)*100:.1f}%)")
    print(f"   • Estabelecimentos privados: {len(df[~df['eh_publico']])} ({len(df[~df['eh_publico']])/len(df)*100:.1f}%)")
    print(f"   • Distância média do centro: {df['dist_centro'].mean():.2f}km")
    print(f"   • Distância mínima: {df['dist_centro'].min():.2f}km")
    print(f"   • Distância máxima: {df['dist_centro'].max():.2f}km")
    print(f"   • Dentro de 5km: {len(df[df['dist_centro'] <= 5])} ({len(df[df['dist_centro'] <= 5])/len(df)*100:.1f}%)")
    
    print(f"\n🎨 PALETAS COLORBREWER APLICADAS:")
    print(f"   • BuGn (Sequencial): Análise de distâncias")
    print(f"   • Set1 (Qualitativa): Diferenciação público/privado")
    print(f"   • Dark2 (Qualitativa): Tipos de estabelecimentos")
    
    print(f"\n📁 ARQUIVOS GERADOS:")
    print(f"   ✅ {os.path.join(MAPAS_DIR, 'mapa_avancado_colorbrewer.html')}")
    print(f"   ✅ {os.path.join(OUTPUT_DIR, 'dashboard_colorbrewer_simplificado.png')}")
    print(f"   ✅ {os.path.join(OUTPUT_DIR, 'dados_processados_colorbrewer.csv')}")
    
    print("\n" + "="*70)
    print("🎯 Projeto finalizado! Verifique os arquivos em 03_RESULTADOS/")
    print("="*70 + "\n")
    
    return df, mapa_avancado

if __name__ == "__main__":
    try:
        dados_finais, mapa_final = main()
        print("🎉 Execução concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        print("🔧 Executando versão de recuperação...")
        
        # Fallback simples
        dados_finais = criar_dados_sinteticos()
        print(f"✅ Dados sintéticos criados: {len(dados_finais)} estabelecimentos")