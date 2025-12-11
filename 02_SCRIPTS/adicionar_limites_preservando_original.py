#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ADICIONAR limites ao mapa existente SEM remover conteúdo original
Apenas injeta camadas de limites mantendo todos os estabelecimentos de saúde

Autor: Caetano Ronan
Data: Novembro 2025
"""

import os
import geopandas as gpd
import json
import warnings
warnings.filterwarnings('ignore')

ROOT_DIR = r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas'
MAPA_PATH = os.path.join(ROOT_DIR, 'docs', 'mapa_avancado_treelayer_colorbrewer.html')
BACKUP_PATH = os.path.join(ROOT_DIR, 'docs', 'mapa_avancado_treelayer_colorbrewer_BACKUP.html')

print("\n" + "="*70)
print("  🗺️ ADICIONANDO LIMITES AO MAPA (mantendo conteúdo original)")
print("="*70)

# Fazer backup do arquivo original
print("\n💾 Criando backup do mapa original...")
try:
    with open(MAPA_PATH, 'r', encoding='utf-8') as f:
        original_content = f.read()
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"   ✅ Backup salvo em: {BACKUP_PATH}")
except Exception as e:
    print(f"   ❌ Erro ao criar backup: {e}")
    exit(1)

# Carregar shapefiles e gerar GeoJSON
print("\n📥 Carregando dados geoespaciais...")

# Limite estadual
geojson_estado = None
try:
    shp_sc = os.path.join(ROOT_DIR, "SC_Municipios_2024", "SC_Municipios_2024.shp")
    print("   → Processando limite estadual...")
    gdf_sc = gpd.read_file(shp_sc)
    if gdf_sc.crs.to_epsg() != 4326:
        gdf_sc = gdf_sc.to_crs(epsg=4326)
    
    gdf_estado_proj = gdf_sc.to_crs(31982)
    gdf_estado = gdf_estado_proj.dissolve().reset_index(drop=True)
    gdf_estado['geometry'] = gdf_estado['geometry'].simplify(500)
    gdf_estado = gdf_estado.to_crs(4326)
    
    geojson_estado = json.loads(gdf_estado.to_json())
    print("      ✅ Limite estadual processado")
except Exception as e:
    print(f"      ⚠️ Erro: {e}")

# Limite municipal
geojson_municipio = None
try:
    print("   → Processando limite municipal...")
    gdf_sc_mun = gpd.read_file(shp_sc)
    if gdf_sc_mun.crs.to_epsg() != 4326:
        gdf_sc_mun = gdf_sc_mun.to_crs(epsg=4326)
    
    cod_cols = [c for c in gdf_sc_mun.columns if 'CD_MUN' in c.upper()]
    if cod_cols:
        gdf_concordia = gdf_sc_mun[gdf_sc_mun[cod_cols[0]].astype(str).str.contains('420430')].copy()
        
        gdf_proj = gdf_concordia.to_crs(31982)
        gdf_proj['geometry'] = gdf_proj['geometry'].simplify(100)
        gdf_concordia = gdf_proj.to_crs(4326)
        
        geojson_municipio = json.loads(gdf_concordia.to_json())
        print("      ✅ Limite municipal processado")
except Exception as e:
    print(f"      ⚠️ Erro: {e}")

# Municípios vizinhos
geojson_vizinhos = None
nome_col = 'NM_MUN'
try:
    print("   → Processando municípios vizinhos...")
    shp_regiao = os.path.join(ROOT_DIR, "SC_municipios_regiao_concordia.shp")
    gdf_regiao = gpd.read_file(shp_regiao)
    if gdf_regiao.crs.to_epsg() != 4326:
        gdf_regiao = gdf_regiao.to_crs(epsg=4326)
    
    nome_cols = [c for c in gdf_regiao.columns if 'NM_MUN' in c.upper() or 'NOME' in c.upper()]
    if nome_cols:
        nome_col = nome_cols[0]
        gdf_vizinhos = gdf_regiao[~gdf_regiao[nome_col].str.upper().str.contains('CONCORD')].copy()
        
        gdf_proj = gdf_vizinhos.to_crs(31982)
        gdf_proj['geometry'] = gdf_proj['geometry'].simplify(200)
        gdf_vizinhos = gdf_proj.to_crs(4326)
        
        geojson_vizinhos = json.loads(gdf_vizinhos.to_json())
        print(f"      ✅ {len(gdf_vizinhos)} municípios vizinhos processados")
except Exception as e:
    print(f"      ⚠️ Erro: {e}")

# Criar código JavaScript para ADICIONAR camadas ao mapa existente
print("\n🔧 Gerando código de injeção...")

js_code = """
<script>
// ============================================================================
// ADICIONAR LIMITES ADMINISTRATIVOS AO MAPA EXISTENTE
// Mantém todos os estabelecimentos de saúde e adiciona camadas de limites
// ============================================================================
(function() {
    setTimeout(function() {
        // Buscar mapa Leaflet existente
        var mapDiv = document.querySelector('.folium-map');
        if (!mapDiv) {
            console.error('❌ Mapa não encontrado');
            return;
        }
        
        var map = mapDiv._leaflet_map || window[mapDiv.id];
        if (!map) {
            console.error('❌ Instância do mapa não disponível');
            return;
        }
        
        console.log('🗺️ Adicionando camadas de limites ao mapa existente...');
        
        // Criar grupos de camadas para limites
        var grupoLimitesAdministrativos = L.featureGroup();
"""

# Adicionar limite estadual
if geojson_estado:
    js_code += f"""
        // === CAMADA: Limite Estadual de Santa Catarina ===
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
                layer.bindPopup(
                    '<div style="font-family: Arial; width: 250px;">' +
                    '<h4 style="color: #41ab5d; margin-bottom: 8px;">🗺️ <b>Santa Catarina</b></h4>' +
                    '<hr style="margin: 6px 0;">' +
                    '<table style="font-size: 12px; width: 100%;">' +
                    '<tr><td><b>Área:</b></td><td>~95.730 km²</td></tr>' +
                    '<tr><td><b>Municípios:</b></td><td>295</td></tr>' +
                    '<tr><td><b>Fonte:</b></td><td>IBGE 2024</td></tr>' +
                    '</table></div>'
                );
            }}
        }});
        limiteEstadual.addTo(grupoLimitesAdministrativos);
        console.log('   ✅ Limite estadual adicionado');
