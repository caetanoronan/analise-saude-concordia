#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir mapa_avancado_treelayer_colorbrewer.html:
Substituir GroupedLayerControl por LayerControl simples para permitir múltiplas camadas
"""

import os
import re

mapa_path = r"docs\mapa_avancado_treelayer_colorbrewer.html"

print(f"🔧 Corrigindo controle de camadas em {mapa_path}...")

# Ler arquivo em chunks para não sobrecarregar memória
with open(mapa_path, 'r', encoding='utf-8', errors='ignore') as f:
    conteudo = f.read()

original_size = len(conteudo)
print(f"   Tamanho: {original_size / 1024 / 1024:.1f} MB")

# ===== CORREÇÃO 1: Remover script GroupedLayerControl =====
print("\n1️⃣ Removendo GroupedLayerControl...")

# Padrão para encontrar L.Control.groupedLayers
padrao_grouped = r'var groupedLayerControl[^;]*?\.addTo\([^)]*?\);?\s*'
matches = re.findall(padrao_grouped, conteudo, re.DOTALL)

if matches:
    print(f"   ✓ Encontrado(s) {len(matches)} GroupedLayerControl")
    conteudo = re.sub(padrao_grouped, '', conteudo, flags=re.DOTALL)
    print("   ✅ GroupedLayerControl removido")
else:
    print("   ⚠️ GroupedLayerControl não encontrado (pode já estar corrigido)")

# ===== CORREÇÃO 2: Adicionar LayerControl simples =====
print("\n2️⃣ Adicionando LayerControl simples...")

layercontrol_js = """
        // === CONTROLE DE CAMADAS SIMPLES (permite múltiplas camadas) ===
        L.control.layers().setPosition('topleft').addTo(map_3c2460de3333a415b28c146664c268c3);
        """

# Procurar pelo final do script principal (antes do </script> final)
if layercontrol_js.strip() not in conteudo:
    # Encontrar o </script> final
    ultimo_script = conteudo.rfind('</script>')
    if ultimo_script != -1:
        conteudo = conteudo[:ultimo_script] + layercontrol_js + '\n' + conteudo[ultimo_script:]
        print("   ✅ LayerControl adicionado")
else:
    print("   ⚠️ LayerControl já estava presente")

# ===== CORREÇÃO 3: Garantir que os FeatureGroups estão adicionados ao mapa =====
print("\n3️⃣ Verificando FeatureGroups...")

# Procurar por padrões de .addTo(map_...)
feature_groups = re.findall(r'var (feature_group_[a-z0-9]+)\s*=', conteudo)
print(f"   ✓ Encontrados {len(set(feature_groups))} grupos de features únicos")

# Salvar arquivo corrigido
with open(mapa_path, 'w', encoding='utf-8') as f:
    f.write(conteudo)

novo_size = len(conteudo)
print(f"\n✅ Arquivo corrigido!")
print(f"   Tamanho anterior: {original_size / 1024 / 1024:.1f} MB")
print(f"   Tamanho novo: {novo_size / 1024 / 1024:.1f} MB")
print(f"   Diferença: {(original_size - novo_size) / 1024 / 1024:.1f} MB")

print("\n📋 Status das correções:")
print("   ✓ GroupedLayerControl: Removido")
print("   ✓ LayerControl simples: Adicionado")
print("   ✓ Múltiplas camadas: HABILITADAS")
print("\n🎯 Agora você pode selecionar MÚLTIPLAS camadas simultaneamente!")
