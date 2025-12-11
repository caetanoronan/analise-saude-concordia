# 📊 Guia Rápido - Dashboard ColorBrewer

## ⚡ Início Rápido (3 minutos)

### 1️⃣ Executar Dashboard
```powershell
python 02_SCRIPTS\dashboard_avancado_colorbrewer.py
```
⏱️ **Tempo:** 2-5 minutos | 📁 **Saída:** `03_RESULTADOS/`

---

### 2️⃣ Abrir Mapa Interativo
```powershell
# Navegador padrão
start 03_RESULTADOS\mapas\mapa_avancado_treelayer_colorbrewer.html

# Ou pelo servidor HTTP (porta 8000)
start http://localhost:8000/mapa_avancado_treelayer_colorbrewer.html
```

---

### 3️⃣ Visualizar Dashboard Visual
```powershell
# Imagem PNG (alta resolução)
start 03_RESULTADOS\dashboard_completo_colorbrewer.png

# PDF vetorial (impressão)
start 03_RESULTADOS\dashboard_completo_colorbrewer.pdf
```

---

## 🎨 Legenda de Cores (ColorBrewer)

### Marcadores no Mapa

| Cor | Ícone | Significado | Exemplos |
|-----|-------|-------------|----------|
| 🔴 **Vermelho** | ➕ | Estabelecimento Público | ESF, Posto de Saúde, UBS |
| ⚪ **Cinza** | ℹ️ | Privado/Outros | Clínicas, Consultórios, Labs |
| ⚫ **Preto** | 🏠 | Centro Urbano | Praça Central (referência) |

### Círculos de Análise

| Cor | Raio | Zona | Cobertura Esperada |
|-----|------|------|-------------------|
| 🟢 **Verde** | 5 km | Urbana | > 70% estabelecimentos |
| 🟠 **Laranja** | 10 km | Periurbana | 85-95% estabelecimentos |
| 🔴 **Vermelho** | 20 km | Rural | 100% estabelecimentos |

### Linhas e Polígonos

| Cor | Estilo | Elemento |
|-----|--------|----------|
| 🔵 **Azul** | Tracejado | Limite Municipal Concórdia |
| 🩶 **Cinza Claro** | Sólido | Municípios Vizinhos |
| 🌈 **Gradiente** | Transparente | Mapa de Calor (densidade) |

---

## 🖱️ Controles do Mapa Interativo

### Navegação Básica

| Ação | Como Fazer | Resultado |
|------|-----------|-----------|
| **Zoom In** | Roda mouse ↑ ou `+` | Aproxima mapa |
| **Zoom Out** | Roda mouse ↓ ou `-` | Afasta mapa |
| **Mover** | Clicar + arrastar | Pan (deslocamento) |
| **Reset** | Duplo clique | Retorna zoom inicial |

### TreeLayerControl (📂)

| Ação | Elemento | Resultado |
|------|----------|-----------|
| **Expandir grupo** | Clicar 📂 pasta | Mostra subcamadas |
| **Ligar camada** | ☑️ Checkbox | Exibe no mapa |
| **Desligar camada** | ☐ Checkbox | Oculta do mapa |
| **Exclusivo** | 🔘 Radio | Apenas uma ativa |

### Interação com Estabelecimentos

| Ação | Resultado |
|------|-----------|
| **Passar mouse** | 💬 Tooltip rápido (nome) |
| **Clicar marcador** | 📋 Popup completo (detalhes) |
| **Clicar cluster** | 🔍 Zoom + expansão automática |

---

## 📈 Interpretação Rápida dos Gráficos

### Dashboard Visual (Grid 3×3)

