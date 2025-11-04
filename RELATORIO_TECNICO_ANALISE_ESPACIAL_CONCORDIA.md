# ANÁLISE ESPACIAL DOS ESTABELECIMENTOS DE SAÚDE EM CONCÓRDIA/SC

## Relatório Técnico

---

**Autor:** Caetano Ronan  
**Instituição:** Universidade Federal de Santa Catarina (UFSC)  
**Data:** Outubro de 2025  
**Disciplina:** [Nome da Disciplina]  

---

## RESUMO EXECUTIVO

Este relatório apresenta uma análise espacial abrangente dos estabelecimentos de saúde no município de Concórdia, Santa Catarina. A pesquisa utilizou técnicas de geoprocessamento, análise estatística e visualização de dados para compreender a distribuição territorial dos serviços de saúde pública e privada na região.

**Principais Resultados:**
- **418 unidades de saúde** identificadas no município
- **401 unidades** com coordenadas geográficas válidas para análise
- **98 postos públicos** mapeados (ESF e PS)
- **78 unidades públicas** localizadas dentro de 5km do centro urbano
- Distância média dos postos públicos ao centro: **3,97 km**

---

## 1. INTRODUÇÃO

### 1.1 Contextualização

A análise da distribuição espacial de serviços de saúde é fundamental para o planejamento territorial e a garantia do acesso equitativo da população aos cuidados médicos. Em municípios médios como Concórdia/SC, compreender a configuração espacial dos estabelecimentos de saúde contribui para:

- Identificação de áreas com déficit de cobertura
- Otimização da localização de novos serviços
- Planejamento de rotas de transporte sanitário
- Análise de acessibilidade geográfica

### 1.2 Objetivos

**Objetivo Geral:**
Analisar a distribuição espacial dos estabelecimentos de saúde em Concórdia/SC utilizando técnicas de geoprocessamento.

**Objetivos Específicos:**
1. Mapear e categorizar todas as unidades de saúde do município
2. Analisar a distribuição geográfica dos serviços públicos e privados
3. Calcular métricas de acessibilidade geográfica
4. Criar visualizações interativas para análise territorial
5. Identificar padrões de concentração e dispersão dos serviços

---

## 2. METODOLOGIA

### 2.1 Fonte de Dados

- **Base Principal:** Cadastro Nacional de Estabelecimentos de Saúde (CNES)
- **Dados Geográficos:** Coordenadas WGS84 (EPSG:4326)
- **Período de Referência:** Dados atualizados até 2025
- **Área de Estudo:** Município de Concórdia (Código IBGE: 420430)

### 2.2 Ferramentas Utilizadas

- **Python:** Análise de dados e geoprocessamento
  - pandas: Manipulação de dados
  - folium: Mapas interativos
  - matplotlib/seaborn: Visualizações
  - geopandas: Análise espacial
- **QGIS:** Geoprocessamento avançado e análise de Voronoi
- **Shapely:** Operações geométricas

### 2.3 Classificação dos Estabelecimentos

Os estabelecimentos foram categorizados segundo o CNES:

| Tipo | Código | Descrição | Quantidade |
|------|--------|-----------|------------|
| ESF | 2 | Estratégia Saúde da Família | 16 |
| PS | 1 | Posto de Saúde | 15 |
| Hospital | 5 | Hospital Geral | 2 |
| Consultório | 22 | Consultório Isolado | 27 |
| Laboratório | 39 | Serviço de Apoio Diagnóstico | 17 |
| Outros | Variados | Demais tipos | 21 |

### 2.4 Métricas Calculadas

1. **Distribuição por Tipo:** Contagem e percentual por categoria
2. **Análise de Proximidade:** Distâncias ao centro urbano
3. **Densidade Espacial:** Concentração por área
4. **Cobertura Territorial:** Áreas de influência (Voronoi)
5. **Acessibilidade:** Raios de atendimento

---

## 3. RESULTADOS

### 3.1 Panorama Geral

#### Total de Estabelecimentos por Categoria

```
ESTABELECIMENTOS DE SAÚDE - CONCÓRDIA/SC
Total Mapeado: 418 unidades
Válidos para análise: 401 unidades (95,9%)

DISTRIBUIÇÃO POR SETOR:
• Público: 98 unidades (24,4%)
• Privado: 303 unidades (75,6%)
```

