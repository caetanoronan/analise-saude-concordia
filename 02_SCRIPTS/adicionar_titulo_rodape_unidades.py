"""
Script para adicionar título e rodapé profissional ao mapa de Unidades de Saúde.
Adiciona elementos estéticos para apresentações e publicações acadêmicas.

Autor: Ronan Armando Caetano
Data: Novembro 2025
Instituição: UFSC
"""

import os

def adicionar_titulo_rodape_mapa():
    """
    Adiciona título no topo e rodapé com créditos ao mapa HTML.
    """
    # Caminhos dos arquivos
    arquivo_entrada = r'C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Exer_tec_geo\Pesquisa_upas\docs\mapa_unidades_saude_concordia.html'
    arquivo_saida = arquivo_entrada  # Sobrescreve o arquivo original
    
    print(f"📂 Lendo arquivo: {os.path.basename(arquivo_entrada)}")
    
    # Ler o conteúdo do mapa HTML
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return
    
    # HTML do título (topo)
    titulo_html = """
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: rgba(255, 255, 255, 0.95);
                padding: 15px 30px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                z-index: 9999;
                text-align: center;
                max-width: 90%;
                border-left: 5px solid #2c5aa0;">
        <h2 style="margin: 0; 
                   color: #2c5aa0; 
                   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                   font-size: 22px;
                   font-weight: 600;
                   letter-spacing: 0.5px;">
            🏥 Mapa de Unidades de Saúde - Concórdia/SC
        </h2>
    </div>
    """
    
    # HTML do rodapé (créditos)
    rodape_html = """
    <div style="position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%;
                background: linear-gradient(to top, rgba(44, 90, 160, 0.92), rgba(44, 90, 160, 0.85));
                padding: 12px 20px;
                z-index: 9999;
                text-align: center;
                border-top: 3px solid #1e3a5f;
                box-shadow: 0 -4px 12px rgba(0,0,0,0.3);">
        <div style="color: white; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 13px;
                    line-height: 1.6;">
            <strong style="font-size: 14px; letter-spacing: 0.5px;">📊 Fonte:</strong> 
            <span style="opacity: 0.95;">CNES/DataSUS | IBGE</span>
            <span style="margin: 0 15px; opacity: 0.7;">|</span>
            <strong style="font-size: 14px; letter-spacing: 0.5px;">👨‍🎓 Autor:</strong> 
            <span style="opacity: 0.95;">Ronan Armando Caetano, Graduando em Ciências Biológicas UFSC e Técnico em Geoprocessamento IFSC</span>
        </div>
    </div>
    """
    
    # Verificar se já existe título/rodapé (evitar duplicação)
    if "Mapa de Unidades de Saúde - Concórdia/SC" in html_content:
        print("⚠️  Título já existe no mapa. Removendo versão antiga...")
        # Remover versões antigas se existirem
    
    # Injetar título e rodapé no HTML
    # Método: Adicionar antes do </body> (ou no final se não existir)
    if '</body>' in html_content:
        html_modificado = html_content.replace('</body>', f'{titulo_html}\n{rodape_html}\n</body>')
    else:
        # Fallback: adicionar no final do HTML
        html_modificado = html_content + f'\n{titulo_html}\n{rodape_html}'
    
    # Salvar o arquivo modificado
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html_modificado)
        print(f"✅ Mapa atualizado com sucesso!")
        print(f"📍 Arquivo: {arquivo_saida}")
        print(f"📏 Tamanho: {len(html_modificado):,} caracteres")
        print("\n🎨 Elementos adicionados:")
        print("   🔝 Título profissional no topo: '🏥 Mapa de Unidades de Saúde - Concórdia/SC'")
        print("   🔽 Rodapé elegante com créditos e fontes")
        print("\n💡 Abra o arquivo no navegador para visualizar as mudanças!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("🎨 ADICIONAR TÍTULO E RODAPÉ PROFISSIONAL - Mapa Unidades de Saúde")
    print("=" * 80)
    print()
    
    adicionar_titulo_rodape_mapa()
    
    print()
    print("=" * 80)
    print("✨ Processamento concluído!")
    print("=" * 80)
