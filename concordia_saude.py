# PRIMEIRO: Execute este código Python para preparar os dados
import pandas as pd

# Carregar e preparar dados
df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')

# Criar arquivo simplificado para QGIS
dados_qgis = df[['Field7', 'Field39', 'Field40', 'Field8', 'Field11', 'Field12']].copy()
dados_qgis.columns = ['NOME', 'LAT', 'LON', 'ENDERECO', 'BAIRRO', 'CEP']
dados_qgis['TIPO'] = dados_qgis['NOME'].apply(lambda x: 'ESF' if 'ESF' in str(x) else 'PS')

# Salvar
dados_qgis.to_csv('concordia_saude_simples.csv', index=False, encoding='utf-8')
print("✅ Arquivo 'concordia_saude_simples.csv' criado!")