#### Estabelecimentos Públicos Detalhados

```
POSTOS PÚBLICOS DE SAÚDE - ANÁLISE DETALHADA
Total: 98 unidades

Por Tipo de Serviço:
• Consultórios (Tipo 22): 27 unidades (27,6%)
• ESF (Tipo 2): 20 unidades (20,4%)  
• Laboratórios (Tipo 39): 17 unidades (17,3%)
• Postos de Saúde (Tipo 1): 15 unidades (15,3%)
• Outros: 19 unidades (19,4%)
```

### 3.2 Análise de Acessibilidade Geográfica

#### Distâncias ao Centro Urbano

| Métrica | Valor |
|---------|-------|
| Distância Média | 3,97 km |
| Posto Mais Próximo | 0,03 km |
| Posto Mais Distante | 47,35 km |
| Unidades ≤ 5km do centro | 78/98 (79,6%) |

#### Distribuição Espacial

A análise revelou:

- **Concentração Central:** 79,6% dos postos públicos estão a menos de 5km do centro
- **Dispersão Rural:** Presença de unidades até 47km do centro urbano
- **Cobertura Equilibrada:** ESFs distribuídas estrategicamente nos bairros periféricos

### 3.3 Principais Estabelecimentos Públicos

#### No Centro Urbano (0-2km)
1. **JCC Psicologia e Consultoria** - Centro - 0,3 km
2. **Clínica Psicológica Concordia** - Centro - 0,5 km  
3. **Farmácia Municipal** - Centro - 0,6 km
4. **Hospital São Francisco** - Centro - 0,2 km
5. **CAPS II** - Centro - 0,2 km

#### ESFs Estratégicas
1. **ESF Novo Horizonte** - 2,4 km
2. **ESF Guilherme Reich** - 1,5 km
3. **ESF Salete** - 2,0 km
4. **ESF São Cristóvão** - 3,7 km
5. **ESF Industriários** - 1,7 km

#### Postos Rurais (Maior Distância)
1. **ESF Estados** - 47,4 km
2. **PS São Paulo** - 36,6 km
3. **PS Terra Vermelha** - 21,2 km

### 3.4 Análise de Densidade e Padrões

#### Concentração por Região

1. **Centro:** Alta densidade de consultórios especializados
2. **Bairros Residenciais:** ESFs bem distribuídas
3. **Área Rural:** Postos de Saúde em localidades estratégicas
4. **Periferia:** Boa cobertura de atenção básica

#### Padrões Identificados

- **Hierarquia Espacial:** Centro → Bairros → Rural
- **Complementaridade:** ESFs na periferia, especialidades no centro
- **Acessibilidade:** 79,6% da atenção básica a menos de 5km

---

## 4. VISUALIZAÇÕES E MAPAS

### 4.1 Produtos Cartográficos Gerados

1. **mapa_unidades_saude_concordia.html**
   - Mapa interativo com todas as 401 unidades
   - Marcadores coloridos por tipo de estabelecimento
   - Pop-ups informativos com detalhes

2. **mapa_postos_publicos_concordia.html**
   - Foco nos 98 estabelecimentos públicos
   - Análise de raios de atendimento
   - Mapa de calor da distribuição

3. **mapa_estabelecimentos_concordia.html**
   - Análise ESF vs PS
   - Marcadores diferenciados por categoria
   - Centro geográfico marcado

### 4.2 Análise de Voronoi

Foram gerados diagramas de Voronoi para determinar áreas de influência:

- **Arquivo:** `areas_influencia_voronoi.shp`
- **Método:** Polígonos de Thiessen
- **Resultado:** Delimitação de territórios de atendimento
- **Aplicação:** Planejamento de novas unidades

---

## 5. ARQUIVOS DE DADOS GERADOS

### 5.1 Dados Estruturados

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `estabelecimentos_concordia_qgis.csv` | Dados limpos para QGIS | Análise espacial |
| `estabelecimentos_concordia_wkt.csv` | Geometrias WKT | Importação direta |
| `concordia_saude_simples.csv` | Dados simplificados | Visualização rápida |