"""

# Adicionar municípios vizinhos
if geojson_vizinhos:
    js_code += f"""
        // === CAMADA: Municípios Vizinhos ===
        var vizinhosData = {json.dumps(geojson_vizinhos)};
        vizinhosData.features.forEach(function(feature) {{
            var nomeMun = feature.properties['{nome_col}'] || feature.properties.NOME || 'Município';
            
            L.geoJSON(feature, {{
                style: {{
                    color: '#969696',
                    weight: 1.2,
                    fillColor: '#e5e5e5',
                    fillOpacity: 0.04,
                    dashArray: '3, 6'
                }},
                onEachFeature: function(feat, layer) {{
                    layer.bindTooltip(nomeMun, {{permanent: false}});
                    layer.bindPopup(
                        '<div style="font-family: Arial; width: 200px;">' +
                        '<h4 style="color: #636363; margin-bottom: 8px;"><b>' + nomeMun + '</b></h4>' +
                        '<hr style="margin: 6px 0;">' +
                        '<p style="font-size: 11px; color: #999;">Município vizinho</p>' +
                        '</div>'
                    );
                    layer.on('mouseover', function(e) {{
                        e.target.setStyle({{weight: 2.5, fillOpacity: 0.15, color: '#636363'}});
                    }});
                    layer.on('mouseout', function(e) {{
                        e.target.setStyle({{weight: 1.2, fillOpacity: 0.04, color: '#969696'}});
                    }});
                }}
            }}).addTo(grupoLimitesAdministrativos);
        }});
        console.log('   ✅ Municípios vizinhos adicionados');
"""

# Adicionar limite municipal (destaque)
if geojson_municipio:
    js_code += f"""
        // === CAMADA: Limite Municipal de Concórdia (DESTAQUE) ===
        var limiteMunicipal = L.geoJSON({json.dumps(geojson_municipio)}, {{
            style: {{
                color: '#005a32',
                weight: 3.5,
                fillColor: '#a1d99b',
                fillOpacity: 0.12,
                lineJoin: 'round'
            }},
            onEachFeature: function(feature, layer) {{
                layer.bindTooltip(
                    '<b style="font-size: 14px;">Município de Concórdia/SC</b>',
                    {{permanent: false}}
                );
                layer.bindPopup(
                    '<div style="font-family: Arial; width: 300px;">' +
                    '<h3 style="color: #005a32; margin-bottom: 10px; border-bottom: 3px solid #a1d99b; padding-bottom: 8px;">' +
                    '📍 <b>Município de Concórdia</b></h3>' +
                    '<table style="font-size: 13px; width: 100%; line-height: 1.8;">' +
                    '<tr><td style="width: 45%;"><b>🏛️ Estado:</b></td><td>Santa Catarina</td></tr>' +
                    '<tr><td><b>🔢 Código IBGE:</b></td><td>420430</td></tr>' +
                    '<tr><td><b>📏 Área:</b></td><td>~799,2 km²</td></tr>' +
                    '<tr><td><b>👥 População:</b></td><td>~75.000 hab (2022)</td></tr>' +
                    '<tr><td><b>🗺️ Microrregião:</b></td><td>Concórdia</td></tr>' +
                    '<tr><td><b>📊 Fonte:</b></td><td>IBGE 2024</td></tr>' +
                    '</table>' +
                    '<hr style="margin: 12px 0;">' +
                    '<p style="font-size: 11px; color: #666; margin: 0;">' +
                    '💡 <i>Análise de estabelecimentos de saúde - UFSC</i></p>' +
                    '</div>'
                );
                layer.on('mouseover', function(e) {{
                    e.target.setStyle({{weight: 5.0, color: '#00441b', fillOpacity: 0.25}});
                }});
                layer.on('mouseout', function(e) {{
                    e.target.setStyle({{weight: 3.5, color: '#005a32', fillOpacity: 0.12}});
                }});
            }}
        }});
        limiteMunicipal.addTo(grupoLimitesAdministrativos);
        console.log('   ✅ Limite municipal adicionado (destaque)');