| Posição | Gráfico | O Que Ver | Interpretação |
|---------|---------|-----------|---------------|
| **[1,1]** | Distribuição por Tipo | Barras horizontais | Tipo mais longo = mais comum |
| **[1,2]** | Público vs Privado | Pizza 🍕 | > 50% vermelho = forte SUS |
| **[1,3]** | Top 10 Bairros | Barras coloridas | Centro deve liderar |
| **[2,1]** | Histograma Distâncias | Frequência | Pico à esquerda = concentração urbana |
| **[2,2]** | Densidade por Raio | Área empilhada | Verde alto = boa cobertura urbana |
| **[2,3]** | Boxplot por Zona | Caixas + bigodes | Caixa pequena = zona homogênea |
| **[3,1]** | Mapa de Dispersão | Scatter lat/lon | Cluster central esperado |
| **[3,2]** | Cobertura Acumulada | Linha crescente | 80% em 10km = meta boa |
| **[3,3]** | Estatísticas | Tabela texto | Números-chave resumidos |

---

## 🎯 Principais Indicadores

### Números Ideais para Concórdia/SC

| Indicador | Valor Atual | Meta Recomendada | Status |
|-----------|-------------|------------------|--------|
| **Total de Estabelecimentos** | 418 | - | ✅ Base |
| **Georreferenciados** | 401 (95.9%) | > 95% | ✅ Excelente |
| **Estabelecimentos Públicos** | 98 (23.4%) | > 20% | ✅ Adequado |
| **Distância Média** | 3.97 km | < 5 km | ✅ Ótimo |
| **Cobertura Urbana (5km)** | ~80% | > 70% | ✅ Bom |
| **Cobertura Periurbana (10km)** | ~95% | > 85% | ✅ Excelente |

### Semáforo de Análise

| 🟢 Verde | 🟡 Amarelo | 🔴 Vermelho |
|----------|------------|-------------|
| Cobertura > 85% | 70-85% | < 70% |
| Dist. média < 5km | 5-10km | > 10km |
| Públicos > 20% | 15-20% | < 15% |
| Concentração urbana | Periurbana | Rural excessivo |

---

## 🔧 Personalizações Rápidas

### Mudar Centro de Referência

```python
# Linha ~50 do script
CENTRO_CONCORDIA = [-27.2335, -52.0238]  # Coordenadas [Lat, Lon]
```

### Ajustar Raios de Análise

```python
# Linha ~800 função criar_mapa_avancado_treelayer()
radius=5000,   # 5km → trocar para 7000 (7km)
radius=10000,  # 10km → trocar para 15000 (15km)
```

### Mudar Paleta de Cores

```python
# Linhas 55-68
COLORBREWER_SEQUENTIAL = {
    'BuGn_5': [...],    # Atual: azul-verde
    'PuRd_5': [...],    # Trocar: roxo-vermelho
}
```

**Paletas disponíveis:** https://colorbrewer2.org/

---

## ❓ Troubleshooting Expresso

| Problema | Solução Rápida |
|----------|----------------|
| 🚫 **Mapa não carrega** | Aguarde 30s, recarregue (F5), use Chrome |
| 🎨 **Cores erradas** | Desative modo alto contraste Windows |
| 🐌 **Lento no PC** | Desative heatmap, reduza estabelecimentos |
| ❌ **Erro ao executar** | `pip install pandas folium matplotlib` |
| 📱 **Mobile não funciona** | Use zoom pinch, rotacione para landscape |
| 🖨️ **Impressão cortada** | Abra PDF ao invés de PNG |

---

## 📁 Estrutura de Arquivos Gerados

```
03_RESULTADOS/
├── mapas/
│   ├── mapa_avancado_colorbrewer.html         # Mapa simples
│   └── mapa_avancado_treelayer_colorbrewer.html  # Mapa com TreeLayer ⭐
├── dashboard_completo_colorbrewer.png          # Dashboard visual (PNG)
├── dashboard_completo_colorbrewer.pdf          # Dashboard visual (PDF)
├── relatorio_analise_avancada_colorbrewer.md   # Relatório técnico
└── dados_processados_colorbrewer.csv           # Dados tabulares

docs/ (cópia para GitHub Pages)
├── mapa_avancado_colorbrewer.html
└── dashboard_completo_colorbrewer.html
```

