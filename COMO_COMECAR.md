# 🎯 Como Começar com o Dashboard ColorBrewer

## ⚡ Início em 3 Passos

### 1. Execute o Dashboard
```powershell
python 02_SCRIPTS\dashboard_avancado_colorbrewer.py
```

### 2. Explore os Resultados
```powershell
# Mapa interativo
start 03_RESULTADOS\mapas\mapa_avancado_treelayer_colorbrewer.html

# Dashboard visual
start 03_RESULTADOS\dashboard_completo_colorbrewer.png
```

### 3. Leia a Documentação

**🚀 Você quer:**

| Se você precisa... | Leia este arquivo | Tempo |
|-------------------|------------------|-------|
| 💨 **Começar AGORA** | `04_DOCUMENTACAO/GUIA_RAPIDO_DASHBOARD.md` | 3 min |
| 📚 **Entender tudo em detalhes** | `04_DOCUMENTACAO/GUIA_DASHBOARD_COLORBREWER.md` | 30 min |
| 🎓 **Metodologia científica** | `04_DOCUMENTACAO/RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md` | 45 min |
| 🎤 **Apresentar para alguém** | `04_DOCUMENTACAO/APRESENTACAO_EXECUTIVA.md` | 15 min |
| 🗺️ **Navegar o projeto** | `INDICE_GERAL_PROJETO.md` | 5 min |

---

## 📊 O Que É Este Dashboard?

**Dashboard ColorBrewer** combina:
- ✅ **Mapa interativo** com controles hierárquicos (TreeLayerControl)
- ✅ **Paletas científicas** validadas para acessibilidade (ColorBrewer)
- ✅ **9 gráficos analíticos** (distribuição, densidade, cobertura)
- ✅ **Relatório técnico** gerado automaticamente
- ✅ **Dados processados** exportados em CSV

**Resultado:** Análise espacial completa de 418 estabelecimentos de saúde em Concórdia/SC.

---

## 🎨 Por Que ColorBrewer?

**ColorBrewer** são paletas de cores desenvolvidas por cartógrafos que garantem:

1. 👁️ **Acessibilidade** - Funciona para daltonismo (8% da população masculina)
2. 📖 **Legibilidade** - Clara em tela E impressão
3. 🧪 **Cientificidade** - Padrão internacional em geoprocessamento
4. 🎯 **Diferenciação** - Cores distintas mesmo com muitas categorias

---

## 🗺️ Principais Recursos do Mapa

### TreeLayerControl (Controle Hierárquico)
Organiza camadas em grupos expansíveis como pastas:

```
📂 Estabelecimentos de Saúde
  ├─ 🔴 Públicos (ESF, PS, UBS)
  └─ ⚪ Privados (Clínicas, Labs)
📂 Contexto Geográfico
  ├─ 🔵 Limite Municipal
  ├─ 🏛️ Centro Urbano
  └─ 🗺️ Municípios Vizinhos
📂 Análise Espacial
  ├─ 🟢 Raio 5km (Urbano)
  ├─ 🟠 Raio 10km (Periurbano)
  ├─ 🌡️ Mapa de Calor (Densidade)
  └─ 📍 Clusters Interativos
```

### Interações Disponíveis
- **Zoom:** Roda do mouse ou botões +/-
- **Pan:** Clicar e arrastar
- **Ligar/Desligar camadas:** Checkboxes no controle
- **Ver detalhes:** Clicar nos marcadores
- **Expandir clusters:** Clicar nos números

---

## 📈 Dashboard Visual (9 Gráficos)

| Gráfico | O Que Mostra | Para Que Serve |
|---------|--------------|----------------|
| **Distribuição por Tipo** | Barras de quantidade | Identificar categorias mais comuns |
| **Público vs Privado** | Pizza de proporção | Avaliar presença do SUS |
| **Top 10 Bairros** | Barras coloridas | Encontrar concentrações |
| **Histograma Distâncias** | Frequência | Ver dispersão espacial |
| **Densidade por Raio** | Área empilhada | Analisar cobertura por zona |
| **Boxplot por Zona** | Distribuição estatística | Comparar zonas urbana/rural |
| **Mapa de Dispersão** | Scatter lat/lon | Visualizar distribuição geográfica |
| **Cobertura Acumulada** | Linha crescente | Calcular % atendimento por raio |
| **Estatísticas Resumidas** | Tabela | Números-chave consolidados |

**Formato:** PNG alta resolução + PDF vetorial (impressão)

---

## 🔧 Personalização Rápida

### Mudar Centro de Referência
```python
# Linha ~50 do script dashboard_avancado_colorbrewer.py
CENTRO_CONCORDIA = [-27.2335, -52.0238]  # [Latitude, Longitude]
```

### Ajustar Raios de Análise
```python
# Linha ~800 na função criar_mapa_avancado_treelayer()
radius=5000,   # 5km urbano → ajustar para sua necessidade
radius=10000,  # 10km periurbano
radius=20000,  # 20km rural
```

### Trocar Paleta de Cores
```python
# Linhas 55-68 - Escolha em https://colorbrewer2.org/
COLORBREWER_SEQUENTIAL = {
    'BuGn_5': [...],  # Azul-verde (atual)
    'PuRd_5': [...],  # Roxo-vermelho (alternativa)
}
```

---

## 📁 Arquivos Gerados

Após executar, encontre em `03_RESULTADOS/`:

