"""Script temporário para analisar tipos de estabelecimentos"""
import pandas as pd

# Carregar Excel
df = pd.read_excel('Tabela_estado_SC.xlsx')
df_conc = df[df['CO_MUNICIPIO_GESTOR'] == 420430]

print("=" * 70)
print("ANÁLISE DE TIPOS DE ESTABELECIMENTOS - CONCÓRDIA/SC")
print("=" * 70)

print(f"\n📊 TOTAL: {len(df_conc)} estabelecimentos\n")

print("=" * 70)
print("DISTRIBUIÇÃO POR TIPO DE UNIDADE (TP_UNIDADE)")
print("=" * 70)
print(df_conc['TP_UNIDADE'].value_counts())

print("\n" + "=" * 70)
print("EXEMPLOS DE CADA TIPO")
print("=" * 70)

for tipo in df_conc['TP_UNIDADE'].value_counts().head(15).index:
    print(f"\n🏥 TIPO {tipo}:")
    exemplos = df_conc[df_conc['TP_UNIDADE'] == tipo][['NO_FANTASIA', 'NO_RAZAO_SOCIAL']].head(5)
    for idx, row in exemplos.iterrows():
        print(f"   • {row['NO_FANTASIA']}")
