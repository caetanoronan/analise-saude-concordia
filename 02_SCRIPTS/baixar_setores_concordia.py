#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para baixar setores censitários de Concórdia/SC (IBGE Censo 2022)
e prepará-los para uso nos mapas de análise espacial.

Autor: GitHub Copilot + Ronan Caetano
Data: Novembro 2025
"""

import os
import requests
import zipfile
import geopandas as gpd
from pathlib import Path

# Configurações
ROOT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "01_DADOS" / "processados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Código IBGE de Concórdia: 420430
CODIGO_CONCORDIA = "420430"

def baixar_setores_ibge():
    """
    Baixa os setores censitários de Santa Catarina do FTP do IBGE.
    Censo Demográfico 2022.
    """
    print("📥 Baixando setores censitários de SC do IBGE...")
    
    # URL do arquivo de setores de SC (Censo 2022)
    # Fonte: https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2022/
    url_setores_sc = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2022/UFs/SC/sc_setores_censitarios_2022.zip"
    
    zip_path = OUTPUT_DIR / "sc_setores_2022.zip"
    
    try:
        print(f"   → Baixando de {url_setores_sc}")
        response = requests.get(url_setores_sc, stream=True, timeout=300)
        response.raise_for_status()
        
        # Salvar o zip
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"   ✅ Arquivo baixado: {zip_path} ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")
        return zip_path
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro ao baixar: {e}")
        return None

def extrair_e_filtrar_concordia(zip_path):
    """
    Extrai o shapefile e filtra apenas os setores de Concórdia.
    """
    print("📂 Extraindo e filtrando setores de Concórdia...")
    
    extract_dir = OUTPUT_DIR / "setores_sc_temp"
    extract_dir.mkdir(exist_ok=True)
    
    try:
        # Extrair ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        print("   ✅ Arquivos extraídos")
        
        # Encontrar o shapefile principal
        shp_files = list(extract_dir.rglob("*.shp"))
        if not shp_files:
            print("   ❌ Nenhum shapefile encontrado no ZIP")
            return None
        
        shp_path = shp_files[0]
        print(f"   → Carregando shapefile: {shp_path.name}")
        
        # Carregar shapefile completo de SC
        gdf_sc = gpd.read_file(shp_path)
        print(f"   ✅ {len(gdf_sc)} setores carregados (SC completo)")
        
        # Filtrar apenas Concórdia
        # Procurar coluna com código do município
        cod_mun_cols = [c for c in gdf_sc.columns if 'CD_MUN' in c.upper() or 'CODMUN' in c.upper()]
        
        if not cod_mun_cols:
            print(f"   ⚠️ Colunas disponíveis: {list(gdf_sc.columns)}")
            print("   ⚠️ Tentando filtro por primeiros 6 dígitos do código do setor...")
            # Fallback: usar CD_SETOR e pegar primeiros 6 dígitos
            setor_cols = [c for c in gdf_sc.columns if 'CD_SETOR' in c.upper() or 'GEOCODIGO' in c.upper()]
            if setor_cols:
                gdf_concordia = gdf_sc[gdf_sc[setor_cols[0]].astype(str).str[:6] == CODIGO_CONCORDIA]
            else:
                print("   ❌ Não foi possível identificar coluna de filtro")
                return None
        else:
            cod_col = cod_mun_cols[0]
            print(f"   → Filtrando por coluna: {cod_col}")
            gdf_concordia = gdf_sc[gdf_sc[cod_col].astype(str) == CODIGO_CONCORDIA]
        
        if gdf_concordia.empty:
            print("   ❌ Nenhum setor encontrado para Concórdia")
            return None
        
        print(f"   ✅ {len(gdf_concordia)} setores de Concórdia filtrados")
        
        # Garantir CRS WGS84
        if gdf_concordia.crs.to_epsg() != 4326:
            gdf_concordia = gdf_concordia.to_crs(epsg=4326)
            print("   ✅ CRS convertido para WGS84")
        
        # Salvar como shapefile limpo
        output_shp = OUTPUT_DIR.parent / "Concordia_sencitario"
        gdf_concordia.to_file(output_shp.with_suffix(".shp"), driver="ESRI Shapefile")
        print(f"   ✅ Shapefile salvo: {output_shp}.shp")
        
        # Salvar também como GeoPackage (mais moderno)
        output_gpkg = OUTPUT_DIR / "concordia_setores_2022.gpkg"
        gdf_concordia.to_file(output_gpkg, driver="GPKG", layer="setores")
        print(f"   ✅ GeoPackage salvo: {output_gpkg}")
        
        # Limpeza
        import shutil
        shutil.rmtree(extract_dir)
        zip_path.unlink()
        print("   ✅ Arquivos temporários removidos")
        
        return gdf_concordia
    
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def gerar_estatisticas(gdf):
    """Gera estatísticas básicas dos setores."""
    print("\n📊 ESTATÍSTICAS DOS SETORES CENSITÁRIOS")
    print("="*50)
    print(f"Total de setores: {len(gdf)}")
    print(f"Área total: {gdf.to_crs(31982).area.sum() / 1_000_000:.2f} km²")
    print(f"CRS: {gdf.crs}")
    print(f"\nColunas disponíveis:")
    for col in gdf.columns:
        if col != 'geometry':
            print(f"  - {col}")
    print("="*50)

def main():
    print("🚀 INICIANDO DOWNLOAD DOS SETORES CENSITÁRIOS DE CONCÓRDIA/SC")
    print("="*70)
    
    # 1. Baixar
    zip_path = baixar_setores_ibge()
    if not zip_path:
        print("\n❌ Falha no download. Verifique a conexão e tente novamente.")
        return
    
    # 2. Extrair e filtrar
    gdf_concordia = extrair_e_filtrar_concordia(zip_path)
    if gdf_concordia is None:
        print("\n❌ Falha ao processar os setores.")
        return
    
    # 3. Estatísticas
    gerar_estatisticas(gdf_concordia)
    
    print("\n✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("\n📁 Arquivos gerados:")
    print(f"   • Concordia_sencitario.shp (na raiz do projeto)")
    print(f"   • concordia_setores_2022.gpkg (em 01_DADOS/processados)")
    print("\n💡 Agora você pode regenerar o mapa avançado com:")
    print("   python 02_SCRIPTS/dashboard_avancado_colorbrewer.py")

if __name__ == "__main__":
    main()
