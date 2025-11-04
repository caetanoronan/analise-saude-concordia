import csv
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2

# Função para calcular distância
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Critérios para identificar postos públicos
def eh_posto_publico(nome_fantasia, tipo_unidade, razao_social):
    nome = str(nome_fantasia).upper()
    razao = str(razao_social).upper()
    
    # Critérios para postos públicos
    criterios = [
        # Nomes típicos de unidades públicas
        'ESF' in nome,                    # Estratégia Saúde da Família
        'PS' in nome,                     # Posto de Saúde
        'POSTO' in nome and 'SAUDE' in nome,
        'UBS' in nome,                    # Unidade Básica de Saúde
        'UNIDADE BASICA' in nome,
        'UNIDADE DE SAUDE' in nome,
        'CENTRO DE SAUDE' in nome,
        'CENTRO DE ATENCAO' in nome,
        'CAPS' in nome,                   # Centro de Atenção Psicossocial
        'POLICLINICA' in nome,
        'SAMU' in nome,
        'SECRETARIA DE SAUDE' in razao,
        'PREFEITURA' in razao,
        'MUNICIPIO' in razao,
        'FUNDO MUNICIPAL' in razao,
        
        # Tipos de unidade que são tipicamente públicos
        str(tipo_unidade) in ['1', '2', '4', '5', '39', '40', '42', '70', '71', '72', '73']
    ]
    
    return any(criterios)

# Ler o arquivo CSV
unidades_publicas = []
centro_concordia = [-27.2335, -52.0238]

with open('Tabela_estado_SC.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    
    for row in reader:
        if row.get('CO_MUNICIPIO_GESTOR') == '420430':  # Concórdia
            try:
                lat = float(row.get('NU_LATITUDE', 0))
                lon = float(row.get('NU_LONGITUDE', 0))
                if lat != 0 and lon != 0:
                    # Verificar se é posto público
                    if eh_posto_publico(
                        row.get('NO_FANTASIA', ''),
                        row.get('TP_UNIDADE', ''),
                        row.get('NO_RAZAO_SOCIAL', '')
                    ):
                        # Calcular distância do centro
                        dist_centro = calcular_distancia(centro_concordia[0], centro_concordia[1], lat, lon)
                        
                        unidades_publicas.append({
                            'nome': row.get('NO_FANTASIA', 'N/A'),
                            'lat': lat,
                            'lon': lon,
                            'endereco': row.get('NO_LOGRADOURO', 'N/A'),
                            'bairro': row.get('NO_BAIRRO', 'N/A'),
                            'tipo': row.get('TP_UNIDADE', 'N/A'),
                            'razao_social': row.get('NO_RAZAO_SOCIAL', 'N/A'),
                            'dist_centro': dist_centro
                        })
            except (ValueError, TypeError):
                continue

# ANÁLISE DOS POSTOS PÚBLICOS
print("="*60)
print("ANÁLISE DOS POSTOS PÚBLICOS DE SAÚDE - CONCÓRDIA")
print("="*60)
print(f"Total de unidades públicas mapeadas: {len(unidades_publicas)}")

# Estatísticas
if unidades_publicas:
    distancias = [u['dist_centro'] for u in unidades_publicas]
    print(f"\nDistância média do centro: {sum(distancias)/len(distancias):.2f} km")
    print(f"Posto mais próximo: {min(distancias):.2f} km")
    print(f"Posto mais distante: {max(distancias):.2f} km")
    
    unidades_5km = sum(1 for d in distancias if d <= 5)
    print(f"Postos dentro de 5km do centro: {unidades_5km}/{len(unidades_publicas)}")
    
    # Análise por tipo
    print(f"\nDistribuição por tipo de unidade:")
    tipos = {}
    for unidade in unidades_publicas:
        tipo = unidade['tipo']
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"Tipo {tipo}: {count} unidades")
    
    # Mostrar todos os postos públicos
    print(f"\nLISTA COMPLETA DOS POSTOS PÚBLICOS:")
    for i, unidade in enumerate(unidades_publicas, 1):
        print(f"{i:2d}. {unidade['nome']} | {unidade['bairro']} | {unidade['dist_centro']:.1f} km | Tipo: {unidade['tipo']}")
    
