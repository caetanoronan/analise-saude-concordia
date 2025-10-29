# ESTRUTURA ORGANIZACIONAL DO PROJETO

## 📁 Organização dos Arquivos

### 📂 01_DADOS
**Dados utilizados no projeto**

#### 📂 01_DADOS/originais
- `Tabela_estado_SC.csv` - Base completa do CNES para SC
- `Concordia_ps.xlsx` - Dados específicos de Concórdia
- `SC_setores_CD2022.gpkg` - Setores censitários de SC

#### 📂 01_DADOS/processados  
- `estabelecimentos_concordia_qgis.csv` - Dados limpos para QGIS
- `estabelecimentos_concordia_wkt.csv` - Dados com geometria WKT
- `concordia_saude_simples.csv` - Dados simplificados

### 📂 02_SCRIPTS
**Códigos Python desenvolvidos**

- `Análise_da_distribuicao_PS_publico.py` - Análise de postos públicos
- `ANALISE_ESPACIAL_corrigido.py` - Análise espacial geral
- `preparacao_qgis.py` - Preparação dados para QGIS
- `mapa_concordia.py` - Geração de mapas interativos
- `Separação_mun_concordia.py` - Filtro municipal
- `concordia_saude.py` - Script principal

### 📂 03_RESULTADOS  
**Produtos gerados pela análise**

#### 📂 03_RESULTADOS/mapas
- `mapa_unidades_saude_concordia.html` - Mapa geral interativo
- `mapa_postos_publicos_concordia.html` - Foco postos públicos  
- `mapa_estabelecimentos_concordia.html` - ESF vs PS
- `mapa_concordia_analise.html` - Análise completa

#### 📂 03_RESULTADOS/shapefiles
- `areas_influencia_voronoi.*` - Áreas de influência
- `voronoi_recortado.*` - Voronoi recortado
- `Centroide_concordia.*` - Centroide municipal
- `Concordia_sencitario.*` - Setores censitários

### 📂 04_DOCUMENTACAO
**Documentação e relatórios**

- `RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md` - Relatório principal
- `METADADOS_estabelecimentos.txt` - Metadados dos dados
- `README_ORGANIZACIONAL.md` - Este arquivo
- Apresentações e documentos complementares

---

## 🎯 PRINCIPAIS PRODUTOS

### 1. **Relatório Técnico Principal**
📄 `04_DOCUMENTACAO/RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md`

Documento completo com:
- Metodologia detalhada
- Resultados e análises
- Visualizações e mapas
- Conclusões e recomendações

### 2. **Mapas Interativos**
🗺️ `03_RESULTADOS/mapas/`

- **mapa_unidades_saude_concordia.html**: Visão geral (418 unidades)
- **mapa_postos_publicos_concordia.html**: Foco público (98 unidades)
- **mapa_estabelecimentos_concordia.html**: ESF vs PS

### 3. **Dados Processados**
📊 `01_DADOS/processados/`

Datasets limpos e estruturados para:
- Análises estatísticas
- Importação em QGIS
- Visualizações interativas

### 4. **Scripts Reproduzíveis**  
💻 `02_SCRIPTS/`

Códigos Python documentados para:
- Reprodução das análises
- Adaptação para outros municípios
- Extensão dos estudos

---

## 📈 RESUMO DOS RESULTADOS

### Principais Números
- **418** estabelecimentos de saúde total
- **401** com coordenadas válidas (95,9%)
- **98** unidades públicas mapeadas
- **78** postos públicos a menos de 5km do centro (79,6%)
- **3,97km** distância média ao centro urbano

### Distribuição por Tipo
- **ESF**: 16 unidades (Estratégia Saúde da Família)
- **PS**: 15 unidades (Postos de Saúde)  
- **Consultórios**: 27 unidades
- **Laboratórios**: 17 unidades
- **Hospitais**: 2 unidades
- **Outros**: 21 unidades

---

## 🔄 FLUXO DE TRABALHO

```
Dados Originais (CNES) 
    ↓
Scripts de Processamento
    ↓  
Dados Limpos + Análises
    ↓
Mapas + Visualizações
    ↓
Relatório Final
```

---

## 🛠️ TECNOLOGIAS UTILIZADAS

- **Python**: pandas, folium, geopandas, matplotlib
- **QGIS**: Análise espacial e Voronoi
- **HTML/CSS**: Mapas interativos
- **Markdown**: Documentação

---

## 📞 CONTATO

**Autor:** Caetano Ronan  
**Instituição:** UFSC  
**Projeto:** Análise Espacial Estabelecimentos de Saúde - Concórdia/SC  
**Data:** Outubro 2025