| Arquivo | Tipo | Para Que Serve |
|---------|------|----------------|
| `mapa_avancado_treelayer_colorbrewer.html` | Mapa | Navegação interativa (melhor) |
| `mapa_avancado_colorbrewer.html` | Mapa | Versão simplificada |
| `dashboard_completo_colorbrewer.png` | Imagem | Visualização rápida |
| `dashboard_completo_colorbrewer.pdf` | PDF | Impressão vetorial |
| `relatorio_analise_avancada_colorbrewer.md` | Markdown | Relatório técnico completo |
| `dados_processados_colorbrewer.csv` | CSV | Dados para análise externa |

**Cópia em `docs/`:** Arquivos HTML são copiados para publicação via GitHub Pages.

---

## ❓ Resolução Rápida de Problemas

| Problema | Solução |
|----------|---------|
| 🚫 Mapa não carrega | Aguarde 30s, atualize (F5), use Chrome |
| 🎨 Cores estranhas | Desative modo alto contraste do Windows |
| 🐌 Lento | Desative heatmap, reduza estabelecimentos |
| ❌ Erro Python | `pip install pandas folium matplotlib` |
| 📱 Mobile ruim | Use landscape, zoom com dois dedos |
| 🖨️ Impressão cortada | Use PDF ao invés de PNG |

---

## 📚 Navegação da Documentação

```
📂 04_DOCUMENTACAO/
│
├─ ⚡ GUIA_RAPIDO_DASHBOARD.md
│   └─ Referência de 1 página (3 min)
│      ✅ Atalhos de comando
│      ✅ Tabelas de cores
│      ✅ Troubleshooting expresso
│
├─ 📊 GUIA_DASHBOARD_COLORBREWER.md
│   └─ Tutorial completo (30 min)
│      ✅ Conceitos detalhados
│      ✅ Guia de uso passo a passo
│      ✅ Personalização avançada
│      ✅ FAQ extensa
│      ✅ Referências científicas
│
├─ 📖 RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md
│   └─ Metodologia científica (45 min)
│      ✅ Revisão de literatura
│      ✅ Métodos de análise
│      ✅ Resultados estatísticos
│      ✅ Discussão crítica
│
├─ 🎤 APRESENTACAO_EXECUTIVA.md
│   └─ Slides para apresentação (15 min)
│      ✅ Resumo executivo
│      ✅ Principais números
│      ✅ Visualizações-chave
│
└─ 💻 Analise_Espacial_Concordia_Demonstrativo.ipynb
    └─ Notebook interativo (execute célula por célula)
       ✅ Código executável
       ✅ Explicações inline
       ✅ Gráficos interativos
```

---

## 🎯 Fluxo de Trabalho Recomendado

### Para Primeira Execução (30 min total)
1. ⚡ Leia **GUIA_RAPIDO_DASHBOARD.md** (3 min)
2. 🔧 Execute `python 02_SCRIPTS\dashboard_avancado_colorbrewer.py` (3 min)
3. 🗺️ Explore mapa HTML no navegador (10 min)
4. 📊 Analise dashboard PNG/PDF (5 min)
5. 📖 Consulte seções relevantes do **GUIA_DASHBOARD_COLORBREWER.md** (10 min)

### Para Apresentação Acadêmica
1. 📚 Leia **RELATORIO_TECNICO** completo (45 min)
2. 🎤 Prepare slides baseado em **APRESENTACAO_EXECUTIVA.md** (20 min)
3. 💻 Teste **Notebook Jupyter** interativo (15 min)
4. 🔍 Identifique 3-5 insights principais dos mapas (10 min)
5. 📝 Elabore script de apresentação (20 min)

### Para Customização
1. 📖 Leia seção "Personalização" do **GUIA_DASHBOARD_COLORBREWER.md** (10 min)
2. 🔧 Edite script Python conforme necessidade (30 min)
3. 🧪 Teste mudanças iterativamente (20 min)
4. 📋 Documente alterações no README (10 min)

---

## 🎓 Conceitos-Chave em 1 Minuto

**ColorBrewer:** Paletas de cores cientificamente validadas para mapas.  
**TreeLayerControl:** Organização hierárquica de camadas em árvore.  
**Haversine:** Fórmula para calcular distância na superfície da Terra.  
**Heatmap:** Visualização de densidade com gradiente de cores.  
**MarkerCluster:** Agrupamento automático de marcadores próximos.  

---

## 🏆 Números do Projeto

| Indicador | Valor Atual |
|-----------|-------------|
| 📍 **Estabelecimentos** | 418 total |
| 🗺️ **Georreferenciados** | 401 (95.9%) |
| 🏥 **Públicos** | 98 (23.4%) |
| 📏 **Distância Média** | 3.97 km |
| ✅ **Cobertura Urbana** | ~80% em 5km |

**Status:** ✅ Projeto completo e documentado

---

## 📞 Suporte

**Problemas técnicos:** Abra issue no GitHub  
**Dúvidas metodológicas:** Consulte RELATORIO_TECNICO  
**Personalização:** Edite scripts (bem comentados)  

---

**Última atualização:** Outubro 2025  
**Autor:** Ronan Armando Caetano | **UFSC**  
**Licença:** CC BY-SA 4.0

---

💡 **Próximo passo:** Abra `04_DOCUMENTACAO/GUIA_RAPIDO_DASHBOARD.md` e comece! 🚀
