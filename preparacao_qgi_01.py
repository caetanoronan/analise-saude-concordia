# preparacao_qgis.py
import pandas as pd
import os

print("=== PREPARAÇÃO DE DADOS PARA QGIS - CONCÓRDIA/SC ===")

try:
    # Carregar dados do Excel
    df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')
    print("✓ Dados carregados com sucesso!")
    
except ImportError:
    print("ERRO: Biblioteca openpyxl não instalada!")
    print("Execute no terminal: pip install openpyxl")
    exit()
except FileNotFoundError:
    print("ERRO: Arquivo 'Concordia_ps.xlsx' não encontrado!")
    exit()

# Criar colunas organizadas para QGIS
df_qgis = df[[
    'fid', 'Field7', 'Field8', 'Field9', 'Field11', 'Field12', 
    'Field16', 'Field18', 'Field39', 'Field40'
]].copy()

# Renomear colunas para facilitar no QGIS
df_qgis.columns = [
    'ID', 'NOME', 'ENDERECO', 'NUMERO', 'BAIRRO', 'CEP', 
    'TELEFONE', 'EMAIL', 'LATITUDE', 'LONGITUDE'
]

# Adicionar coluna de TIPO
df_qgis['TIPO'] = df_qgis['NOME'].apply(
    lambda x: 'ESF' if 'ESF' in str(x) else 'PS' if 'PS' in str(x) else 'OUTROS'
)

# Exportar para CSV otimizado para QGIS
df_qgis.to_csv('estabelecimentos_concordia_qgis.csv', index=False, encoding='utf-8')
print("✓ CSV para QGIS exportado: 'estabelecimentos_concordia_qgis.csv'")

# Exportar com WKT (Well-Known Text) para fácil importação
with open('estabelecimentos_concordia_wkt.csv', 'w', encoding='utf-8') as f:
    f.write('ID,NOME,TIPO,ENDERECO,BAIRRO,CEP,LAT,LON,WKT\n')
    for _, row in df_qgis.iterrows():
        wkt = f'POINT ({row["LONGITUDE"]} {row["LATITUDE"]})'
        f.write(f'{row["ID"]},"{row["NOME"]}","{row["TIPO"]}","{row["ENDERECO"]}",')
        f.write(f'"{row["BAIRRO"]}",{row["CEP"]},{row["LATITUDE"]},{row["LONGITUDE"]},"{wkt}"\n')

print("✓ CSV com WKT exportado: 'estabelecimentos_concordia_wkt.csv'")

# Criar arquivo de metadados
with open('METADADOS_estabelecimentos.txt', 'w', encoding='utf-8') as f:
    f.write("METADADOS - ESTABELECIMENTOS DE SAÚDE CONCÓRDIA/SC\n")
    f.write("=" * 50 + "\n")
    f.write(f"Total de estabelecimentos: {len(df_qgis)}\n")
    f.write(f"ESF: {len(df_qgis[df_qgis['TIPO']=='ESF'])}\n")
    f.write(f"PS: {len(df_qgis[df_qgis['TIPO']=='PS'])}\n")
    f.write(f"Outros: {len(df_qgis[df_qgis['TIPO']=='OUTROS'])}\n\n")
    f.write("SISTEMA DE COORDENADAS: WGS84 (EPSG:4326)\n")
    f.write("LATITUDE: Field39\n")
    f.write("LONGITUDE: Field40\n\n")
    f.write("ARQUIVOS GERADOS:\n")
    f.write("- estabelecimentos_concordia_qgis.csv (para carregamento simples)\n")
    f.write("- estabelecimentos_concordia_wkt.csv (com geometria WKT)\n")

print("✓ Metadados exportados: 'METADADOS_estabelecimentos.txt'")

# Resumo estatístico
print("\n" + "="*50)
print("RESUMO PARA QGIS:")
print("="*50)
print(f"• Arquivos CSV criados: 2")
print(f"• Sistema coordenadas: WGS84 (Lat/Lon)")
print(f"• Total pontos: {len(df_qgis)}")
print(f"• Extensão geográfica:")
print(f"  - Lat: {df_qgis['LATITUDE'].min():.3f} a {df_qgis['LATITUDE'].max():.3f}")
print(f"  - Lon: {df_qgis['LONGITUDE'].min():.3f} a {df_qgis['LONGITUDE'].max():.3f}")

print("\n🎯 PRÓXIMOS PASSOS NO QGIS:")
print("1. Abrir QGIS")
print("2. Camada → Adicionar Camada → Adicionar Camada de Texto Delimitado")
print("3. Escolher 'estabelecimentos_concordia_qgis.csv'")
print("4. Definir X: LONGITUDE, Y: LATITUDE")
print("5. Sistema de referência: WGS84 (EPSG:4326)")