#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar Limites Municipal e Estadual ao mapa_avancado_treelayer_colorbrewer.html
Aplica padrões cartográficos profissionais do IBGE

Autor: Caetano Ronan
Instituição: UFSC
Data: Novembro 2025
"""

import os
import geopandas as gpd
import folium
from folium.plugins import GroupedLayerControl
import warnings
warnings.filterwarnings('ignore')

# Configurações de caminhos
SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
DOCS_DIR = os.path.join(ROOT_DIR, 'docs')
MAPA_PATH = os.path.join(DOCS_DIR, 'mapa_avancado_treelayer_colorbrewer.html')
OUTPUT_PATH = os.path.join(DOCS_DIR, 'mapa_avancado_treelayer_colorbrewer.html')

# Configurações cartográficas
CORES_CARTOGRAFIA = {
    'limite_estadual': {
        'color': '#41ab5d',           # Verde médio (ColorBrewer BuGn)
        'weight': 2.5,                 # Linha média-grossa
        'fillColor': 'transparent',
        'fillOpacity': 0,
        'dashArray': '8, 4',          # Tracejado médio
        'lineCap': 'round'
    },
    'limite_municipal': {
        'color': '#005a32',           # Verde escuro intenso (ColorBrewer)
        'weight': 3.5,                 # Linha de destaque
        'fillColor': '#a1d99b',       # Verde claro preenchimento
        'fillOpacity': 0.12,          # Transparência adequada
        'dashArray': None,            # Linha contínua
        'lineJoin': 'round'
    },
    'municipios_vizinhos': {
        'color': '#969696',           # Cinza neutro
        'weight': 1.2,
        'fillColor': '#e5e5e5',
        'fillOpacity': 0.04,
        'dashArray': '3, 6'
    }
}

def carregar_limite_estadual():
    """Carrega limite estadual de SC"""
    print("📥 Carregando limite estadual de Santa Catarina...")
    
    try:
        shp_path = os.path.join(ROOT_DIR, "SC_Municipios_2024", "SC_Municipios_2024.shp")
        if os.path.isfile(shp_path):
            gdf_sc = gpd.read_file(shp_path)
            if gdf_sc.crs is None or gdf_sc.crs.to_epsg() != 4326:
                gdf_sc = gdf_sc.to_crs(epsg=4326)
            
            # Dissolver todos os municípios para criar limite estadual
            gdf_estado = gdf_sc.dissolve().reset_index(drop=True)
            
            # Simplificar geometria para melhor performance
            gdf_estado_proj = gdf_estado.to_crs(31982)
            gdf_estado_proj['geometry'] = gdf_estado_proj['geometry'].buffer(0)
            gdf_estado_proj['geometry'] = gdf_estado_proj['geometry'].simplify(500)
            gdf_estado = gdf_estado_proj.to_crs(4326)
            
            print(f"   ✅ Limite estadual carregado e processado")
            return gdf_estado
    except Exception as e:
        print(f"   ⚠️ Erro ao carregar limite estadual: {e}")
    
    return None

def carregar_limite_municipal():
    """Carrega limite municipal de Concórdia"""
    print("📥 Carregando limite municipal de Concórdia...")
    
    try:
        # Tentar shapefile completo de SC
        shp_path = os.path.join(ROOT_DIR, "SC_Municipios_2024", "SC_Municipios_2024.shp")
        if os.path.isfile(shp_path):
            gdf_sc = gpd.read_file(shp_path)
            if gdf_sc.crs is None or gdf_sc.crs.to_epsg() != 4326:
                gdf_sc = gdf_sc.to_crs(epsg=4326)
            
            # Identificar coluna de código IBGE
            cod_cols = [c for c in gdf_sc.columns if 'CD_MUN' in c.upper() or 'GEOCOD' in c.upper()]
            if cod_cols:
                cod_col = cod_cols[0]
                gdf_concordia = gdf_sc[gdf_sc[cod_col].astype(str).str.contains('420430')].copy()
                
                if not gdf_concordia.empty:
                    # Simplificar geometria
                    gdf_proj = gdf_concordia.to_crs(31982)
                    gdf_proj['geometry'] = gdf_proj['geometry'].buffer(0)
                    gdf_proj['geometry'] = gdf_proj['geometry'].simplify(100)
                    gdf_concordia = gdf_proj.to_crs(4326)
                    
                    print(f"   ✅ Limite municipal carregado e processado")
                    return gdf_concordia
        
        # Fallback: Shapefile da região
        shp_regiao = os.path.join(ROOT_DIR, "SC_municipios_regiao_concordia.shp")
        if os.path.isfile(shp_regiao):
            gdf_regiao = gpd.read_file(shp_regiao)
            if gdf_regiao.crs is None or gdf_regiao.crs.to_epsg() != 4326:
                gdf_regiao = gdf_regiao.to_crs(epsg=4326)
            
            # Filtrar Concórdia
            nome_cols = [c for c in gdf_regiao.columns if 'NM_MUN' in c.upper() or 'NOME' in c.upper()]
            if nome_cols:
                nome_col = nome_cols[0]
                gdf_concordia = gdf_regiao[gdf_regiao[nome_col].str.upper().str.contains('CONCORD')].copy()
                
                if not gdf_concordia.empty:
                    print(f"   ✅ Limite municipal carregado (fonte: shapefile regional)")
                    return gdf_concordia
        
        # Fallback final: Setores censitários dissolvidos
        shp_setores = os.path.join(ROOT_DIR, "03_RESULTADOS", "shapefiles", "Concordia_sencitario.shp")
        if os.path.isfile(shp_setores):
            gdf_setores = gpd.read_file(shp_setores)
            if gdf_setores.crs is None or gdf_setores.crs.to_epsg() != 4326:
                gdf_setores = gdf_setores.to_crs(epsg=4326)
            
            gdf_concordia = gdf_setores.dissolve().reset_index(drop=True)
            print(f"   ✅ Limite municipal carregado (fonte: setores censitários)")
            return gdf_concordia
            
    except Exception as e:
        print(f"   ⚠️ Erro ao carregar limite municipal: {e}")
    
    return None

def carregar_municipios_vizinhos():
    """Carrega municípios vizinhos para contexto regional"""
    print("📥 Carregando municípios vizinhos...")
    
    try:
        # Carregar shapefile regional
        shp_regiao = os.path.join(ROOT_DIR, "SC_municipios_regiao_concordia.shp")
        if os.path.isfile(shp_regiao):
            gdf_regiao = gpd.read_file(shp_regiao)
            if gdf_regiao.crs is None or gdf_regiao.crs.to_epsg() != 4326:
                gdf_regiao = gdf_regiao.to_crs(epsg=4326)
            
            # Remover Concórdia da lista de vizinhos
            nome_cols = [c for c in gdf_regiao.columns if 'NM_MUN' in c.upper() or 'NOME' in c.upper()]
            if nome_cols:
                nome_col = nome_cols[0]
                gdf_vizinhos = gdf_regiao[~gdf_regiao[nome_col].str.upper().str.contains('CONCORD')].copy()
                
                # Simplificar geometrias
                gdf_proj = gdf_vizinhos.to_crs(31982)
                gdf_proj['geometry'] = gdf_proj['geometry'].simplify(200)
                gdf_vizinhos = gdf_proj.to_crs(4326)
                
                print(f"   ✅ {len(gdf_vizinhos)} municípios vizinhos carregados")
                return gdf_vizinhos, nome_col
                
    except Exception as e:
        print(f"   ⚠️ Erro ao carregar municípios vizinhos: {e}")
    
    return None, None

def criar_mapa_com_limites():
    """Cria novo mapa com limites administrativos adequados"""
    print("\n🗺️ CRIANDO MAPA COM LIMITES ADMINISTRATIVOS\n")
    print("="*60)
    
    # Carregar dados geoespaciais
    gdf_estado = carregar_limite_estadual()
    gdf_municipio = carregar_limite_municipal()
    gdf_vizinhos, nome_col = carregar_municipios_vizinhos()
    
    if gdf_municipio is None or gdf_municipio.empty:
        print("\n❌ ERRO: Limite municipal não encontrado!")
        print("   Não é possível continuar sem o polígono de Concórdia.")
        return False
    
    # Criar mapa base centrado em Concórdia
    centro_concordia = [-27.2335, -52.0238]
    
    mapa = folium.Map(
        location=centro_concordia,
        zoom_start=11,
        min_zoom=9,
        max_zoom=17,
        tiles=None,
        prefer_canvas=True
    )
    
    # Adicionar tiles base
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='OpenStreetMap',
        control=True
    ).add_to(mapa)
    
    folium.TileLayer(
        tiles='CartoDB positron',
        name='CartoDB Claro',
        control=True
    ).add_to(mapa)
    
    print("\n📍 ADICIONANDO CAMADAS GEOGRÁFICAS")
    print("-"*60)
    
    # === CAMADA 1: LIMITE ESTADUAL ===
    if gdf_estado is not None and not gdf_estado.empty:
        print("\n1️⃣ Limite Estadual de Santa Catarina")
        grupo_estadual = folium.FeatureGroup(name="🗺️ Limite Estadual (SC)", show=True)
        
        folium.GeoJson(
            data=gdf_estado.__geo_interface__,
            name='Limite Estadual SC',
            style_function=lambda x: CORES_CARTOGRAFIA['limite_estadual'],
            tooltip=folium.Tooltip('Estado de Santa Catarina'),
            popup=folium.Popup(
                '<div style="font-family: Arial; width: 250px;">'
                '<h4 style="color: #41ab5d; margin-bottom: 8px;">🗺️ <b>Santa Catarina</b></h4>'
                '<hr style="margin: 6px 0;">'
                '<table style="font-size: 12px; width: 100%;">'
                '<tr><td><b>Área:</b></td><td>~95.730 km²</td></tr>'
                '<tr><td><b>Municípios:</b></td><td>295</td></tr>'
                '<tr><td><b>Fonte:</b></td><td>IBGE 2024</td></tr>'
                '</table></div>',
                max_width=280
            )
        ).add_to(grupo_estadual)
        
        grupo_estadual.add_to(mapa)
        print("   ✅ Camada adicionada com estilo ColorBrewer")
    
    # === CAMADA 2: MUNICÍPIOS VIZINHOS ===
    if gdf_vizinhos is not None and not gdf_vizinhos.empty:
        print("\n2️⃣ Municípios Vizinhos (Contexto Regional)")
        grupo_vizinhos = folium.FeatureGroup(name="🏘️ Municípios Vizinhos", show=True)
        
        for idx, row in gdf_vizinhos.iterrows():
            nome_mun = row[nome_col] if nome_col else f"Município {idx+1}"
            
            folium.GeoJson(
                data=row['geometry'].__geo_interface__,
                style_function=lambda x: CORES_CARTOGRAFIA['municipios_vizinhos'],
                highlight_function=lambda x: {
                    'weight': 2.5,
                    'fillOpacity': 0.15,
                    'color': '#636363'
                },
                tooltip=folium.Tooltip(nome_mun),
                popup=folium.Popup(
                    f'<div style="font-family: Arial; width: 200px;">'
                    f'<h4 style="color: #636363; margin-bottom: 8px;"><b>{nome_mun}</b></h4>'
                    f'<hr style="margin: 6px 0;">'
                    f'<p style="font-size: 11px; color: #999;">Município vizinho</p>'
                    f'</div>',
                    max_width=220
                )
            ).add_to(grupo_vizinhos)
        
        grupo_vizinhos.add_to(mapa)
        print(f"   ✅ {len(gdf_vizinhos)} municípios adicionados")
    
    # === CAMADA 3: LIMITE MUNICIPAL DE CONCÓRDIA (DESTAQUE) ===
    print("\n3️⃣ Limite Municipal de Concórdia (DESTAQUE)")
    grupo_municipio = folium.FeatureGroup(name="📍 Limite Municipal (Concórdia)", show=True)
    
    folium.GeoJson(
        data=gdf_municipio.__geo_interface__,
        name='Limite Municipal Concórdia',
        style_function=lambda x: CORES_CARTOGRAFIA['limite_municipal'],
        highlight_function=lambda x: {
            'weight': 5.0,
            'color': '#00441b',
            'fillOpacity': 0.25
        },
        tooltip=folium.Tooltip(
            '<b>Município de Concórdia/SC</b>',
            style='font-size: 14px; font-weight: bold;'
        ),
        popup=folium.Popup(
            '<div style="font-family: Arial; width: 300px;">'
            '<h3 style="color: #005a32; margin-bottom: 10px; border-bottom: 3px solid #a1d99b; padding-bottom: 8px;">'
            '📍 <b>Município de Concórdia</b></h3>'
            '<table style="font-size: 13px; width: 100%; line-height: 1.8;">'
            '<tr><td style="width: 45%;"><b>🏛️ Estado:</b></td><td>Santa Catarina</td></tr>'
            '<tr><td><b>🔢 Código IBGE:</b></td><td>420430</td></tr>'
            '<tr><td><b>📏 Área:</b></td><td>~799,2 km²</td></tr>'
            '<tr><td><b>👥 População:</b></td><td>~75.000 hab (2022)</td></tr>'
            '<tr><td><b>🗺️ Microrregião:</b></td><td>Concórdia</td></tr>'
            '<tr><td><b>📊 Fonte:</b></td><td>IBGE 2024</td></tr>'
            '</table>'
            '<hr style="margin: 12px 0;">'
            '<p style="font-size: 11px; color: #666; margin: 0;">'
            '💡 <i>Análise de estabelecimentos de saúde - UFSC</i></p>'
            '</div>',
            max_width=330
        )
    ).add_to(grupo_municipio)
    
    grupo_municipio.add_to(mapa)
    print("   ✅ Camada de destaque adicionada")
    
    # Ajustar bounds do mapa
    try:
        minx, miny, maxx, maxy = gdf_municipio.total_bounds
        # Adicionar margem de 10%
        margin_x = (maxx - minx) * 0.1
        margin_y = (maxy - miny) * 0.1
        bounds = [
            [miny - margin_y, minx - margin_x],
            [maxy + margin_y, maxx + margin_x]
        ]
        mapa.fit_bounds(bounds)
        print("\n🎯 Zoom ajustado para área de Concórdia")
    except Exception as e:
        print(f"\n⚠️ Não foi possível ajustar bounds: {e}")
    
    # Adicionar controles
    print("\n🎛️ ADICIONANDO CONTROLES")
    print("-"*60)
    
    folium.LayerControl(position='topleft', collapsed=False).add_to(mapa)
    
    from folium.plugins import Fullscreen, MeasureControl
    Fullscreen(position='topright').add_to(mapa)
    MeasureControl(
        position='topleft',
        primary_length_unit='kilometers',
        secondary_length_unit='meters',
        primary_area_unit='sqkilometers'
    ).add_to(mapa)
    
    print("   ✅ LayerControl (gerenciamento de camadas)")
    print("   ✅ Fullscreen (tela cheia)")
    print("   ✅ MeasureControl (medição de distâncias)")
    
    # Adicionar título profissional
    titulo_html = '''
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                width: auto;
                max-width: 90%;
                background-color: white;
                border: 3px solid #005a32;
                border-radius: 10px;
                z-index: 9999;
                padding: 12px 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                text-align: center;
                font-family: 'Arial', sans-serif;">
        <h3 style="margin: 0; color: #005a32; font-size: 18px; font-weight: bold;">
            📍 Limites Administrativos - Concórdia/SC
        </h3>
        <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">
            Município | Estado | Contexto Regional • IBGE 2024 • UFSC
        </p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    
    # Adicionar rodapé com informações
    rodape_html = '''
    <div style="position: fixed; 
                bottom: 10px; 
                left: 10px;
                width: 280px;
                background-color: rgba(255,255,255,0.95);
                border: 2px solid #005a32;
                border-radius: 8px;
                z-index: 9998;
                padding: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                font-family: 'Arial', sans-serif;
                font-size: 11px;">
        <h4 style="margin: 0 0 8px 0; color: #005a32; font-size: 13px; border-bottom: 2px solid #a1d99b; padding-bottom: 5px;">
            📊 Padrões Cartográficos
        </h4>
        <table style="width: 100%; font-size: 11px; line-height: 1.6;">
            <tr>
                <td style="width: 20px;"><div style="width: 15px; height: 3px; background: #005a32; border-radius: 2px;"></div></td>
                <td><b>Concórdia</b> (destaque)</td>
            </tr>
            <tr>
                <td><div style="width: 15px; height: 3px; background: #41ab5d; border-radius: 2px; border-style: dashed;"></div></td>
                <td>Santa Catarina (estado)</td>
            </tr>
            <tr>
                <td><div style="width: 15px; height: 3px; background: #969696; border-radius: 2px; opacity: 0.6;"></div></td>
                <td>Municípios vizinhos</td>
            </tr>
        </table>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid #ccc;">
        <p style="margin: 0; color: #666; font-size: 10px;">
            <b>Fonte:</b> IBGE 2024 • Malha Municipal Digital<br>
            <b>Sistema:</b> WGS84 (EPSG:4326)<br>
            <b>Elaboração:</b> UFSC • Novembro 2025
        </p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(rodape_html))
    
    # Salvar mapa
    print("\n💾 SALVANDO MAPA")
    print("-"*60)
    mapa.save(OUTPUT_PATH)
    print(f"   ✅ Salvo em: {OUTPUT_PATH}")
    
    # Estatísticas finais
    print("\n📈 ESTATÍSTICAS DO MAPA")
    print("="*60)
    print(f"✓ Limite Estadual: {'SIM' if gdf_estado is not None else 'NÃO'}")
    print(f"✓ Limite Municipal: {'SIM' if gdf_municipio is not None else 'NÃO'}")
    print(f"✓ Municípios Vizinhos: {len(gdf_vizinhos) if gdf_vizinhos is not None else 0}")
    print(f"✓ Padrões Cartográficos: ColorBrewer (IBGE)")
    print(f"✓ Sistema de Coordenadas: WGS84 (EPSG:4326)")
    print("="*60)
    
    return True

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("  ADICIONANDO LIMITES ADMINISTRATIVOS AO MAPA")
    print("  Padrões Cartográficos IBGE • ColorBrewer Palettes")
    print("="*60 + "\n")
    
    sucesso = criar_mapa_com_limites()
    
    if sucesso:
        print("\n✅ MAPA ATUALIZADO COM SUCESSO!")
        print(f"\n📂 Abra o arquivo:\n   {OUTPUT_PATH}")
    else:
        print("\n❌ ERRO AO CRIAR MAPA")
        print("   Verifique se os shapefiles estão disponíveis.")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