---

## 🚀 Workflow Completo (Diagrama)

```
┌─────────────────────────────────────────────────────────┐
│  1️⃣ PREPARAR AMBIENTE                                    │
│  ├─ Ativar venv: geoprocessamento\Scripts\Activate.ps1 │
│  └─ Verificar dados: 01_DADOS\originais\               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  2️⃣ EXECUTAR DASHBOARD                                   │
│  ├─ python 02_SCRIPTS\dashboard_avancado_colorbrewer.py│
│  ├─ Aguardar 2-5 minutos ⏱️                             │
│  └─ Verificar mensagem "CONCLUÍDO COM SUCESSO!" ✅      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  3️⃣ EXPLORAR RESULTADOS                                  │
│  ├─ Mapa HTML: Navegador → Interagir com camadas       │
│  ├─ Dashboard PNG/PDF: Visualizador de imagens         │
│  └─ Relatório MD: VS Code ou navegador                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  4️⃣ ANÁLISE E DECISÕES                                   │
│  ├─ Identificar vazios assistenciais 🔍                 │
│  ├─ Avaliar distribuição público/privado 📊            │
│  ├─ Planejar novas unidades 🏥                          │
│  └─ Gerar apresentação para gestores 📽️                │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Atalhos de Documentação

| Documento | Para Quê | Tempo Leitura |
|-----------|----------|---------------|
| **Este Guia Rápido** | Referência instantânea | 3 min |
| `GUIA_DASHBOARD_COLORBREWER.md` | Tutorial completo | 30 min |
| `RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md` | Metodologia científica | 45 min |
| `APRESENTACAO_EXECUTIVA.md` | Slides para gestores | 15 min |
| `INDICE_GERAL_PROJETO.md` | Navegação completa | 5 min |

---

## 🎓 Conceitos em 30 Segundos

### ColorBrewer
> Paletas de cores cientificamente validadas para mapas, otimizadas para acessibilidade (daltonismo) e legibilidade.

### TreeLayerControl
> Controle hierárquico de camadas do mapa, permite organizar múltiplas camadas em grupos expansíveis (como pastas).

### Haversine
> Fórmula matemática que calcula distância entre dois pontos na superfície da Terra considerando sua curvatura.

### Heatmap
> Visualização de densidade espacial usando gradiente de cores (azul=baixo, verde=médio, vermelho=alto).

### MarkerCluster
> Agrupamento automático de marcadores próximos, melhora performance e clareza visual em mapas com muitos pontos.

---

## ✅ Checklist Pré-Apresentação

**Antes de apresentar para gestores:**

- [ ] Executar dashboard e verificar todos os arquivos gerados
- [ ] Abrir mapa HTML e testar controles (zoom, camadas, popups)
- [ ] Conferir números principais (total estabelecimentos, cobertura, distâncias)
- [ ] Identificar 2-3 insights principais para destacar
- [ ] Preparar resposta para: "Onde precisamos expandir?"
- [ ] Testar em projetor (resolução, cores, legibilidade)
- [ ] Backup em pen drive (HTML pode não funcionar em rede corporativa)
- [ ] Imprimir dashboard PDF (plano B se tecnologia falhar)

---

## 📞 Suporte Rápido

**Problemas técnicos:**  
📧 Abra issue no GitHub: [analise-saude-concordia/issues](https://github.com/caetanoronan/analise-saude-concordia/issues)

**Dúvidas metodológicas:**  
📖 Consulte: `04_DOCUMENTACAO/RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md`

**Personalização:**  
🔧 Edite: `02_SCRIPTS/dashboard_avancado_colorbrewer.py` (bem comentado)

---

**Versão:** 2.0 | **Atualizado:** Outubro 2025  
**Autor:** Ronan Armando Caetano | **Instituição:** UFSC  
**Licença:** CC BY-SA 4.0

---

💡 **Dica Final:** Salve este guia nos favoritos do navegador para consulta rápida!
