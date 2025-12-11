
# Análise Espacial dos Estabelecimentos de Saúde - Concórdia/SC

**Autor:** Ronan Armando Caetano  
**Instituições:** UFSC (Graduando em Ciências Biológicas) | IFSC (Técnico em Geoprocessamento)

---

## 🎯 Sobre o Projeto

Análise espacial completa dos **388 estabelecimentos de saúde** em Concórdia/SC utilizando técnicas avançadas de geoprocessamento. O projeto oferece **7 mapas interativos**, dashboards analíticos e relatórios técnicos profissionais.

### 📊 Principais Números
- **388 estabelecimentos** validados dentro do limite municipal
- **37 unidades públicas** (ESF, Postos, UBS, Policlínicas)
- **351 estabelecimentos privados** (Consultórios, Farmácias, Clínicas, Labs, Hospitais)
- **14 categorias** de estabelecimentos classificadas
- **311 polígonos de Voronoi** (áreas de influência)
- **200 setores censitários** mapeados
- **7 mapas interativos** publicados

---

## 🗺️ Mapas Interativos Disponíveis

Acesse o **Dashboard Interativo**: [https://caetanoronan.github.io/analise-saude-concordia/dashboard_interativo_saude.html](https://caetanoronan.github.io/analise-saude-concordia/dashboard_interativo_saude.html)

1. **Mapa Avançado ColorBrewer** - Análise por tipo de unidade com paleta ColorBrewer
2. **Mapa TreeLayer** - Hierarquia de camadas com múltiplas visualizações
3. **Postos Públicos** - Foco em estabelecimentos públicos (ESF/PS)
4. **Estabelecimentos Filtrados** - Visualização com filtro espacial rigoroso
5. **Todas as Unidades** - Visão geral com clusters dinâmicos
6. **Mapa Completo Corrigido** - Versão otimizada com Voronoi e setores
7. **🆕 Camadas Detalhadas** - 14 categorias | Voronoi colorido | Controle retrátil

---

## 🛠️ Tecnologias Utilizadas

### Linguagens e Bibliotecas
- **Python 3.14** (Análise e automação)
   - `pandas` - Manipulação de dados
   - `geopandas` - Análise espacial
   - `folium` - Mapas interativos
   - `shapely` - Operações geométricas
   - `matplotlib/seaborn` - Visualizações
   - `openpyxl` - Leitura de Excel

### Ferramentas
- **QGIS** - Geoprocessamento avançado
- **Jupyter Notebook** - Documentação interativa
- **GitHub Pages** - Publicação web
- **VS Code + Copilot** - Desenvolvimento assistido por IA
- **Git + GitKraken** - Controle de versão

### Fontes de Dados
- **CNES/DataSUS** - Cadastro Nacional de Estabelecimentos de Saúde
- **IBGE** - Limites municipais e setores censitários
- **OpenStreetMap** - Tiles para mapas base

---

## 📁 Estrutura do Repositório

## 📁 Estrutura do Repositório

```
Pesquisa_upas/
├── 01_DADOS/
│   ├── originais/           # Dados brutos (não versionados)
│   └── processados/         # Dados limpos (CSV, WKT)
├── 02_SCRIPTS/
│   ├── mapa_camadas_detalhadas.py          # 🆕 Mapa com 14 categorias
│   ├── atualizar_mapa_unidades_saude.py    # Mapa de todas as unidades
│   ├── dashboard_avancado_colorbrewer.py   # Dashboard com ColorBrewer
│   ├── ANALISE_ESPACIAL_corrigido.py       # Análise espacial geral
│   └── preparacao_qgis.py                  # Exportação para QGIS
├── 03_RESULTADOS/
│   ├── mapas/               # Mapas HTML interativos
│   └── shapefiles/          # Arquivos para QGIS (Voronoi, setores)
├── 04_DOCUMENTACAO/
│   ├── RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md
│   ├── Analise_Espacial_Concordia_Demonstrativo.ipynb
│   └── APRESENTACAO_EXECUTIVA.md
├── docs/                    # GitHub Pages (mapas publicados)
│   ├── dashboard_interativo_saude.html     # Dashboard principal
│   ├── mapa_camadas_detalhadas.html        # 🆕 Mapa com camadas
│   ├── mapa_avancado_colorbrewer.html
│   ├── mapa_unidades_saude_concordia.html
│   └── ...
├── SC_Municipios_2024/      # Shapefiles de limites municipais
├── INDICE_GERAL_PROJETO.md  # Navegação completa do projeto
└── README.md                # Este arquivo
```

---

## 🚀 Como Usar

### Visualização Online
Acesse diretamente os mapas interativos:
- **Dashboard Principal**: [https://caetanoronan.github.io/analise-saude-concordia/dashboard_interativo_saude.html](https://caetanoronan.github.io/analise-saude-concordia/dashboard_interativo_saude.html)
- **Mapa Camadas Detalhadas**: [https://caetanoronan.github.io/analise-saude-concordia/mapa_camadas_detalhadas.html](https://caetanoronan.github.io/analise-saude-concordia/mapa_camadas_detalhadas.html)

### Reprodução Local

1. **Clone o repositório**
   ```bash
   git clone https://github.com/caetanoronan/analise-saude-concordia.git
   cd analise-saude-concordia
   ```

2. **Instale as dependências**
   ```bash
   pip install pandas geopandas folium shapely matplotlib seaborn openpyxl
   ```

3. **Execute os scripts**
   ```bash
   python 02_SCRIPTS/mapa_camadas_detalhadas.py
   python 02_SCRIPTS/atualizar_mapa_unidades_saude.py
   ```

4. **Visualize os mapas**
   - Abra os arquivos `.html` em `docs/` ou `03_RESULTADOS/mapas/`

---

## 📊 Funcionalidades dos Mapas

### Mapa Camadas Detalhadas (NOVO! 🎨)
- ✅ **388 estabelecimentos** classificados em 14 categorias
- 📐 **Voronoi colorido** com 311 polígonos
- 🗺️ **Setores censitários** (200 subdivisões)
- 🔽 **Controle de camadas retrátil** (lado esquerdo)
- 📋 **Legenda completa** com contadores
- 🧭 **Rosa dos ventos** (N, S, L, O)
- 🎯 **Filtro espacial rigoroso** (dentro do limite municipal)

### Categorias de Estabelecimentos
- 🏥 **Públicos**: ESF (19) | Postos (14) | Policlínicas (2) | Centros de Saúde (1)
- 🩺 **Consultórios Médicos**: 187 unidades
- 🦷 **Consultórios Odontológicos**: 60 unidades
- 🏨 **Clínicas Especializadas**: 49 unidades
- 💊 **Farmácias**: 23 unidades
- 🔬 **Laboratórios**: 17 unidades (análises + prótese)
- 🏥 **Hospitais**: 4 unidades
- 🚑 **Emergência** (SAMU): 3 unidades
- 🏢 **Gestão/Outros**: 8 unidades

---

## 📖 Documentação

- **Relatório Técnico Completo**: [04_DOCUMENTACAO/RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md](04_DOCUMENTACAO/RELATORIO_TECNICO_ANALISE_ESPACIAL_CONCORDIA.md)
- **Apresentação Executiva**: [04_DOCUMENTACAO/APRESENTACAO_EXECUTIVA.md](04_DOCUMENTACAO/APRESENTACAO_EXECUTIVA.md)
- **Notebook Interativo**: [04_DOCUMENTACAO/Analise_Espacial_Concordia_Demonstrativo.ipynb](04_DOCUMENTACAO/Analise_Espacial_Concordia_Demonstrativo.ipynb)
- **Índice Geral**: [INDICE_GERAL_PROJETO.md](INDICE_GERAL_PROJETO.md)

---

## 🎓 Metodologia

1. **Coleta de Dados**: CNES/DataSUS (418 estabelecimentos)
2. **Filtragem Municipal**: Código IBGE 420430 (Concórdia)
3. **Validação Espacial**: Filtro rigoroso com GeoPandas (388 válidos)
4. **Classificação**: 14 categorias baseadas em TP_UNIDADE e nome
5. **Análise Espacial**: Voronoi, setores censitários, raios de cobertura
6. **Visualização**: Mapas Folium interativos com controle de camadas

---

## 🔍 Principais Insights

- ✅ **95,9%** dos estabelecimentos possuem coordenadas válidas
- ✅ **79,6%** dos postos públicos a menos de 5km do centro urbano
- ✅ **3,97 km** distância média dos estabelecimentos ao centro
- ✅ **Ampla diversidade** de serviços (consultórios, clínicas, labs, hospitais)
- ✅ **Cobertura equilibrada** entre zona urbana e periurbana

---

## 📝 Créditos e Licença

**Autor:** Ronan Armando Caetano  
**Graduação:** Ciências Biológicas - UFSC  
**Formação Técnica:** Geoprocessamento - IFSC  

**Fontes de Dados:**
- CNES/DataSUS (Ministério da Saúde)
- IBGE (Limites municipais e setores censitários)
- Município de Concórdia/SC

**Data de Elaboração:** Dezembro 2025

---

## 📧 Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato através do GitHub.

---

**Última Atualização:** Dezembro 2025 | **Versão:** 2.0 (Mapa Camadas Detalhadas)
Instituição: **IFSC - Técnico em Geoprocessamento**  
Assistência AI: **GitHub Copilot**  
Outubro 2025

---

Para dúvidas ou sugestões, abra uma issue no repositório ou entre em contato.
