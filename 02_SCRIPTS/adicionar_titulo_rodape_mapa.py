#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar título e rodapé ao mapa HTML existente
"""

import os

# Caminho do arquivo
arquivo_html = r"C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas\docs\mapa_estabelecimentos_concordia.html"

# HTML do título
titulo_html = '''
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                width: auto;
                max-width: 90%;
                height: auto;
                background-color: white;
                border: 3px solid #238b45;
                border-radius: 10px;
                z-index: 9999;
                padding: 15px 25px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                text-align: center;
                font-family: 'Arial', sans-serif;">
        <h2 style="margin: 0; 
                   padding: 0; 
                   font-size: 22px; 
                   font-weight: bold; 
                   color: #00441b;
                   line-height: 1.3;">
            🏥 ANÁLISE ESPACIAL DOS ESTABELECIMENTOS DE SAÚDE
        </h2>
        <p style="margin: 5px 0 0 0; 
                  padding: 0; 
                  font-size: 16px; 
                  color: #238b45;
                  font-weight: 600;">
            Município de Concórdia/SC
        </p>
    </div>
'''

# HTML do rodapé
rodape_html = '''
    <div style="position: fixed; 
                bottom: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                width: auto;
                max-width: 95%;
                height: auto;
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid #238b45;
                border-radius: 8px;
                z-index: 9999;
                padding: 10px 20px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                text-align: center;
                font-family: 'Arial', sans-serif;">
        <p style="margin: 0; 
                  padding: 0; 
                  font-size: 12px; 
                  color: #333;
                  line-height: 1.6;">
            <b>Fonte:</b> CNES/DataSUS | IBGE | 
            <b>Autor:</b> Ronan Armando Caetano, Graduando em Ciências Biológicas UFSC e Técnico em Geoprocessamento IFSC
        </p>
    </div>
'''

print("📝 Adicionando título e rodapé ao mapa...")

# Ler o arquivo
with open(arquivo_html, 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Verificar se já tem título/rodapé
if 'ANÁLISE ESPACIAL DOS ESTABELECIMENTOS DE SAÚDE' in conteudo:
    print("⚠️ Título já existe no arquivo. Substituindo...")
    # Remover título antigo se existir
    if '<div style="position: fixed;' in conteudo and 'top: 10px;' in conteudo:
        inicio = conteudo.find('<div style="position: fixed;')
        if inicio != -1:
            fim = conteudo.find('</div>', inicio) + 6
            # Procurar próximo div fechado
            contador = 1
            i = inicio + len('<div')
            while i < len(conteudo) and contador > 0:
                if conteudo[i:i+4] == '<div':
                    contador += 1
                elif conteudo[i:i+6] == '</div>':
                    contador -= 1
                    if contador == 0:
                        fim = i + 6
                        break
                i += 1
            conteudo = conteudo[:inicio] + conteudo[fim:]

# Encontrar a posição antes do </script> final (ou </body>)
if '</script>\n</html>' in conteudo:
    pos_insercao = conteudo.rfind('</script>\n</html>')
elif '</body>' in conteudo:
    pos_insercao = conteudo.rfind('</body>')
else:
    pos_insercao = conteudo.rfind('</html>')

if pos_insercao == -1:
    print("❌ Erro: Não foi possível encontrar posição de inserção")
    exit(1)

# Inserir título e rodapé
novo_conteudo = conteudo[:pos_insercao] + titulo_html + '\n' + rodape_html + '\n' + conteudo[pos_insercao:]

# Salvar o arquivo
with open(arquivo_html, 'w', encoding='utf-8') as f:
    f.write(novo_conteudo)

print("✅ Título e rodapé adicionados com sucesso!")
print(f"📁 Arquivo atualizado: {arquivo_html}")