"""

js_code += """
        // Adicionar grupo de limites ao mapa
        grupoLimitesAdministrativos.addTo(map);
        
        // Enviar camadas para trás (atrás dos marcadores de estabelecimentos)
        grupoLimitesAdministrativos.bringToBack();
        
        console.log('✅ LIMITES ADMINISTRATIVOS ADICIONADOS COM SUCESSO!');
        console.log('   → Todas as camadas originais foram mantidas');
        console.log('   → Limites adicionados como camada de fundo');
        
    }, 2000); // Aguardar 2 segundos para garantir que o mapa carregou
})();
</script>

<!-- Legenda de Limites Administrativos -->
<div style="position: fixed; 
            bottom: 80px; 
            left: 10px;
            width: 280px;
            background-color: rgba(255,255,255,0.95);
            border: 2px solid #005a32;
            border-radius: 8px;
            z-index: 9998;
            padding: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            font-family: Arial;
            font-size: 11px;">
    <h4 style="margin: 0 0 8px 0; color: #005a32; font-size: 13px; border-bottom: 2px solid #a1d99b; padding-bottom: 5px;">
        📊 Limites Administrativos
    </h4>
    <table style="width: 100%; font-size: 11px; line-height: 1.8;">
        <tr>
            <td style="width: 25px;">
                <div style="width: 20px; height: 3px; background: #005a32; border-radius: 2px;"></div>
            </td>
            <td><b>Concórdia</b> (município)</td>
        </tr>
        <tr>
            <td>
                <div style="width: 20px; height: 2px; background: #41ab5d; border: 1px dashed #41ab5d;"></div>
            </td>
            <td>Santa Catarina (estado)</td>
        </tr>
        <tr>
            <td>
                <div style="width: 20px; height: 2px; background: #969696; opacity: 0.6;"></div>
            </td>
            <td>Municípios vizinhos</td>
        </tr>
    </table>
    <hr style="margin: 8px 0; border: none; border-top: 1px solid #ccc;">
    <p style="margin: 0; color: #666; font-size: 10px;">
        <b>Fonte:</b> IBGE 2024<br>
        <b>Sistema:</b> WGS84 (EPSG:4326)<br>
        <b>Elaboração:</b> UFSC • Nov 2025
    </p>
</div>
"""

# Injetar código no HTML ANTES do </body>
print("💉 Injetando código no HTML...")
if '</body>' in original_content:
    modified_content = original_content.replace('</body>', js_code + '\n</body>')
    print("   ✅ Código injetado antes do </body>")
else:
    modified_content = original_content + js_code
    print("   ⚠️ Tag </body> não encontrada, adicionando ao final")

# Salvar arquivo modificado
print("\n💾 Salvando mapa atualizado...")
try:
    with open(MAPA_PATH, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print(f"   ✅ Arquivo salvo com sucesso!")
except Exception as e:
    print(f"   ❌ Erro ao salvar: {e}")
    exit(1)

print("\n" + "="*70)
print("✅ LIMITES ADICIONADOS AO MAPA COM SUCESSO!")
print("="*70)
print("\n📊 Resumo:")
print(f"   ✓ Limite Estadual (SC): {'✅ ADICIONADO' if geojson_estado else '❌ FALHOU'}")
print(f"   ✓ Limite Municipal (Concórdia): {'✅ ADICIONADO' if geojson_municipio else '❌ FALHOU'}")
print(f"   ✓ Municípios Vizinhos: {'✅ ADICIONADOS' if geojson_vizinhos else '❌ FALHARAM'}")
print("   ✓ Estabelecimentos de saúde: ✅ MANTIDOS (conteúdo original preservado)")
print("   ✓ Marcadores e clusters: ✅ MANTIDOS")
print("   ✓ Camadas temáticas: ✅ MANTIDAS")
print("\n📂 Arquivos:")
print(f"   • Mapa atualizado: {MAPA_PATH}")
print(f"   • Backup original: {BACKUP_PATH}")
print("\n💡 Abra o mapa no navegador para ver os limites + estabelecimentos!")
print("="*70 + "\n")
