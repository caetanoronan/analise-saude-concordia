
# Análise Espacial dos Estabelecimentos de Saúde - Concórdia/SC

**Autor:** Ronan Armando Caetano  
**Instituição:** IFSC - Técnico em Geoprocessamento

## Referências de Software Utilizado

- **Python** (Análise e automação)
   - pandas
   - numpy
   - folium
   - matplotlib
   - seaborn
   - geopandas
   - shapely
- **QGIS** (Geoprocessamento avançado, Voronoi, shapefiles)
- **Jupyter Notebook** (Documentação interativa)
- **GitHub Pages** (Publicação web)
- **VS Code** (Ambiente de desenvolvimento)
- **Git** (Controle de versão)
- **Copilot** (Assistente de programação AI)

## O que subir para o repositório

**Necessário para publicação e reprodutibilidade:**
- Pasta `docs/` com mapas HTML e dashboards PNG
   - `mapa_avancado_colorbrewer.html`
   - `mapa_estabelecimentos_concordia.html`
   - `mapa_unidades_saude_concordia.html`
   - `DASHBOARD_ANALISE_ESPACIAL_CONCORDIA.png`
- Pasta `02_SCRIPTS/` com scripts Python principais
   - `dashboard_simples.py`
   - `ANALISE_ESPACIAL_corrigido.py`
   - `Análise_da_distribuicao_PS_publico.py`
   - `mapa_concordia.py`
   - `preparacao_qgis.py`
- Pasta `01_DADOS/processados/` com dados limpos
   - `concordia_saude_simples.csv`
   - `estabelecimentos_concordia_qgis.csv`
   - `estabelecimentos_concordia_wkt.csv`
- Pasta `03_RESULTADOS/shapefiles/` com shapefiles gerados
   - `areas_influencia_voronoi.*`
   - `voronoi_recortado.*`
   - `Centroide_concordia.*`
   - `Concordia_sencitario.*`
- Pasta `04_DOCUMENTACAO/` com relatórios e notebooks
   - `RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md`
   - `Analise_Espacial_Concordia_Demonstrativo.ipynb`
   - `APRESENTACAO_EXECUTIVA.md`
- Arquivos de metadados e README
   - `METADADOS_estabelecimentos.txt`
   - `README.md`
   - `README_ORGANIZACIONAL.md`
   - `INDICE_GERAL_PROJETO.md`

**Não subir:**  
- Dados originais brutos (CNES completo, Excel original)
- Arquivos temporários, outputs intermediários, PDFs de referência

---

### Exemplo de Estrutura Final

```
docs/
   mapa_avancado_colorbrewer.html
   mapa_estabelecimentos_concordia.html
   mapa_unidades_saude_concordia.html
   DASHBOARD_ANALISE_ESPACIAL_CONCORDIA.png
01_DADOS/processados/
   concordia_saude_simples.csv
   estabelecimentos_concordia_qgis.csv
   estabelecimentos_concordia_wkt.csv
02_SCRIPTS/
   dashboard_simples.py
   ANALISE_ESPACIAL_corrigido.py
   Análise_da_distribuicao_PS_publico.py
   mapa_concordia.py
   preparacao_qgis.py
03_RESULTADOS/shapefiles/
   areas_influencia_voronoi.*
   voronoi_recortado.*
   Centroide_concordia.*
   Concordia_sencitario.*
04_DOCUMENTACAO/
   RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md
   Analise_Espacial_Concordia_Demonstrativo.ipynb
   APRESENTACAO_EXECUTIVA.md
METADADOS_estabelecimentos.txt
README.md
README_ORGANIZACIONAL.md
INDICE_GERAL_PROJETO.md
```

---

### Créditos

Projeto realizado por **Ronan Armando Caetano**  
Instituição: **IFSC - Técnico em Geoprocessamento**  
Assistência AI: **GitHub Copilot**  
Outubro 2025

---

Para dúvidas ou sugestões, abra uma issue no repositório ou entre em contato.