else:
    print("Nenhum posto público encontrado!")

# CRIAR MAPA DOS POSTOS PÚBLICOS
if unidades_publicas:
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>POSTOS PÚBLICOS DE SAÚDE - Concórdia/SC</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map {{ height: 600px; }}
            .info {{ padding: 10px; background: white; border-radius: 5px; margin: 10px; }}
            .legend {{ background: white; padding: 10px; border-radius: 5px; position: absolute; bottom: 20px; left: 20px; z-index: 1000; }}
        </style>
    </head>
    <body>
        <h1>POSTOS PÚBLICOS DE SAÚDE - Concórdia/SC</h1>
        <div class="info">
            <h3>Total de postos públicos: {len(unidades_publicas)}</h3>
            <p>Postos dentro de 5km do centro: {unidades_5km}</p>
            <p>Distância média do centro: {sum(distancias)/len(distancias):.1f} km</p>
        </div>
        <div id="map"></div>

        <script>
            // Mapa centrado em Concórdia
            var map = L.map('map').setView([-27.2335, -52.0238], 13);
            
            // Camada do mapa
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap'
            }}).addTo(map);

            // Adicionar círculo de 5km
            L.circle([-27.2335, -52.0238], {{
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.2,
                radius: 5000
            }}).addTo(map).bindPopup("Raio de 5km do centro");

            // Adicionar marcador do centro
            L.marker([-27.2335, -52.0238])
                .bindPopup("<b>Centro de Concórdia</b>")
                .addTo(map);

            // Adicionar postos públicos
            var unidades = {unidades_publicas};
            
            // Cores por tipo de unidade
            function getColor(tipo) {{
                var colors = {{
                    '1': 'green',    // Posto de Saúde
                    '2': 'blue',     // Centro de Saúde
                    '4': 'red',      // Policlínica
                    '5': 'orange',   // Hospital
                    '39': 'purple',  // Laboratório
                    '42': 'brown',   // SAMU
                    '70': 'pink',    // CAPS
                    '71': 'cyan'     // Consultório Especializado
                }};
                return colors[tipo] || 'gray';
            }}
            
            unidades.forEach(function(unidade) {{
                var marker = L.marker([unidade.lat, unidade.lon])
                    .bindPopup("<b>" + unidade.nome + "</b><br>" + 
                              unidade.endereco + "<br>" + 
                              unidade.bairro + "<br>" +
                              "Tipo: " + unidade.tipo + "<br>" +
                              "Distância do centro: " + unidade.dist_centro.toFixed(1) + " km")
                    .addTo(map);
                
                // Destacar postos dentro de 5km
                if (unidade.dist_centro <= 5) {{
                    marker.setIcon(L.icon({{
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    }}));
                }}
            }});
            
            // Legenda
            var legend = L.control({{position: 'bottomright'}});
            legend.onAdd = function (map) {{
                var div = L.DomUtil.create('div', 'info legend');
                div.innerHTML = '<h4>Legenda</h4>' +
                    '<div style="background-color: green; width: 20px; height: 20px; display: inline-block;"></div> ≤ 5km do centro<br>' +
                    '<div style="background-color: blue; width: 20px; height: 20px; display: inline-block;"></div> > 5km do centro<br>' +
                    '<div style="border: 2px solid red; width: 20px; height: 20px; display: inline-block; background-color: rgba(255,0,0,0.2);"></div> Raio 5km';
                return div;
            }};
            legend.addTo(map);
        </script>
    </body>
    </html>
    '''

    # Salvar e abrir
    with open('mapa_postos_publicos_concordia.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nMapa dos postos públicos gerado: mapa_postos_publicos_concordia.html")
    webbrowser.open('file://' + os.path.abspath('mapa_postos_publicos_concordia.html'))