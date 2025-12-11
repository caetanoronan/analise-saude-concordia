#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script MINIMALISTA - Apenas injeta JavaScript para adicionar limites
NÃO MODIFICA NADA do mapa existente, apenas adiciona código JavaScript no final

Autor: Caetano Ronan  
Data: Novembro 2025
"""

import os
import geopandas as gpd
import json

ROOT = r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas'
MAPA = os.path.join(ROOT, 'docs', 'mapa_avancado_treelayer_colorbrewer.html')

print("\n🗺️ ADICIONANDO LIMITES (injeção minimalista)")
print("="*70)

# Carregar shapefiles
print("📥 Processando shapefiles...")
shp_sc = os.path.join(ROOT, "SC_Municipios_2024", "SC_Municipios_2024.shp")

# Limite estadual
gdf_sc = gpd.read_file(shp_sc).to_crs(4326)
gdf_estado = gdf_sc.to_crs(31982).dissolve().reset_index(drop=True)
gdf_estado['geometry'] = gdf_estado['geometry'].simplify(500)
gdf_estado = gdf_estado.to_crs(4326)
geojson_estado = gdf_estado.to_json()

# Limite municipal
cod_col = [c for c in gdf_sc.columns if 'CD_MUN' in c.upper()][0]
gdf_conc = gdf_sc[gdf_sc[cod_col].astype(str).str.contains('420430')].copy()
gdf_conc = gdf_conc.to_crs(31982)
gdf_conc['geometry'] = gdf_conc['geometry'].simplify(100)
gdf_conc = gdf_conc.to_crs(4326)
geojson_municipio = gdf_conc.to_json()

# Municípios vizinhos
shp_reg = os.path.join(ROOT, "SC_municipios_regiao_concordia.shp")
gdf_reg = gpd.read_file(shp_reg).to_crs(4326)
nome_col = [c for c in gdf_reg.columns if 'NM_MUN' in c.upper()][0]
gdf_viz = gdf_reg[~gdf_reg[nome_col].str.upper().str.contains('CONCORD')].copy()
gdf_viz = gdf_viz.to_crs(31982)
gdf_viz['geometry'] = gdf_viz['geometry'].simplify(200)
gdf_viz = gdf_viz.to_crs(4326)
geojson_vizinhos = gdf_viz.to_json()

print("   ✅ Dados processados")

# JavaScript para injetar
js = f"""
<script>
(function() {{
    setTimeout(function() {{
        var map = document.querySelector('.folium-map')._leaflet_map;
        if (!map) return;
        
        // Limite Estadual
        L.geoJSON({geojson_estado}, {{
            style: {{color: '#41ab5d', weight: 2.5, fillOpacity: 0, dashArray: '8,4'}}
        }}).bindTooltip('Santa Catarina').addTo(map).bringToBack();
        
        // Municípios Vizinhos
        var viz = {geojson_vizinhos};
        viz.features.forEach(f => {{
            L.geoJSON(f, {{
                style: {{color: '#969696', weight: 1.2, fillColor: '#e5e5e5', fillOpacity: 0.04, dashArray: '3,6'}}
            }}).bindTooltip(f.properties.{nome_col}).addTo(map).bringToBack();
        }});
        
        // Limite Municipal
        L.geoJSON({geojson_municipio}, {{
            style: {{color: '#005a32', weight: 3.5, fillColor: '#a1d99b', fillOpacity: 0.12}}
        }}).bindTooltip('<b>Município de Concórdia/SC</b>').addTo(map).bringToBack();
        
        console.log('✅ Limites adicionados');
    }}, 2000);
}})();
</script>
"""

# Ler e injetar
print("💉 Injetando código...")
with open(MAPA, 'r', encoding='utf-8') as f:
    html = f.read()

if '✅ Limites adicionados' not in html:
    html = html.replace('</body>', js + '</body>')
    with open(MAPA, 'w', encoding='utf-8') as f:
        f.write(html)
    print("   ✅ Código injetado!")
else:
    print("   ⚠️ Limites já foram adicionados")

print("\n✅ CONCLUÍDO! Abra o mapa no navegador")
print("="*70 + "\n")