### 5.2 Arquivos Geoespaciais

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `areas_influencia_voronoi.*` | Shapefile | Áreas de influência |
| `voronoi_recortado.*` | Shapefile | Voronoi recortado |
| `Projeto_Concordia.gpkg` | GeoPackage | Projeto completo |

---

## 6. ANÁLISE CRÍTICA E DISCUSSÃO

### 6.1 Pontos Fortes da Distribuição

1. **Boa Cobertura Central:** 79,6% dos serviços públicos próximos ao centro
2. **ESFs Bem Posicionadas:** Estratégia de territorialização efetiva
3. **Diversidade de Serviços:** 418 estabelecimentos para atender diferentes demandas
4. **Integração Público-Privada:** Complementaridade entre setores

### 6.2 Desafios Identificados

1. **Distâncias Rurais:** Algumas localidades a mais de 40km dos serviços
2. **Concentração Urbana:** Possível sobrecarga no centro
3. **Lacunas Territoriais:** Áreas com menor densidade de cobertura

### 6.3 Recomendações

1. **Fortalecimento Rural:** Ampliar presença de ESFs em áreas remotas
2. **Transporte Sanitário:** Melhorar sistemas de deslocamento
3. **Telemedicina:** Implementar soluções digitais para áreas isoladas
4. **Monitoramento Contínuo:** Acompanhar mudanças demográficas

---

## 7. CONCLUSÕES

### 7.1 Síntese dos Resultados

A análise espacial dos estabelecimentos de saúde em Concórdia/SC revelou uma distribuição territorialmente organizada, com características específicas:

1. **Estrutura Hierárquica Bem Definida**
   - Centro urbano concentra especialidades
   - Bairros residenciais com ESFs
   - Área rural com postos estratégicos

2. **Boa Acessibilidade Geral**
   - 79,6% dos serviços públicos a menos de 5km do centro
   - Distância média de 3,97km aos postos públicos
   - Cobertura territorial adequada

3. **Diversidade de Oferta**
   - 418 estabelecimentos no total
   - Mix equilibrado público-privado
   - Serviços desde atenção básica até alta complexidade

### 7.2 Contribuições do Estudo

1. **Metodológica:** Demonstração de técnicas de análise espacial aplicadas à saúde
2. **Técnica:** Geração de base de dados georreferenciados confiável
3. **Aplicada:** Subsídios para planejamento territorial da saúde
4. **Acadêmica:** Contribuição para estudos de geografia da saúde

### 7.3 Limitações e Estudos Futuros

**Limitações:**
- Análise baseada apenas em localização geográfica
- Não consideração de aspectos socioeconômicos
- Ausência de dados populacionais detalhados

**Estudos Futuros:**
- Incorporar análise de demanda populacional
- Avaliar qualidade e capacidade dos serviços
- Analisar fluxos de pacientes
- Estudar acessibilidade por transporte público

---

## REFERÊNCIAS

1. BRASIL. Ministério da Saúde. Cadastro Nacional de Estabelecimentos de Saúde - CNES. 2025.

2. IBGE. Instituto Brasileiro de Geografia e Estatística. Códigos municipais. 2025.

3. OSM. OpenStreetMap Contributors. Dados geográficos colaborativos. 2025.

---

## ANEXOS

### Anexo A - Scripts Python Desenvolvidos
- `Análise_da_distribuicao_PS_publico.py`: Análise focada em postos públicos
- `ANALISE_ESPACIAL_corrigido.py`: Análise espacial geral
- `preparacao_qgis.py`: Preparação de dados para QGIS
- `mapa_concordia.py`: Geração de mapas interativos

### Anexo B - Arquivos de Dados
- Datasets CSV processados
- Shapefiles gerados
- Mapas HTML interativos

### Anexo C - Metadados
- Sistema de coordenadas: WGS84 (EPSG:4326)
- Precisão das coordenadas: 6 casas decimais
- Data de atualização: Outubro 2025

---

**Relatório elaborado utilizando técnicas de geoprocessamento e análise espacial**  
**Universidade Federal de Santa Catarina - UFSC**  
**Outubro de 2025**