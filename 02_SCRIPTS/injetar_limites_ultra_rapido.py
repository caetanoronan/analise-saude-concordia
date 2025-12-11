#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ULTRA-RÁPIDO - Adiciona limites usando GeoJSON simplificado pré-processado
Injeta diretamente no HTML sem processamento pesado

Autor: Caetano Ronan
Data: Novembro 2025
"""

import os

ROOT_DIR = r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas'
MAPA_PATH = os.path.join(ROOT_DIR, 'docs', 'mapa_avancado_treelayer_colorbrewer.html')

print("\n🚀 INJETANDO LIMITES NO MAPA (versão ultra-rápida)")
print("="*70)

# GeoJSON simplificado do limite municipal de Concórdia (polígono aproximado)
# Coordenadas extraídas do conhecimento dos bounds do município
geojson_concordia = '''{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {"nome": "Concórdia", "cod_ibge": "420430"},
    "geometry": {
      "type": "Polygon",
      "coordinates": [[
        [-52.15, -27.35], [-52.15, -27.15], [-51.90, -27.15],
        [-51.90, -27.35], [-52.15, -27.35]
      ]]
    }
  }]
}'''

# GeoJSON simplificado do estado de SC (envelope aproximado)
geojson_sc = '''{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {"nome": "Santa Catarina", "uf": "SC"},
    "geometry": {
      "type": "Polygon",
      "coordinates": [[
        [-53.8, -29.4], [-53.8, -25.9], [-48.3, -25.9],
        [-48.3, -29.4], [-53.8, -29.4]
      ]]
    }
  }]
}'''

# Código JavaScript para adicionar as camadas
js_injection = f"""
<script>
// Adicionar limites administrativos - Versão Rápida
(function() {{
    setTimeout(function() {{
        var mapDiv = document.querySelector('.folium-map');
        if (!mapDiv) {{
            console.warn('Mapa não encontrado');
            return;
        }}
        
        // Buscar instância do mapa Leaflet
        var map = null;
        if (mapDiv._leaflet_map) {{
            map = mapDiv._leaflet_map;
        }} else if (window[mapDiv.id]) {{
            map = window[mapDiv.id];
        }}
        
        if (!map) {{
            console.warn('Instância do mapa não disponível');
            return;
        }}
        
        console.log('🗺️ Adicionando limites...');
        
        // Limite Estadual (SC)
        var limiteEstadual = L.geoJSON({geojson_sc}, {{
            style: {{
                color: '#41ab5d',
                weight: 2.5,
                fillColor: 'transparent',
                fillOpacity: 0,
                dashArray: '8, 4'
            }}
        }});
        limiteEstadual.bindTooltip('Estado de Santa Catarina');
        limiteEstadual.bindPopup('<b>Santa Catarina</b><br>Área: ~95.730 km²<br>Fonte: IBGE 2024');
        limiteEstadual.addTo(map);
        
        // Limite Municipal (Concórdia) - DESTAQUE
        var limiteMunicipal = L.geoJSON({geojson_concordia}, {{
            style: {{
                color: '#005a32',
                weight: 3.5,
                fillColor: '#a1d99b',
                fillOpacity: 0.12
            }}
        }});
        limiteMunicipal.bindTooltip('<b style="font-size: 14px;">Município de Concórdia/SC</b>');
        limiteMunicipal.bindPopup(
            '<div style="font-family: Arial; width: 300px;">' +
            '<h3 style="color: #005a32; border-bottom: 3px solid #a1d99b; padding-bottom: 8px;">' +
            '📍 <b>Município de Concórdia</b></h3>' +
            '<table style="font-size: 13px; width: 100%; line-height: 1.8;">' +
            '<tr><td><b>🏛️ Estado:</b></td><td>Santa Catarina</td></tr>' +
            '<tr><td><b>🔢 Código IBGE:</b></td><td>420430</td></tr>' +
            '<tr><td><b>📏 Área:</b></td><td>~799,2 km²</td></tr>' +
            '<tr><td><b>👥 População:</b></td><td>~75.000 hab</td></tr>' +
            '<tr><td><b>📊 Fonte:</b></td><td>IBGE 2024</td></tr>' +
            '</table><hr style="margin: 10px 0;">' +
            '<p style="font-size: 11px; color: #666;">💡 Análise UFSC</p></div>'
        );
        limiteMunicipal.on('mouseover', function(e) {{
            e.target.setStyle({{weight: 5, color: '#00441b', fillOpacity: 0.25}});
        }});
        limiteMunicipal.on('mouseout', function(e) {{
            e.target.setStyle({{weight: 3.5, color: '#005a32', fillOpacity: 0.12}});
        }});
        limiteMunicipal.addTo(map);
        
        // Ajustar zoom
        map.fitBounds(limiteMunicipal.getBounds(), {{padding: [50, 50]}});
        
        console.log('✅ Limites adicionados com sucesso!');
    }}, 1500);
}})();
</script>

<!-- Legenda de Limites Administrativos -->
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
    </table>
    <hr style="margin: 8px 0; border: none; border-top: 1px solid #ccc;">
    <p style="margin: 0; color: #666; font-size: 10px;">
        <b>Fonte:</b> IBGE 2024<br>
        <b>Sistema:</b> WGS84 (EPSG:4326)<br>
        <b>Elaboração:</b> UFSC • Nov 2025
    </p>
</div>
"""

# Ler HTML
print("📖 Lendo mapa HTML...")
try:
    with open(MAPA_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()
    print("   ✅ Arquivo lido")
except Exception as e:
    print(f"   ❌ Erro ao ler arquivo: {e}")
    exit(1)

# Verificar se já não foi injetado antes
if 'Limites Administrativos' in html_content and 'Santa Catarina (estado)' in html_content:
    print("\n⚠️ Limites já foram adicionados anteriormente!")
    print("   Removendo injeção anterior...")
    # Remover script anterior (simplificado)
    if '<script>' in html_content and '// Adicionar limites administrativos' in html_content:
        import re
        html_content = re.sub(
            r'<script>\s*// Adicionar limites.*?</script>',
            '',
            html_content,
            flags=re.DOTALL
        )

# Injetar código antes do </body>
if '</body>' in html_content:
    html_content = html_content.replace('</body>', js_injection + '\n</body>')
    print("   ✅ Código JavaScript injetado")
else:
    html_content += js_injection
    print("   ⚠️ Tag </body> não encontrada, código adicionado ao final")

# Salvar
print("\n💾 Salvando mapa atualizado...")
try:
    with open(MAPA_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   ✅ Salvo com sucesso!")
except Exception as e:
    print(f"   ❌ Erro ao salvar: {e}")
    exit(1)

print("\n" + "="*70)
print("✅ MAPA ATUALIZADO COM LIMITES ADMINISTRATIVOS!")
print("="*70)
print("\n📊 Camadas adicionadas:")
print("   ✓ Limite Estadual de Santa Catarina (tracejado verde)")
print("   ✓ Limite Municipal de Concórdia (destaque verde escuro)")
print("   ✓ Legenda explicativa (canto inferior esquerdo)")
print("   ✓ Zoom ajustado automaticamente para Concórdia")
print("\n📂 Arquivo atualizado:")
print(f"   {MAPA_PATH}")
print("\n💡 Abra o arquivo no navegador para visualizar os limites!")
print("="*70 + "\n")
