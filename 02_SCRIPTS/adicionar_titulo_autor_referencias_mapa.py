"""
Script para adicionar título, autor e referências ao mapa interativo avançado
Autor: Ronan Armando Caetano
Data: Novembro 2025
"""

import os

# Caminho do arquivo HTML
arquivo_mapa = r'docs\mapa_avancado_treelayer_colorbrewer.html'

# Verificar se arquivo existe
if not os.path.exists(arquivo_mapa):
    print(f"❌ Arquivo não encontrado: {arquivo_mapa}")
    exit(1)

print(f"📂 Processando arquivo: {arquivo_mapa}")
print(f"📊 Tamanho: {os.path.getsize(arquivo_mapa) / (1024*1024):.2f} MB")

# Ler conteúdo do arquivo
print("🔄 Lendo arquivo...")
with open(arquivo_mapa, 'r', encoding='utf-8') as f:
    html_content = f.read()

# CSS para título e rodapé
css_titulo_rodape = """
    <style>
        /* Título do Mapa */
        .map-title {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            text-align: center;
            max-width: 90%;
            border-left: 5px solid #2c7fb8;
        }
        
        .map-title h1 {
            margin: 0 0 5px 0;
            font-size: 22px;
            color: #1a1a1a;
            font-weight: 700;
            line-height: 1.3;
        }
        
        .map-title p {
            margin: 0;
            font-size: 14px;
            color: #666;
            font-weight: 400;
        }
        
        /* Rodapé com Autor e Referências */
        .map-footer {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.95);
            padding: 12px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            text-align: center;
            max-width: 95%;
            border-top: 3px solid #41b6c4;
            font-size: 12px;
            line-height: 1.6;
        }
        
        .map-footer .author {
            margin: 0 0 8px 0;
            font-weight: 600;
            color: #1a1a1a;
            font-size: 13px;
        }
        
        .map-footer .author i {
            color: #2c7fb8;
            margin-right: 5px;
        }
        
        .map-footer .references {
            margin: 0;
            color: #666;
            font-size: 11px;
            border-top: 1px solid #e0e0e0;
            padding-top: 8px;
        }
        
        .map-footer .references strong {
            color: #333;
            font-weight: 600;
        }
        
        /* Responsividade para mobile */
        @media (max-width: 768px) {
            .map-title {
                padding: 10px 15px;
                top: 5px;
            }
            
            .map-title h1 {
                font-size: 16px;
            }
            
            .map-title p {
                font-size: 11px;
            }
            
            .map-footer {
                padding: 8px 15px;
                font-size: 10px;
                bottom: 5px;
            }
            
            .map-footer .author {
                font-size: 11px;
            }
            
            .map-footer .references {
                font-size: 9px;
            }
        }
    </style>
"""

# HTML do título
html_titulo = """
    <div class="map-title">
        <h1>📍 Análise Espacial dos Estabelecimentos de Saúde - Concórdia/SC</h1>
        <p>Mapa Interativo com Limites Administrativos e Distribuição Geoespacial</p>
    </div>
"""

# HTML do rodapé com autor e referências
html_rodape = """
    <div class="map-footer">
        <p class="author">
            <i class="fas fa-user-graduate"></i>
            <strong>Autor:</strong> Ronan Armando Caetano | 
            Graduando em Ciências Biológicas (UFSC) | 
            Técnico em Geoprocessamento (IFSC)
        </p>
        <p class="references">
            <strong>Fontes de Dados:</strong> CNES/DataSUS (Estabelecimentos de Saúde) | 
            IBGE 2024 (Malha Municipal de Santa Catarina) | 
            OpenStreetMap (Mapa Base) • 
            <strong>Ferramentas:</strong> Python 3.x, GeoPandas, Folium, QGIS • 
            <strong>Sistema de Coordenadas:</strong> WGS84 (EPSG:4326) • 
            <strong>Município:</strong> Concórdia/SC (IBGE: 420430) • 
            <strong>Data:</strong> Novembro 2025
        </p>
    </div>
"""

# Procurar tag </head> para inserir CSS
if '</head>' in html_content:
    print("✅ Tag </head> encontrada")
    html_content = html_content.replace('</head>', f'{css_titulo_rodape}\n</head>')
else:
    print("⚠️ Tag </head> não encontrada")

# Procurar tag <body> ou estrutura do mapa para inserir título
# Folium usa <div class="folium-map" ou similar
if '<body>' in html_content:
    print("✅ Tag <body> encontrada")
    html_content = html_content.replace('<body>', f'<body>\n{html_titulo}')
elif '<div class="folium-map"' in html_content:
    print("✅ Div folium-map encontrada")
    # Inserir antes do div principal do mapa
    html_content = html_content.replace('<div class="folium-map"', f'{html_titulo}\n<div class="folium-map"')
else:
    print("⚠️ Estrutura body não encontrada claramente")

# Procurar tag </body> para inserir rodapé
if '</body>' in html_content:
    print("✅ Tag </body> encontrada")
    html_content = html_content.replace('</body>', f'{html_rodape}\n</body>')
else:
    print("⚠️ Tag </body> não encontrada")

# Salvar arquivo modificado
print("💾 Salvando arquivo modificado...")
with open(arquivo_mapa, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "="*80)
print("✅ MAPA ATUALIZADO COM SUCESSO!")
print("="*80)
print(f"""
📋 Modificações realizadas:

1. ✅ Título adicionado ao topo do mapa
   - "Análise Espacial dos Estabelecimentos de Saúde - Concórdia/SC"
   - Subtítulo com descrição do conteúdo

2. ✅ Rodapé com informações completas:
   - Autor: Ronan Armando Caetano
   - Credenciais: Graduando Ciências Biológicas (UFSC) + Técnico Geoprocessamento (IFSC)
   - Fontes de dados: CNES/DataSUS, IBGE 2024, OpenStreetMap
   - Ferramentas: Python, GeoPandas, Folium, QGIS
   - Sistema de coordenadas: WGS84 (EPSG:4326)
   - Município: Concórdia/SC (IBGE: 420430)
   - Data: Novembro 2025

3. ✅ Design responsivo (adapta para mobile)

4. ✅ Estilo profissional com bordas coloridas

🌐 Arquivo pronto para visualização:
   {os.path.abspath(arquivo_mapa)}
""")
print("="*80)
