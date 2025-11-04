# Copilot Instructions - Análise Espacial Estabelecimentos de Saúde Concórdia/SC

## Project Overview

Análise espacial completa dos estabelecimentos de saúde no município de Concórdia/SC utilizando técnicas de geoprocessamento. Processa dados do CNES (418 estabelecimentos, 401 com coordenadas válidas) para criar mapas interativos, dashboards analíticos e relatórios técnicos acessíveis em português brasileiro.

Key Outputs: Mapas Folium navegáveis, Jupyter notebooks interativos, relatórios técnicos em Markdown, dashboards consolidados, shapefiles para QGIS (todos em português brasileiro)

## Architecture & Data Flow

### Core Data Pipeline Pattern

Todos os scripts de análise seguem este pipeline de 5 estágios:

1. **Carregar Dados CNES** → `Tabela_estado_SC.csv` (base completa SC) + `Concordia_ps.xlsx` (dados específicos)
2. **Filtrar Município** → Código IBGE 420430 (Concórdia) com coordenadas válidas
3. **Calcular Distâncias** → Fórmula de Haversine para distância ao centro urbano (-27.2335, -52.0238)
4. **Classificar Estabelecimentos** → Público/privado baseado em critérios CNES (ESF, PS, tipo de unidade)
5. **Visualizar** → Mapas Folium + Matplotlib/Seaborn → `03_RESULTADOS/` directory

Example: See `Análise_da_distribuicao_PS_publico.py` (lines 1-150) for canonical implementation.

### Directory Structure

```
Pesquisa_upas/
├── 01_DADOS/                     # Datasets originais e processados
│   ├── originais/               # Tabela_estado_SC.csv, Concordia_ps.xlsx (NEVER modify)
│   └── processados/             # CSVs limpos (concordia_saude_simples.csv, etc.)
├── 02_SCRIPTS/                   # Códigos Python desenvolvidos
│   ├── Análise_da_distribuicao_PS_publico.py  # Análise postos públicos
│   ├── ANALISE_ESPACIAL_corrigido.py          # Análise espacial geral
│   ├── preparacao_qgis.py                     # Preparação dados QGIS
│   └── mapa_concordia.py                      # Mapas interativos
├── 03_RESULTADOS/               # Produtos gerados (HTML, PNG, shapefiles)
│   ├── mapas/                   # Mapas HTML interativos (5 mapas disponíveis)
│   └── shapefiles/              # Arquivos para QGIS (Voronoi, centroides)
├── 04_DOCUMENTACAO/             # Relatórios e documentação
│   ├── RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md  # Relatório principal (35 páginas)
│   ├── Analise_Espacial_Concordia_Demonstrativo.ipynb  # Notebook interativo
│   └── APRESENTACAO_EXECUTIVA.md                       # Slides para apresentação
├── .github/                     # Instruções para Copilot
└── INDICE_GERAL_PROJETO.md      # Navegação completa do projeto
```

Convention: Scripts escrevem em `03_RESULTADOS/`, NUNCA sobrescrever dados originais em `01_DADOS/originais/`.

## Critical Developer Workflows

### Running Analysis Scripts

```bash
# Ativar ambiente virtual (se disponível)
.venv\Scripts\activate

# Padrão de execução (maioria dos scripts são standalone)
python 02_SCRIPTS\Análise_da_distribuicao_PS_publico.py
python 02_SCRIPTS\ANALISE_ESPACIAL_corrigido.py
python 02_SCRIPTS\preparacao_qgis.py

# Scripts com interface CLI
python dashboard_simples.py
python gerar_mapas.py
```

Testing Strategy: Validação manual via inspeção dos mapas HTML gerados no navegador. Não existem testes automatizados.

### Data Processing Pattern

Padrão dual para carregamento de dados:

1. **Fonte primária**: `Tabela_estado_SC.csv` (base completa) → filtrar por código IBGE 420430
2. **Fonte alternativa**: `concordia_saude_simples.csv` (dados já processados)
3. **Fallback**: Dados de exemplo sintéticos para demonstração

Why? A base completa pode ser grande (16MB+), dados processados permitem execução mais rápida.

### Git Workflow

```bash
# Padrão: git add → commit com prefixo em português → push to main
git add 02_SCRIPTS/novo_script.py
git commit -m "Feat: adiciona análise de acessibilidade por transporte público"
git push origin main
```

