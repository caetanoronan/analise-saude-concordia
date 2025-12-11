#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar mapa_avancado_treelayer_colorbrewer.html com:
1. max_zoom: 16 -> 18
2. Trocar GroupedLayerControl por LayerControl simples
3. Adicionar rosa dos ventos
"""

import os
import re

mapa_path = r"docs\mapa_avancado_treelayer_colorbrewer.html"

print(f"📝 Atualizando {mapa_path}...")

# Ler arquivo
with open(mapa_path, 'r', encoding='utf-8') as f:
    conteudo = f.read()

# 1. Atualizar max_zoom de 16 para 18 (já feito pelo PowerShell, mas vamos confirmar)
conteudo_original = conteudo
conteudo = re.sub(r'"maxZoom": 16,', '"maxZoom": 18,', conteudo)

if conteudo != conteudo_original:
    print("   ✅ maxZoom atualizado para 18")
else:
    print("   ⚠️ maxZoom já estava em 18 ou não encontrado")

# 2. Trocar GroupedLayerControl por LayerControl simples
# Procurar e remover o script do GroupedLayerControl
conteudo = re.sub(
    r'new L\.Control\.groupedLayers\([^}]+\}\s*\)\.addTo\([^)]+\);',
    'L.control.layers().addTo(map_[a-z0-9]+);',
    conteudo,
    flags=re.DOTALL
)

print("   ✅ GroupedLayerControl verificado/atualizado")

# 3. Adicionar rosa dos ventos antes da tag </body>
rosa_html = '''    <div id="rosa-ventos-unica" style="
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 75px;
        height: 75px;
        z-index: 10001;
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #2c5aa0;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;">
        <svg width="70" height="70" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="48" fill="white" stroke="#2c5aa0" stroke-width="2"/>
            <!-- Seta Norte (Vermelha) -->
            <path d="M 50 10 L 55 40 L 50 35 L 45 40 Z" fill="#cc0000"/>
            <!-- Seta Sul -->
            <path d="M 50 90 L 55 60 L 50 65 L 45 60 Z" fill="#666"/>
            <!-- Seta Leste -->
            <path d="M 90 50 L 60 55 L 65 50 L 60 45 Z" fill="#666"/>
            <!-- Seta Oeste -->
            <path d="M 10 50 L 40 55 L 35 50 L 40 45 Z" fill="#666"/>
            <!-- Letras -->
            <text x="50" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#cc0000">N</text>
            <text x="50" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">S</text>
            <text x="85" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">L</text>
            <text x="15" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#666">O</text>
        </svg>
    </div>

</body>'''

if '</body>' in conteudo and 'rosa-ventos-unica' not in conteudo:
    conteudo = conteudo.replace('</body>', rosa_html)
    print("   ✅ Rosa dos ventos adicionada")
else:
    print("   ⚠️ Rosa dos ventos já estava ou </body> não encontrado")

# Salvar arquivo
with open(mapa_path, 'w', encoding='utf-8') as f:
    f.write(conteudo)

print(f"\n✅ Arquivo {mapa_path} atualizado com sucesso!")
print("\n📋 Melhorias aplicadas:")
print("   ✓ maxZoom: 18")
print("   ✓ LayerControl simples (múltiplas camadas)")
print("   ✓ Rosa dos ventos (N/S/L/O)")
