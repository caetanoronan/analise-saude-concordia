"""
Script para filtrar estabelecimentos de saúde dentro dos limites de Concórdia/SC.
Remove estabelecimentos que estão fora do polígono municipal.

Autor: Ronan Armando Caetano
Data: Novembro 2025
Instituição: UFSC
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

def filtrar_estabelecimentos_municipio():
    """
    Filtra estabelecimentos que estão dentro do limite municipal de Concórdia.
    """
    print("🗺️  Carregando limite municipal de Concórdia...")
    
    # Caminhos dos arquivos
    shapefile_municipios = r'SC_Municipios_2024\SC_Municipios_2024.shp'
    arquivo_dados = r'01_DADOS\processados\concordia_saude_simples.csv'
    arquivo_saida = r'01_DADOS\processados\concordia_saude_filtrado.csv'
    
    # Verificar se arquivos existem
    if not os.path.exists(shapefile_municipios):
        print(f"❌ Shapefile não encontrado: {shapefile_municipios}")
        return
    
    if not os.path.exists(arquivo_dados):
        print(f"❌ Arquivo de dados não encontrado: {arquivo_dados}")
        return
    
    # Carregar shapefile dos municípios
    try:
        municipios_gdf = gpd.read_file(shapefile_municipios)
        print(f"✅ Shapefile carregado: {len(municipios_gdf)} municípios encontrados")
        print(f"   Colunas disponíveis: {list(municipios_gdf.columns)}")
    except Exception as e:
        print(f"❌ Erro ao carregar shapefile: {e}")
        return
    
    # Filtrar apenas Concórdia (código IBGE 420430)
    # Tentar diferentes nomes de colunas possíveis
    coluna_codigo = None
    for col in ['CD_MUN', 'CD_GEOCMU', 'GEOCODIGO', 'COD_IBGE', 'CODIGO']:
        if col in municipios_gdf.columns:
            coluna_codigo = col
            break
    
    if coluna_codigo is None:
        print("⚠️  Coluna de código IBGE não encontrada. Tentando filtrar por nome...")
        concordia_gdf = municipios_gdf[municipios_gdf['NM_MUN'].str.upper() == 'CONCORDIA']
    else:
        concordia_gdf = municipios_gdf[municipios_gdf[coluna_codigo].astype(str).str.contains('420430')]
    
    if len(concordia_gdf) == 0:
        print("❌ Município de Concórdia não encontrado no shapefile")
        print(f"   Municípios disponíveis: {municipios_gdf['NM_MUN'].head(10).tolist()}")
        return
    
    print(f"✅ Limite municipal de Concórdia encontrado")
    print(f"   CRS: {concordia_gdf.crs}")
    
    # Pegar o polígono de Concórdia
    concordia_poligono = concordia_gdf.geometry.iloc[0]
    
    # Carregar dados dos estabelecimentos
    df = pd.read_csv(arquivo_dados)
    print(f"\n📊 Estabelecimentos no arquivo original: {len(df)}")
    
    # Converter para GeoDataFrame
    df_clean = df.dropna(subset=['LAT', 'LON'])
    df_clean['LAT'] = pd.to_numeric(df_clean['LAT'], errors='coerce')
    df_clean['LON'] = pd.to_numeric(df_clean['LON'], errors='coerce')
    df_clean = df_clean.dropna(subset=['LAT', 'LON'])
    
    print(f"   Com coordenadas válidas: {len(df_clean)}")
    
    # Criar geometrias de pontos
    geometry = [Point(lon, lat) for lon, lat in zip(df_clean['LON'], df_clean['LAT'])]
    estabelecimentos_gdf = gpd.GeoDataFrame(df_clean, geometry=geometry, crs='EPSG:4326')
    
    # Reprojetar para o mesmo CRS do shapefile
    if concordia_gdf.crs != estabelecimentos_gdf.crs:
        estabelecimentos_gdf = estabelecimentos_gdf.to_crs(concordia_gdf.crs)
    
    # Filtrar estabelecimentos dentro do polígono de Concórdia
    print("\n🔍 Filtrando estabelecimentos dentro do limite municipal...")
    
    estabelecimentos_dentro = estabelecimentos_gdf[estabelecimentos_gdf.geometry.within(concordia_poligono)]
    estabelecimentos_fora = estabelecimentos_gdf[~estabelecimentos_gdf.geometry.within(concordia_poligono)]
    
    print(f"\n📍 Resultados da filtragem:")
    print(f"   ✅ Dentro do limite: {len(estabelecimentos_dentro)} estabelecimentos")
    print(f"   ❌ Fora do limite: {len(estabelecimentos_fora)} estabelecimentos")
    
    # Mostrar estabelecimentos removidos
    if len(estabelecimentos_fora) > 0:
        print(f"\n🗑️  Estabelecimentos REMOVIDOS (fora do limite municipal):")
        for idx, row in estabelecimentos_fora.iterrows():
            print(f"   - {row['NOME']} ({row['LAT']:.6f}, {row['LON']:.6f})")
    
    # Salvar dados filtrados (remover coluna geometry antes de salvar como CSV)
    df_filtrado = estabelecimentos_dentro.drop(columns=['geometry'])
    
    # Reprojetar de volta para WGS84 se necessário
    if 'LAT' in df_filtrado.columns and 'LON' in df_filtrado.columns:
        # Coordenadas já estão corretas no dataframe original
        pass
    
    df_filtrado.to_csv(arquivo_saida, index=False)
    print(f"\n✅ Dados filtrados salvos em: {arquivo_saida}")
    print(f"   Total de estabelecimentos válidos: {len(df_filtrado)}")
    
    # Estatísticas finais
    print(f"\n📊 Estatísticas:")
    print(f"   Taxa de retenção: {len(df_filtrado)/len(df_clean)*100:.1f}%")
    print(f"   Estabelecimentos removidos: {len(estabelecimentos_fora)}")
    
    return df_filtrado, estabelecimentos_fora

if __name__ == "__main__":
    print("=" * 80)
    print("🗺️  FILTRAR ESTABELECIMENTOS PELO LIMITE MUNICIPAL DE CONCÓRDIA")
    print("=" * 80)
    print()
    
    try:
        df_filtrado, df_fora = filtrar_estabelecimentos_municipio()
        
        print()
        print("=" * 80)
        print("✨ Processamento concluído com sucesso!")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Erro durante processamento: {e}")
        import traceback
        traceback.print_exc()