Convention: Mensagens de commit em português, usar prefixos: `Feat:`, `Fix:`, `Docs:`, `Refactor:`

## Project-Specific Conventions

### Qualidade Geoespacial é NÃO-NEGOCIÁVEL

Toda visualização DEVE seguir padrões cartográficos:

• **Sistema de Coordenadas**: WGS84 (EPSG:4326) para mapas finais - requisito Folium
• **Operações**: Realizar em CRS projetado (EPSG:31982 SIRGAS 2000 UTM 22S) para precisão
• **Simplificação**: `simplify(100)` em metros antes da exportação - reduz tamanho HTML
• **Agregação**: `groupby()` com `aggfunc='sum'` para somatórios - padrão GeoPandas

Testing: Chrome DevTools → Rendering → Emular deficiências visuais (deuteranopia, protanopia, tritanopia)

Implementation: See `ANALISE_ESPACIAL_corrigido.py` (lines 80-120) for map configuration patterns.

### Padrões de Análise Espacial

1. **Centro de Referência**: Coordenadas fixas (-27.2335, -52.0238) - praça central de Concórdia
2. **Cálculo de Distância**: Fórmula de Haversine em km - precisão adequada para escala municipal
3. **Classificação Pública**: Critérios baseados em nome_fantasia, razao_social e tipo_unidade
4. **Raios de Análise**: 5km (urbano), 10km (periurbano), >10km (rural)

Example (from `Análise_da_distribuicao_PS_publico.py` lines 24-35):

```python
# Padrão: Centro fixo → Calcular distância → Classificar proximidade
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    # ... implementação Haversine
    return R * c
```

### Folium Map Patterns

Configuração padrão de controles:

• **LayerControl**: `collapsed=True, position='topleft'` - amigável ao mobile
• **Marcadores**: Cores diferenciadas (vermelho=público, azul=privado, preto=centro)
• **Círculos de Referência**: 5km, 10km, 20km com transparência
• **Popups**: HTML estruturado com informações detalhadas
• **HeatMap**: `radius=15, blur=10` para densidade espacial

Legend Injection (CRÍTICO):

```python
# MÉTODO CORRETO - injeta no elemento <html>
mapa.get_root().html.add_child(folium.Element(legend_html))

# MÉTODO ERRADO - quebra renderização
# mapa.get_root().add_child(folium.Element(legend_html))  # ❌ Não usar
```

### Output Standards

Todos os relatórios seguem esta estrutura:

1. **Header**: Título com informações do projeto e autor (UFSC)
2. **Resumo Executivo**: Principais números (418 estabelecimentos, 95.9% cobertura)
3. **Metodologia**: Descrição das técnicas de geoprocessamento aplicadas
4. **Resultados**: Análises estatísticas e visualizações
5. **Conclusões**: Insights para planejamento territorial
6. **Footer**: Créditos, fontes de dados, data de elaboração

Mobile-First: Mapas HTML responsivos, documentação Markdown para compatibilidade universal.

## Integration Points

### External APIs/Services

• **CNES/DataSUS**: Cadastro Nacional de Estabelecimentos de Saúde (dados offline)
• **IBGE**: Códigos municipais e setores censitários (dados offline)
• **OpenStreetMap**: Tiles para mapas base via Folium (online)

Rate limits: Nenhum documentado para uso offline, OSM tiles seguem política fair use.

### Dependencies

```python
# Geoespacial core
pandas     # 2.0+ - manipulação de dados
geopandas  # 0.14+ (quando disponível)
folium     # 0.15+ - mapas interativos baseados em Leaflet

# Visualização
matplotlib # 3.8+ - gráficos estatísticos
seaborn    # 0.12+ (quando disponível)

# Análise espacial
shapely    # 2.0+ (quando disponível para operações geométricas)

# Notebook
jupyter    # Para notebooks interativos

# Sistema
os, math   # Bibliotecas padrão Python
```

Dependency management: Sem `requirements.txt` formal. Scripts verificam imports e fazem fallback gracioso.

## Common Gotchas

### 1. Tipos de Dados em Coordenadas

Coordenadas podem vir como string no CSV - sempre converter para float:

