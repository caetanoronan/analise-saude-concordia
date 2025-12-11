#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script RÁPIDO para adicionar Limites ao mapa_avancado_treelayer_colorbrewer.html
Injeta camadas de limites diretamente no HTML existente

Autor: Caetano Ronan
Instituição: UFSC
Data: Novembro 2025
"""

import os
import geopandas as gpd
import json
import warnings
warnings.filterwarnings('ignore')

# Configurações de caminhos
ROOT_DIR = r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas'
MAPA_PATH = os.path.join(ROOT_DIR, 'docs', 'mapa_avancado_treelayer_colorbrewer.html')
OUTPUT_PATH = MAPA_PATH

print("\n" + "="*70)
print("  🗺️ ADICIONANDO LIMITES ADMINISTRATIVOS AO MAPA EXISTENTE")
print("="*70)

# Carregar limite estadual
print("\n📥 Carregando limite estadual...")
try:
    shp_sc = os.path.join(ROOT_DIR, "SC_Municipios_2024", "SC_Municipios_2024.shp")
    gdf_sc = gpd.read_file(shp_sc)
    if gdf_sc.crs.to_epsg() != 4326:
        gdf_sc = gdf_sc.to_crs(epsg=4326)
    
    # Dissolver e simplificar
    gdf_estado_proj = gdf_sc.to_crs(31982)
    gdf_estado = gdf_estado_proj.dissolve().reset_index(drop=True)
    gdf_estado['geometry'] = gdf_estado['geometry'].simplify(500)
    gdf_estado = gdf_estado.to_crs(4326)
    
    geojson_estado = json.loads(gdf_estado.to_json())
    print("   ✅ Limite estadual carregado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    geojson_estado = None

# Carregar limite municipal
print("📥 Carregando limite municipal de Concórdia...")
try:
    gdf_sc_mun = gpd.read_file(shp_sc)
    if gdf_sc_mun.crs.to_epsg() != 4326:
        gdf_sc_mun = gdf_sc_mun.to_crs(epsg=4326)
    
    # Filtrar Concórdia
    cod_cols = [c for c in gdf_sc_mun.columns if 'CD_MUN' in c.upper()]
    if cod_cols:
        gdf_concordia = gdf_sc_mun[gdf_sc_mun[cod_cols[0]].astype(str).str.contains('420430')].copy()
        
        # Simplificar
        gdf_proj = gdf_concordia.to_crs(31982)
        gdf_proj['geometry'] = gdf_proj['geometry'].simplify(100)
        gdf_concordia = gdf_proj.to_crs(4326)
        
        geojson_municipio = json.loads(gdf_concordia.to_json())
        print("   ✅ Limite municipal carregado")
    else:
        geojson_municipio = None
except Exception as e:
    print(f"   ❌ Erro: {e}")
    geojson_municipio = None

# Carregar municípios vizinhos
print("📥 Carregando municípios vizinhos...")
try:
    shp_regiao = os.path.join(ROOT_DIR, "SC_municipios_regiao_concordia.shp")
    gdf_regiao = gpd.read_file(shp_regiao)
    if gdf_regiao.crs.to_epsg() != 4326:
        gdf_regiao = gdf_regiao.to_crs(epsg=4326)
    
    # Filtrar vizinhos (excluir Concórdia)
    nome_cols = [c for c in gdf_regiao.columns if 'NM_MUN' in c.upper()]
    if nome_cols:
        gdf_vizinhos = gdf_regiao[~gdf_regiao[nome_cols[0]].str.upper().str.contains('CONCORD')].copy()
        
        # Simplificar
        gdf_proj = gdf_vizinhos.to_crs(31982)
        gdf_proj['geometry'] = gdf_proj['geometry'].simplify(200)
        gdf_vizinhos = gdf_proj.to_crs(4326)
        
        geojson_vizinhos = json.loads(gdf_vizinhos.to_json())
        print(f"   ✅ {len(gdf_vizinhos)} municípios vizinhos carregados")
    else:
        geojson_vizinhos = None
except Exception as e:
    print(f"   ❌ Erro: {e}")
    geojson_vizinhos = None

# Ler HTML existente
print("\n📖 Lendo mapa HTML existente...")
with open(MAPA_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Criar código JavaScript para adicionar camadas
js_code = """
<script>
// Adicionar camadas de limites administrativos
(function() {
    // Aguardar carregamento do mapa
    setTimeout(function() {
        var mapElement = document.querySelector('.folium-map');
        if (!mapElement || !mapElement._leaflet_id) {
            console.error('Mapa não encontrado');
            return;
        }
        
        var map = mapElement._leaflet_map || window[mapElement.id];
        if (!map) {
            console.error('Objeto mapa não disponível');
            return;
        }
        
        console.log('🗺️ Adicionando limites administrativos...');
"""

# Adicionar limite estadual
if geojson_estado:
    js_code += f"""
        // Limite Estadual de Santa Catarina
        var limiteEstadual = L.geoJSON({json.dumps(geojson_estado)}, {{
            style: {{
                color: '#41ab5d',
                weight: 2.5,
                fillColor: 'transparent',
                fillOpacity: 0,
                dashArray: '8, 4',
                lineCap: 'round'
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip('Estado de Santa Catarina', {{permanent: false}});
                layer.bindPopup('<div style="font-family: Arial; width: 250px;">' +
                    '<h4 style="color: #41ab5d; margin-bottom: 8px;">🗺️ <b>Santa Catarina</b></h4>' +
                    '<hr style="margin: 6px 0;"><table style="font-size: 12px; width: 100%;">' +
                    '<tr><td><b>Área:</b></td><td>~95.730 km²</td></tr>' +
                    '<tr><td><b>Municípios:</b></td><td>295</td></tr>' +
                    '<tr><td><b>Fonte:</b></td><td>IBGE 2024</td></tr></table></div>');
            }}
        }}).addTo(map);
        console.log('✅ Limite estadual adicionado');
"""

# Adicionar municípios vizinhos
if geojson_vizinhos:
    js_code += f"""
        // Municípios Vizinhos
        var municipiosVizinhos = L.geoJSON({json.dumps(geojson_vizinhos)}, {{
            style: {{
                color: '#969696',
                weight: 1.2,
                fillColor: '#e5e5e5',
                fillOpacity: 0.04,
                dashArray: '3, 6'
            }},
            onEachFeature: function(feature, layer) {{
                var nome = feature.properties.NM_MUN || feature.properties.NOME || 'Município';
                layer.bindTooltip(nome, {{permanent: false}});
                layer.bindPopup('<div style="font-family: Arial;"><h4 style="color: #636363;">' + 
                    nome + '</h4><p style="font-size: 11px; color: #999;">Município vizinho</p></div>');
                layer.on('mouseover', function() {{
                    this.setStyle({{weight: 2.5, fillOpacity: 0.15, color: '#636363'}});
                }});
                layer.on('mouseout', function() {{
                    this.setStyle({{weight: 1.2, fillOpacity: 0.04, color: '#969696'}});
                }});
            }}
        }}).addTo(map);
        console.log('✅ Municípios vizinhos adicionados');
"""

# Adicionar limite municipal (destaque)
if geojson_municipio:
    js_code += f"""
        // Limite Municipal de Concórdia (DESTAQUE)
        var limiteMunicipal = L.geoJSON({json.dumps(geojson_municipio)}, {{
            style: {{
                color: '#005a32',
                weight: 3.5,
                fillColor: '#a1d99b',
                fillOpacity: 0.12,
                lineJoin: 'round'
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip('<b>Município de Concórdia/SC</b>', {{
                    permanent: false,
                    style: 'font-size: 14px; font-weight: bold;'
                }});
                layer.bindPopup('<div style="font-family: Arial; width: 300px;">' +
                    '<h3 style="color: #005a32; margin-bottom: 10px; border-bottom: 3px solid #a1d99b; padding-bottom: 8px;">' +
                    '📍 <b>Município de Concórdia</b></h3>' +
                    '<table style="font-size: 13px; width: 100%; line-height: 1.8;">' +
                    '<tr><td style="width: 45%;"><b>🏛️ Estado:</b></td><td>Santa Catarina</td></tr>' +
                    '<tr><td><b>🔢 Código IBGE:</b></td><td>420430</td></tr>' +
                    '<tr><td><b>📏 Área:</b></td><td>~799,2 km²</td></tr>' +
                    '<tr><td><b>👥 População:</b></td><td>~75.000 hab (2022)</td></tr>' +
                    '<tr><td><b>🗺️ Microrregião:</b></td><td>Concórdia</td></tr>' +
                    '<tr><td><b>📊 Fonte:</b></td><td>IBGE 2024</td></tr></table>' +
                    '<hr style="margin: 12px 0;">' +
                    '<p style="font-size: 11px; color: #666; margin: 0;">' +
                    '💡 <i>Análise de estabelecimentos de saúde - UFSC</i></p></div>');
                layer.on('mouseover', function() {{
                    this.setStyle({{weight: 5.0, color: '#00441b', fillOpacity: 0.25}});
                }});
                layer.on('mouseout', function() {{
                    this.setStyle({{weight: 3.5, color: '#005a32', fillOpacity: 0.12}});
                }});
            }}
        }}).addTo(map);
        console.log('✅ Limite municipal adicionado');
        
        // Ajustar zoom para Concórdia
        map.fitBounds(limiteMunicipal.getBounds());
"""

js_code += """
        console.log('✅ Todas as camadas de limites adicionadas com sucesso!');
    }, 1000);
})();
</script>
"""

# Injetar antes do </body>
if '</body>' in html_content:
    html_content = html_content.replace('</body>', js_code + '\n</body>')
    print("   ✅ Código JavaScript injetado no HTML")
else:
    print("   ⚠️ Tag </body> não encontrada, adicionando ao final")
    html_content += js_code

# Salvar
print("\n💾 Salvando mapa atualizado...")
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"   ✅ Salvo em: {OUTPUT_PATH}")

print("\n📊 RESUMO")
print("="*70)
print(f"✓ Limite Estadual (SC): {'✅ ADICIONADO' if geojson_estado else '❌ NÃO DISPONÍVEL'}")
print(f"✓ Limite Municipal (Concórdia): {'✅ ADICIONADO' if geojson_municipio else '❌ NÃO DISPONÍVEL'}")
print(f"✓ Municípios Vizinhos: {'✅ ADICIONADOS' if geojson_vizinhos else '❌ NÃO DISPONÍVEIS'}")
print(f"✓ Padrões Cartográficos: ColorBrewer (IBGE)")
print("="*70)
print("\n✅ MAPA ATUALIZADO COM SUCESSO!")
print(f"\n📂 Abra o arquivo: {OUTPUT_PATH}\n")
