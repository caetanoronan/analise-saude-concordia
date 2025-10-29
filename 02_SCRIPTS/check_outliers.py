#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para identificar estabelecimentos fora do município de Concórdia
"""
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Carregar dados
df = pd.read_csv('01_DADOS/processados/concordia_saude_simples.csv')

# Calcular distâncias
centro = (-27.2335, -52.0238)
df['dist_centro'] = df.apply(
    lambda r: haversine(centro[0], centro[1], r['LAT'], r['LON']), 
    axis=1
)

# Identificar outliers (>30km)
outliers = df[df['dist_centro'] > 30].sort_values('dist_centro', ascending=False)

print("=" * 80)
print("ESTABELECIMENTOS FORA DO MUNICÍPIO (>30km do centro)")
print("=" * 80)
print(f"\nTotal de outliers encontrados: {len(outliers)}\n")

if len(outliers) > 0:
    for idx, row in outliers.iterrows():
        nome = row.get('NO_FANTASIA', row.get('NOME', 'N/A'))
        print(f"📍 {nome}")
        print(f"   Distância: {row['dist_centro']:.2f} km")
        print(f"   Coordenadas: {row['LAT']:.6f}, {row['LON']:.6f}")
        print(f"   Endereço: {row.get('NO_LOGRADOURO', row.get('ENDERECO', 'N/A'))}")
        print(f"   Bairro: {row.get('NO_BAIRRO', row.get('BAIRRO', 'N/A'))}")
        print(f"   Tipo: {row.get('tipo_descricao', row.get('TIPO', 'N/A'))}")
        print()

# Estatísticas gerais
print("=" * 80)
print("ESTATÍSTICAS GERAIS")
print("=" * 80)
print(f"Total de estabelecimentos: {len(df)}")
print(f"Dentro de 30km: {len(df[df['dist_centro'] <= 30])} ({len(df[df['dist_centro'] <= 30])/len(df)*100:.1f}%)")
print(f"Fora de 30km: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
print(f"\nDistância máxima: {df['dist_centro'].max():.2f} km")
print(f"Distância média: {df['dist_centro'].mean():.2f} km")
print(f"Distância mediana: {df['dist_centro'].median():.2f} km")