```python
# Tratamento correto
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
df_clean = df.dropna(subset=['LAT', 'LON'])
```

### 2. Classificação de Estabelecimentos Públicos

Critérios múltiplos necessários - nome fantasia pode ser incompleto:

```python
# Implementação robusta
def eh_posto_publico(nome_fantasia, tipo_unidade, razao_social):
    criterios = [
        'ESF' in str(nome_fantasia).upper(),
        'PS ' in str(nome_fantasia).upper(),
        'MUNICIPIO' in str(razao_social).upper(),
        str(tipo_unidade) in ['1', '2', '70', '81']
    ]
    return any(criterios)
```

### 3. Performance com Grandes Datasets

Base completa SC tem 16MB+ - filtrar cedo no pipeline:

```python
# Filtrar primeiro, processar depois
df_sc = pd.read_csv('Tabela_estado_SC.csv', sep=';', low_memory=False)
df_concordia = df_sc[df_sc['CO_MUNICIPIO_GESTOR'] == 420430]  # Reduz de ~400k para ~400 linhas
```

### 4. Caminhos de Arquivo Windows

Scripts usam raw strings `r'path\file.ext'` - específico para Windows:

```python
# Windows-specific (atual)
dados = pd.read_csv(r'01_DADOS\processados\file.csv')

# Cross-platform (para refatoração futura)
import os
dados = pd.read_csv(os.path.join('01_DADOS', 'processados', 'file.csv'))
```

### 5. Fallback para Bibliotecas Ausentes

Nem todas as bibliotecas podem estar instaladas - implementar fallbacks:

```python
try:
    import seaborn as sns
    sns.set_palette("husl")
except ImportError:
    print("⚠️ Seaborn não disponível, usando matplotlib padrão")
```

## Key Files to Reference

• `Análise_da_distribuicao_PS_publico.py` (150 lines) - Padrão canônico: filtro municipal, cálculo distâncias, classificação público/privado, estatísticas
• `ANALISE_ESPACIAL_corrigido.py` (130 lines) - Mapas Folium com controles, múltiplas camadas, popups estruturados
• `preparacao_qgis.py` (50 lines) - Exportação para formatos geoespaciais (CSV com WKT, shapefiles)
• `dashboard_simples.py` (200 lines) - Visualizações matplotlib/seaborn, tratamento robusto de dados
• `RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md` - Documentação técnica completa (metodologia, resultados, conclusões)

## When Making Changes

1. **Novos tipos de análise**: Seguir padrão `Análise_da_distribuicao_PS_publico.py` (carregar → filtrar → calcular → visualizar)
2. **Modificar visualizações**: Verificar compatibilidade mobile e acessibilidade primeiro
3. **Integrações de API**: Implementar fallback para dados offline (padrão do projeto)
4. **Novos outputs**: Sempre salvar em `03_RESULTADOS/`, usar nomes descritivos em português
5. **Documentação**: Atualizar `INDICE_GERAL_PROJETO.md` se estrutura mudar

Testing Checklist:

• Mapas carregam corretamente no navegador
• Dados numéricos são válidos (sem NaN em coordenadas)
• Popups mostram informações corretas
• Layout funciona em tela pequena (< 768px)
• Arquivos de saída são gerados no diretório correto

## Principais Números do Projeto

### Estatísticas Chave para Referência:
- **418** estabelecimentos de saúde total identificados
- **401** com coordenadas válidas (**95,9%** de cobertura georreferenciada)
- **98** unidades públicas mapeadas (**23,4%** do total)
- **79,6%** dos postos públicos a menos de 5km do centro urbano
- **3,97 km** distância média dos estabelecimentos ao centro
- **16 ESFs** + **15 Postos de Saúde** públicos mapeados
- **5 mapas HTML** interativos gerados
- **35 páginas** de relatório técnico
- **4 pastas** organizacionais estruturadas

### Distribuição por Tipo (Top 5):
1. **Tipo 22** (Consultórios): 27 unidades
2. **Tipo 2** (ESF): 20 unidades  
3. **Tipo 39** (Laboratórios): 17 unidades
4. **Tipo 1** (Postos): 15 unidades
5. **Tipo 5** (Hospitais): 2 unidades

Last Updated: Outubro 2025 | Language: Português Brasileiro (code comments + outputs) | Institution: UFSC