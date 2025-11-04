import folium
# Dashboard Simplificado - Análise Espacial Concórdia/SC
# Autor: Caetano Ronan - UFSC
# Data: Outubro 2025

import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import warnings
warnings.filterwarnings('ignore')

print("🏥 DASHBOARD SIMPLIFICADO - ANÁLISE ESPACIAL CONCÓRDIA/SC")
print("="*60)

# Função para calcular distância
def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula distância usando fórmula de Haversine"""
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Função para identificar estabelecimentos públicos
def eh_posto_publico(nome_fantasia, tipo_unidade, razao_social):
    """Identifica estabelecimentos públicos"""
    nome = str(nome_fantasia).upper() if nome_fantasia else ""
    razao = str(razao_social).upper() if razao_social else ""
    
    criterios_publicos = [
        'ESF' in nome, 'PS ' in nome, 'POSTO' in nome,
        'MUNICIPIO' in razao, 'PREFEITURA' in razao,
        'SECRETARIA' in razao, 'CAPS' in nome, 'SAMU' in nome,
        tipo_unidade in ['1', '2', '70', '81']
    ]
    return any(criterios_publicos)

# Carregamento de dados
try:
    print("📊 Carregando dados...")
    df_sc = pd.read_csv('Tabela_estado_SC.csv', sep=';', encoding='utf-8', low_memory=False)
    df_concordia = df_sc[df_sc['CO_MUNICIPIO_GESTOR'] == 420430].copy()
    df_geo = df_concordia.copy()
    # Converter coordenadas para float e filtrar nulos
    df_geo['NU_LATITUDE'] = pd.to_numeric(df_geo['NU_LATITUDE'], errors='coerce')
    df_geo['NU_LONGITUDE'] = pd.to_numeric(df_geo['NU_LONGITUDE'], errors='coerce')
    df_geo = df_geo.dropna(subset=['NU_LATITUDE', 'NU_LONGITUDE'])
    print(f"✅ Dados carregados: {len(df_geo)} estabelecimentos")
    dados_reais = True
except Exception as e:
    print(f"⚠️ Erro no carregamento: {e}")
    print("🔄 Usando dados existentes processados...")
    try:
        # Tentar carregar dados já processados
        df_geo = pd.read_csv('concordia_saude_simples.csv')
        print(f"✅ Dados processados carregados: {len(df_geo)} estabelecimentos")
        # Renomear colunas se necessário
        if 'LAT' in df_geo.columns:
            df_geo = df_geo.rename(columns={'LAT': 'NU_LATITUDE', 'LON': 'NU_LONGITUDE'})
        # Converter coordenadas para float e filtrar nulos
        df_geo['NU_LATITUDE'] = pd.to_numeric(df_geo['NU_LATITUDE'], errors='coerce')
        df_geo['NU_LONGITUDE'] = pd.to_numeric(df_geo['NU_LONGITUDE'], errors='coerce')
        df_geo = df_geo.dropna(subset=['NU_LATITUDE', 'NU_LONGITUDE'])
        dados_reais = True
    except:
        print("❌ Criando dados de exemplo...")
        import numpy as np
        np.random.seed(42)
        n_estabelecimentos = 100
        df_geo = pd.DataFrame({
            'NU_LATITUDE': np.random.normal(-27.235, 0.05, n_estabelecimentos),
            'NU_LONGITUDE': np.random.normal(-52.025, 0.1, n_estabelecimentos),
            'NO_FANTASIA': [f'Estabelecimento {i}' for i in range(n_estabelecimentos)],
            'TP_UNIDADE': np.random.choice(['1', '2', '22', '39', '5'], n_estabelecimentos),
            'NO_BAIRRO': np.random.choice(['Centro', 'Bairro A', 'Bairro B'], n_estabelecimentos),
            'NO_RAZAO_SOCIAL': ['Razão Social'] * n_estabelecimentos
        })
        dados_reais = False

centro_concordia = [-27.2335, -52.0238]

# Calcular distâncias e identificar públicos
df_geo['dist_centro'] = df_geo.apply(
    lambda row: calcular_distancia(
        centro_concordia[0], centro_concordia[1],
        row['NU_LATITUDE'], row['NU_LONGITUDE']
    ), axis=1
)

df_geo['eh_publico'] = df_geo.apply(
    lambda row: eh_posto_publico(
        row.get('NO_FANTASIA', ''),
        str(row.get('TP_UNIDADE', '')),
        row.get('NO_RAZAO_SOCIAL', '')
    ), axis=1
)

df_publicos = df_geo[df_geo['eh_publico']].copy()

print(f"🏛️ Estabelecimentos públicos: {len(df_publicos)}")
print(f"🏢 Estabelecimentos privados: {len(df_geo) - len(df_publicos)}")

# === GERAÇÃO DO MAPA FOLIUM ===
try:
    if not df_geo.empty:
        centro_lat = df_geo['NU_LATITUDE'].mean()
        centro_lon = df_geo['NU_LONGITUDE'].mean()
        mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=12)
        for idx, row in df_geo.iterrows():
            folium.Marker(
                location=[row['NU_LATITUDE'], row['NU_LONGITUDE']],
                popup=row.get('NO_FANTASIA', 'Estabelecimento'),
                icon=folium.Icon(color='blue', icon='plus')
            ).add_to(mapa)
        mapa.save('03_RESULTADOS/mapas/mapa_estabelecimentos_concordia.html')
        print('✅ Mapa atualizado: 03_RESULTADOS/mapas/mapa_estabelecimentos_concordia.html')
except Exception as e:
    print(f"⚠️ Erro ao gerar mapa Folium: {e}")

# Criar visualizações simplificadas
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('🏥 ANÁLISE ESPACIAL - ESTABELECIMENTOS DE SAÚDE CONCÓRDIA/SC', 
             fontsize=16, fontweight='bold')

# Gráfico 1: Distribuição das distâncias
axes[0,0].hist(df_geo['dist_centro'], bins=15, color='skyblue', alpha=0.7, edgecolor='black')
axes[0,0].axvline(df_geo['dist_centro'].mean(), color='red', linestyle='--', 
                  label=f'Média: {df_geo["dist_centro"].mean():.1f}km')
axes[0,0].set_title('📏 Distribuição das Distâncias')
axes[0,0].set_xlabel('Distância ao Centro (km)')
axes[0,0].set_ylabel('Frequência')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Gráfico 2: Tipos de estabelecimentos
tipo_counts = df_geo['TP_UNIDADE'].value_counts().head(6)
axes[0,1].bar(range(len(tipo_counts)), tipo_counts.values, color='lightcoral')
axes[0,1].set_title('🏥 Tipos de Estabelecimentos')
axes[0,1].set_xlabel('Tipo de Unidade')
axes[0,1].set_ylabel('Quantidade')
axes[0,1].set_xticks(range(len(tipo_counts)))
axes[0,1].set_xticklabels([f'Tipo {t}' for t in tipo_counts.index], rotation=45)
axes[0,1].grid(True, alpha=0.3)

# Gráfico 3: Dispersão geográfica
cores_scatter = ['red' if pub else 'blue' for pub in df_geo['eh_publico']]
axes[1,0].scatter(df_geo['NU_LONGITUDE'], df_geo['NU_LATITUDE'], 
                  c=cores_scatter, alpha=0.6, s=30)
axes[1,0].scatter(centro_concordia[1], centro_concordia[0], 
                  c='black', s=200, marker='*', label='Centro')
axes[1,0].set_title('📍 Dispersão Geográfica')
axes[1,0].set_xlabel('Longitude')
axes[1,0].set_ylabel('Latitude')
axes[1,0].legend(['Privado', 'Público', 'Centro'])
axes[1,0].grid(True, alpha=0.3)

# Gráfico 4: Pizza Público vs Privado
sizes = [len(df_publicos), len(df_geo) - len(df_publicos)]
labels = ['Público', 'Privado']
colors = ['lightcoral', 'lightblue']
axes[1,1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
axes[1,1].set_title('⚖️ Distribuição Público vs Privado')

plt.tight_layout()

# Salvar o dashboard
plt.savefig('03_RESULTADOS/DASHBOARD_ANALISE_ESPACIAL_CONCORDIA.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Dashboard salvo: 03_RESULTADOS/DASHBOARD_ANALISE_ESPACIAL_CONCORDIA.png")

plt.show()

# Gerar relatório de estatísticas
print("\n" + "="*60)
print("📊 RELATÓRIO FINAL DE ESTATÍSTICAS")
print("="*60)

print(f"\n🏥 NÚMEROS PRINCIPAIS:")
print(f"   • Total analisado: {len(df_geo)} estabelecimentos")
print(f"   • Públicos: {len(df_publicos)} ({len(df_publicos)/len(df_geo)*100:.1f}%)")
print(f"   • Privados: {len(df_geo)-len(df_publicos)} ({(len(df_geo)-len(df_publicos))/len(df_geo)*100:.1f}%)")

print(f"\n📏 ACESSIBILIDADE:")
print(f"   • Distância média: {df_geo['dist_centro'].mean():.2f} km")
print(f"   • Distância mínima: {df_geo['dist_centro'].min():.2f} km")
print(f"   • Distância máxima: {df_geo['dist_centro'].max():.2f} km")
print(f"   • ≤ 5km do centro: {len(df_geo[df_geo['dist_centro'] <= 5])}/{len(df_geo)} ({len(df_geo[df_geo['dist_centro'] <= 5])/len(df_geo)*100:.1f}%)")

if len(df_publicos) > 0:
    print(f"   • Públicos ≤ 5km: {len(df_publicos[df_publicos['dist_centro'] <= 5])}/{len(df_publicos)} ({len(df_publicos[df_publicos['dist_centro'] <= 5])/len(df_publicos)*100:.1f}%)")

print(f"\n🎯 PRINCIPAIS TIPOS:")
for tipo, count in tipo_counts.items():
    print(f"   • Tipo {tipo}: {count} unidades ({count/len(df_geo)*100:.1f}%)")

print(f"\n✅ ARQUIVOS GERADOS:")
print("   ✅ Dashboard de visualizações")
print("   ✅ Análise estatística completa")
print("   ✅ Dados processados organizados")

if dados_reais:
    print(f"\n🎯 DADOS: REAIS (Base CNES)")
else:
    print(f"\n🎯 DADOS: EXEMPLO (Para demonstração)")

print(f"\n🎉 DASHBOARD EXECUTADO COM SUCESSO!")
print("="*60)