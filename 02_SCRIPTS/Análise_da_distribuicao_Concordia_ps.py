import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
df = pd.read_excel('Concordia_ps.xlsx', sheet_name='concordia_filtro')

# Análise básica
print("Dimensões do dataset:", df.shape)
print("\nPrimeiras linhas:")
print(df.head())

print("\nColunas disponíveis:")
print(df.columns.tolist())

# Estatísticas descritivas
print("\nEstatísticas descritivas:")
print(df.describe())

# Verificar valores nulos
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# Análise de tipos de estabelecimentos (Field7)
print("\nTipos de estabelecimentos:")
print(df['Field7'].value_counts())

# Visualização - Distribuição de tipos de estabelecimentos
plt.figure(figsize=(12, 6))
df['Field7'].value_counts().plot(kind='bar')
plt.title('Distribuição de Tipos de Estabelecimentos de Saúde - Concordia')
plt.xlabel('Tipo de Estabelecimento')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Contar ESF vs PS
esf_count = df[df['Field7'].str.contains('ESF', na=False)].shape[0]
ps_count = df[df['Field7'].str.contains('PS', na=False)].shape[0]
outros_count = df.shape[0] - esf_count - ps_count

print(f"\nQuantidade por tipo:")
print(f"ESF (Estratégia Saúde da Família): {esf_count}")
print(f"PS (Posto de Saúde): {ps_count}")
print(f"Outros: {outros_count}")

# Salvar análise resumida
resumo = {
    'Total_Estabelecimentos': df.shape[0],
    'ESF': esf_count,
    'PS': ps_count,
    'Outros': outros_count
}

resumo_df = pd.DataFrame([resumo])
resumo_df.to_excel('resumo_estabelecimentos_concordia.xlsx', index=False)