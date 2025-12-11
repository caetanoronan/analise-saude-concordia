# 📊 Guia Completo do Dashboard ColorBrewer

## 🎯 O Que É Este Dashboard?

Este dashboard é uma **ferramenta de análise espacial avançada** que combina **visualização interativa** com **paletas de cores cientificamente validadas** (ColorBrewer) para analisar estabelecimentos de saúde em Concórdia/SC.

### Por Que "ColorBrewer"?

**ColorBrewer** é uma paleta de cores desenvolvida por cartógrafos para garantir:

✅ **Acessibilidade** - Visível para pessoas com daltonismo  
✅ **Clareza** - Distinção visual entre categorias  
✅ **Legibilidade** - Funciona em impressão e tela  
✅ **Cientificidade** - Padrão internacional em geoprocessamento  

---

## 🗺️ Componentes do Dashboard

### 1. **Mapa Interativo com TreeLayerControl**

O mapa principal usa um controle de camadas hierárquico (TreeLayerControl) que organiza as informações em grupos expansíveis:

#### 📍 Camadas Disponíveis:

**🏥 Estabelecimentos de Saúde** (grupo principal)
- **Públicos (ESF/PS)** - Marcadores vermelhos
  - Estratégia Saúde da Família (ESF)
  - Postos de Saúde (PS)
  - Unidades Básicas de Saúde (UBS)
  
- **Privados/Outros** - Marcadores cinza
  - Consultórios particulares
  - Clínicas especializadas
  - Laboratórios
  - Hospitais privados

**🗺️ Contexto Geográfico**
- **Limite Municipal** - Polígono azul tracejado de Concórdia
- **Municípios Vizinhos** - Contexto regional (~60km)
- **Centro Urbano** - Marcador preto (praça central)

**📊 Análise Espacial**
- **Mapa de Calor (Densidade)** - Concentração de estabelecimentos
- **Raios de Análise** - 5km (urbano), 10km (periurbano), 20km (rural)
- **Clusters Interativos** - Agrupamento automático por zoom

#### 🎨 Paletas ColorBrewer Aplicadas:

| Tipo | Paleta | Uso | Cores |
|------|--------|-----|-------|
| **Sequencial** | BuGn (5 classes) | Distâncias ao centro | 🟦🟩🟩🟩🟢 |
| **Qualitativo** | Set1 (8 classes) | Tipos de estabelecimento | 🔴🔵🟢🟣🟠🟡🟤🩷 |
| **Divergente** | RdYlGn | Cobertura (bom ↔ ruim) | 🔴🟠🟡🟢🟢 |

---

### 2. **Dashboard Visual Completo** (PNG/PDF)

O dashboard visual é composto por **9 gráficos analíticos** organizados em grid 3x3:

#### 📈 Gráficos Gerados:

**Linha 1 - Distribuição e Concentração**
1. **Distribuição por Tipo** - Barras horizontais mostrando quantidade por categoria
2. **Público vs Privado** - Pizza comparando proporção de estabelecimentos
3. **Top 10 Bairros** - Barras coloridas com concentração por bairro

**Linha 2 - Análise Espacial**
4. **Distribuição por Distância** - Histograma mostrando distâncias ao centro
5. **Densidade por Raio** - Gráfico de área com zonas urbana/periurbana/rural
6. **Boxplot por Zona** - Distribuição estatística de distâncias

**Linha 3 - Acessibilidade e Cobertura**
7. **Mapa de Dispersão** - Scatter plot latitude vs longitude com cores por distância
8. **Cobertura Acumulada** - Linha mostrando % de população atendida por raio
9. **Estatísticas Resumidas** - Tabela com principais indicadores numéricos

#### 🎨 Recursos Visuais:

- **Cores ColorBrewer** em todos os gráficos
- **Legendas claras** e acessíveis
- **Títulos descritivos** em português
- **Grid lines** para facilitar leitura
- **Anotações automáticas** em pontos relevantes

---

### 3. **Relatório Técnico em Markdown**

Documento gerado automaticamente contendo:

#### 📝 Seções do Relatório:

**1. Resumo Executivo**
- Total de estabelecimentos analisados
- Proporção público/privado
- Distância média ao centro
- Taxa de cobertura geográfica

**2. Metodologia Técnica**
- Fonte dos dados (CNES/DataSUS)
- Critérios de classificação
- Fórmula de cálculo de distância (Haversine)
- Sistema de coordenadas (WGS84 EPSG:4326)

**3. Análise Estatística Descritiva**
- Medidas de centralidade (média, mediana)
- Dispersão (desvio padrão, quartis)
- Distribuição por zona geográfica
- Top estabelecimentos por categoria

**4. Análise de Distribuição Espacial**
- Cobertura por raio (5km, 10km, 20km)
- Identificação de vazios assistenciais
- Concentração por bairro
- Acessibilidade geográfica

**5. Visualizações e Mapas**
- Links para mapas HTML interativos
- Referências aos gráficos do dashboard
- QR codes para acesso mobile (opcional)

**6. Conclusões e Recomendações**
- Pontos fortes da rede
- Áreas que necessitam expansão
- Sugestões para planejamento territorial
- Próximos passos para análise

**7. Referências Técnicas**
- Bibliotecas Python utilizadas
- Artigos científicos sobre ColorBrewer
- Normas cartográficas aplicadas
- Dados complementares (IBGE, OpenStreetMap)

---

## 🚀 Como Usar o Dashboard

### Passo 1: Executar o Script

```powershell
# Ativar ambiente virtual (se disponível)
.\geoprocessamento\Scripts\Activate.ps1

# Executar dashboard avançado
python 02_SCRIPTS\dashboard_avancado_colorbrewer.py
```

**Tempo estimado:** 2-5 minutos (dependendo do hardware)

---

### Passo 2: Explorar o Mapa Interativo

#### 🖱️ Controles do Mapa:

**Navegação**
- **Zoom:** Roda do mouse ou botões +/- no canto superior esquerdo
- **Pan:** Clicar e arrastar o mapa
- **Limite de zoom:** 10 (mínimo) a 18 (máximo) para evitar confusão

**TreeLayerControl (📂 ícone no canto superior direito)**
- **Clicar na pasta** → Expande/colapsa grupo
- **Checkbox individual** → Liga/desliga camada específica
- **Checkbox do grupo** → Liga/desliga todas as camadas do grupo
- **Radio button** → Escolhe apenas uma camada de base (OpenStreetMap, etc.)

**Interação com Estabelecimentos**
- **Passar mouse** → Tooltip rápido com nome
- **Clicar no marcador** → Popup completo com:
  - Nome completo
  - Tipo de estabelecimento
  - Endereço e bairro
  - Distância ao centro
  - Zona (urbana/periurbana/rural)
  - Classificação público/privado

**Clusters (agrupamentos numerados)**
- **Clicar no cluster** → Zoom automático e expansão
- **Números** → Quantidade de estabelecimentos agrupados
- **Cores do cluster** → Variam por densidade (verde ➜ amarelo ➜ vermelho)

**Mapa de Calor**
- **Intensidade de cor** → Concentração espacial
- **Cores quentes (vermelho)** → Alta densidade
- **Cores frias (azul/verde)** → Baixa densidade
- **Transparência** → Permite ver marcadores embaixo

---

### Passo 3: Analisar o Dashboard Visual

#### 📊 Interpretação dos Gráficos:

**Distribuição por Tipo (gráfico 1)**
- **Barras mais longas** → Tipos de estabelecimento mais comuns
- **Cores ColorBrewer** → Cada tipo tem cor única e distinguível
- **Ordem decrescente** → Facilita identificar top categorias

**Público vs Privado (gráfico 2)**
- **Vermelho** → Estabelecimentos públicos (ESF, PS, UBS)
- **Cinza** → Privados e outros
- **Porcentagens** → Proporção exata na legenda
- **Interpretação:** > 50% público indica forte presença SUS

**Top 10 Bairros (gráfico 3)**
- **Eixo horizontal** → Quantidade de estabelecimentos
- **Cores variadas** → Paleta qualitativa ColorBrewer
- **Centro concentrado?** → Bairros centrais devem liderar
- **Vazios assistenciais** → Bairros ausentes da lista

**Distribuição por Distância (gráfico 4)**
- **Histograma** → Frequência de estabelecimentos por faixa de distância
- **Pico à esquerda** → Concentração urbana (desejável)
- **Cauda longa** → Estabelecimentos rurais distantes
- **Bins (caixas)** → Intervalos de 1km

**Densidade por Raio (gráfico 5)**
- **Áreas empilhadas** → Acúmulo de estabelecimentos por raio
- **Verde** → Zona urbana (< 5km)
- **Amarelo** → Zona periurbana (5-10km)
- **Vermelho** → Zona rural (> 10km)
- **Inclinação** → Rapidez de expansão da cobertura

**Boxplot por Zona (gráfico 6)**
- **Caixa** → 50% central dos dados (Q1 a Q3)
- **Linha central** → Mediana
- **Whiskers (bigodes)** → Extensão dos dados (até 1.5*IQR)
- **Pontos isolados** → Outliers (estabelecimentos muito distantes)

**Mapa de Dispersão (gráfico 7)**
- **Eixo X** → Longitude (Oeste ← → Leste)
- **Eixo Y** → Latitude (Sul ← → Norte)
- **Cores** → Gradiente ColorBrewer por distância ao centro
- **Concentração central** → Cluster no centro urbano esperado

**Cobertura Acumulada (gráfico 8)**
- **Linha ascendente** → % de estabelecimentos cobertos por raio
- **Vertical empinada** → Rápida cobertura inicial (bom!)
- **Platô** → Raio máximo necessário para 100%
- **Benchmark:** 80% em 10km é meta aceitável

**Estatísticas Resumidas (gráfico 9)**
- **Tabela textual** → Números chave do projeto
- **Total de estabelecimentos** → Base completa analisada
- **Distâncias (média, mediana, máx)** → Medidas de dispersão
- **Cobertura por zona** → Distribuição percentual
- **Principais tipos** → Top 3 categorias

---

### Passo 4: Consultar o Relatório Técnico

Abra o arquivo `03_RESULTADOS/relatorio_analise_avancada_colorbrewer.md`:

#### 📖 Como Ler o Relatório:

**Para gestores públicos:**
- Foque no **Resumo Executivo** (primeira seção)
- Leia as **Recomendações** (última seção)
- Use os números para embasar decisões orçamentárias

**Para técnicos de saúde:**
- Consulte **Análise de Distribuição Espacial** 
- Identifique **vazios assistenciais** por bairro
- Planeje **novas unidades** baseado em dados

**Para pesquisadores:**
- Revise toda a **Metodologia Técnica**
- Valide critérios de classificação
- Reproduza análise com ajustes específicos

**Para desenvolvedores:**
- Consulte **Recursos Técnicos Utilizados**
- Veja dependências (pandas, folium, matplotlib)
- Adapte scripts para outras cidades

---

## 🎨 Entendendo ColorBrewer em Detalhes

### Tipos de Paletas

#### 1️⃣ **Sequencial** (para dados ordenados)

**Quando usar:**
- Distância ao centro (0km → 30km)
- Densidade populacional (baixa → alta)
- Tempo de deslocamento (rápido → lento)

**Paletas disponíveis no dashboard:**
- `BuGn` (azul-verde) → Distâncias
- `YlOrRd` (amarelo-laranja-vermelho) → Intensidade
- `Blues` (azuis graduados) → Dados demográficos

**Exemplo visual:**
```
🟦 Muito próximo → 🟩 Próximo → 🟩 Médio → 🟩 Longe → 🟢 Muito longe
```

---

#### 2️⃣ **Qualitativo** (para dados categóricos)

**Quando usar:**
- Tipos de estabelecimento (ESF, PS, Clínica...)
- Bairros (Centro, Petrópolis, Salete...)
- Natureza jurídica (Público, Privado, Filantrópico)

**Paletas disponíveis no dashboard:**
- `Set1` (8 cores distintas) → Até 8 categorias
- `Dark2` (cores escuras) → Impressão monocromática
- `Accent` (cores vibrantes) → Apresentações

**Exemplo visual:**
```
🔴 Tipo A | 🔵 Tipo B | 🟢 Tipo C | 🟣 Tipo D | 🟠 Tipo E | 🟡 Tipo F
```

---

#### 3️⃣ **Divergente** (para dados com ponto central)

**Quando usar:**
- Desvio da média (abaixo ↔ média ↔ acima)
- Avaliação de qualidade (ruim ↔ neutro ↔ ótimo)
- Variação temporal (diminuiu ↔ manteve ↔ aumentou)

**Paletas disponíveis no dashboard:**
- `RdYlGn` (vermelho-amarelo-verde) → Avaliação
- `BrBG` (marrom-bege-verde-água) → Tendências
- `PuOr` (roxo-laranja) → Polaridade

**Exemplo visual:**
```
🔴 Ruim → 🟠 Médio-ruim → 🟡 Neutro → 🟢 Médio-bom → 🟢 Excelente
```

---

### Critérios de Escolha de Cores

O dashboard aplica estas regras automaticamente:

✅ **Regra 1:** Público = Vermelho (atenção/SUS), Privado = Cinza (neutro)  
✅ **Regra 2:** Distâncias próximas = Verde (acessível), longas = Vermelho (inacessível)  
✅ **Regra 3:** Limites municipais = Azul (informação neutra institucional)  
✅ **Regra 4:** Marcas de referência = Preto (máximo contraste)  
✅ **Regra 5:** Heatmaps = Gradiente contínuo verde-amarelo-vermelho  

---

## 📁 Arquivos Gerados

Após executar o dashboard, estes arquivos são criados:

### Localização: `03_RESULTADOS/`

| Arquivo | Tipo | Tamanho | Descrição |
|---------|------|---------|-----------|
| `mapa_avancado_colorbrewer.html` | HTML | ~2-5 MB | Mapa interativo completo |
| `mapa_avancado_treelayer_colorbrewer.html` | HTML | ~2-5 MB | Versão com controle hierárquico |
| `dashboard_completo_colorbrewer.png` | Imagem | ~500 KB | Dashboard visual (alta resolução) |
| `dashboard_completo_colorbrewer.pdf` | PDF | ~400 KB | Dashboard vetorial (impressão) |
| `relatorio_analise_avancada_colorbrewer.md` | Markdown | ~50 KB | Relatório técnico completo |
| `dados_processados_colorbrewer.csv` | CSV | ~100 KB | Dados tabulares processados |

### Cópia para Publicação: `docs/`

Arquivos HTML são automaticamente copiados para `docs/` para publicação via GitHub Pages.

---

## 🔧 Personalização e Ajustes

### Modificar Paletas de Cores

Edite o arquivo `dashboard_avancado_colorbrewer.py` nas linhas 55-68:

```python
# Exemplo: Trocar BuGn por PuBu (roxo-azul)
COLORBREWER_SEQUENTIAL = {
    'PuBu_5': ['#f1eef6', '#d0d1e6', '#a6bddb', '#74a9cf', '#0570b0'],
    # ... outras paletas
}
```

**Onde encontrar mais paletas:**
- Site oficial: https://colorbrewer2.org/
- Documentação Folium: https://python-visualization.github.io/folium/

---

### Ajustar Raios de Análise

Modifique a função `criar_mapa_avancado_treelayer()` por volta da linha 800:

```python
# Raios atuais: 5km (urbano), 10km (periurbano), 20km (rural)
# Para expandir área rural:
folium.Circle(
    location=CENTRO_CONCORDIA,
    radius=30000,  # 30km ao invés de 20km
    color='#8b0000',
    # ...
).add_to(mapa)
```

---

### Adicionar Novas Categorias

Para incluir novos tipos de estabelecimento, edite `carregar_dados()` linha ~200:

```python
# Exemplo: Adicionar "Farmácias" como categoria pública
def eh_publico_estendido(nome, tipo):
    criterios_originais = [...]
    criterios_novos = [
        'FARMACIA POPULAR' in str(nome).upper(),
        str(tipo) == '99'  # Código hipotético
    ]
    return any(criterios_originais + criterios_novos)
```

---

### Alterar Centro de Referência

Se a análise for para outra cidade, mude as coordenadas (linha ~50):

```python
# Coordenadas atuais: Praça Central de Concórdia
CENTRO_CONCORDIA = [-27.2335, -52.0238]

# Exemplo para Florianópolis:
# CENTRO_FLORIANOPOLIS = [-27.5954, -48.5480]
```

---

## ❓ Perguntas Frequentes (FAQ)

### 1. **O mapa não carrega completamente**

**Possíveis causas:**
- Arquivo HTML muito grande (> 10 MB)
- Navegador desatualizado
- Bloqueador de pop-ups ativo

**Soluções:**
✅ Use Chrome ou Firefox atualizado  
✅ Desative extensões de bloqueio temporariamente  
✅ Aguarde 10-30 segundos para renderização completa  

---

### 2. **Cores não aparecem corretamente**

**Possíveis causas:**
- Monitor com calibração incorreta
- Modo de alto contraste do Windows ativo
- Problemas com driver de vídeo

**Soluções:**
✅ Desative modo de alto contraste (Configurações Windows)  
✅ Teste em outro monitor/computador  
✅ Abra o PDF ao invés do PNG (renderização vetorial)  

---

### 3. **Dados aparecem duplicados no mapa**

**Possíveis causas:**
- Múltiplas camadas ligadas simultaneamente
- Clusters expandidos sobrepondo marcadores individuais

**Soluções:**
✅ Use TreeLayerControl para desligar camadas desnecessárias  
✅ Dê zoom out para colapsar clusters automaticamente  
✅ Recarregue a página (F5)  

---

### 4. **Erro ao executar o script Python**

**Possíveis causas:**
- Bibliotecas não instaladas
- Arquivo de dados ausente
- Caminho incorreto

**Soluções:**
```powershell
# Instalar dependências
pip install pandas numpy folium matplotlib seaborn geopandas

# Verificar caminhos
python -c "import os; print(os.getcwd())"

# Executar com logs
python 02_SCRIPTS\dashboard_avancado_colorbrewer.py 2>&1 | Tee-Object -FilePath log.txt
```

---

### 5. **Como exportar mapa para PowerPoint?**

**Opção 1: Screenshot**
1. Abra o mapa HTML no navegador
2. Ajuste zoom para visualização desejada
3. Windows + Shift + S (Ferramenta de Captura)
4. Cole no PowerPoint (Ctrl + V)

**Opção 2: PDF**
1. No navegador, Ctrl + P (Imprimir)
2. Escolha "Salvar como PDF"
3. Insira PDF no PowerPoint como objeto

**Opção 3: Conversão HTML→Imagem**
```powershell
# Requer Node.js e html2canvas
npm install -g pageres-cli
pageres mapa_avancado_colorbrewer.html 1920x1080 --filename=mapa
```

---

### 6. **Dashboard lento no computador**

**Otimizações:**
✅ Reduza quantidade de estabelecimentos (filtre por tipo)  
✅ Desative heatmap (linha ~850 do script)  
✅ Diminua complexidade dos polígonos municipais (simplify mais agressivo)  
✅ Use versão sem TreeLayerControl (dashboard_colorbrewer_simplificado.py)  

---

## 🎓 Conceitos Técnicos Detalhados

### Fórmula de Haversine

Calcula distância entre dois pontos na superfície esférica da Terra:

```python
def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula distância geodésica entre dois pontos em km
    
    Parâmetros:
        lat1, lon1: Coordenadas do ponto 1 (decimal)
        lat2, lon2: Coordenadas do ponto 2 (decimal)
    
    Retorna:
        Distância em quilômetros (float)
    """
    R = 6371  # Raio médio da Terra em km
    
    # Converter graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Diferenças
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c
```

**Precisão:**
- Erro < 0.5% para distâncias até 100km
- Ignora elevação (adequado para Concórdia - relevo suave)
- Alternativa para alta precisão: Vincenty (mais lenta)

---

### TreeLayerControl vs LayerControl

**LayerControl (tradicional):**
- Lista plana de camadas
- Um nível de hierarquia
- Sem agrupamento lógico

**TreeLayerControl (usado neste dashboard):**
- Estrutura em árvore
- Múltiplos níveis de hierarquia
- Agrupamento semântico
- Expansão/colapso de grupos
- Mais intuitivo para muitas camadas

**Implementação:**
```python
from folium import plugins

# Criar grupos
grupo_estabelecimentos = plugins.FeatureGroupSubGroup(overlay, "Estabelecimentos")
subgrupo_publicos = plugins.FeatureGroupSubGroup(grupo_estabelecimentos, "Públicos")

# Adicionar ao mapa
overlay.add_to(mapa)
grupo_estabelecimentos.add_to(overlay)
subgrupo_publicos.add_to(grupo_estabelecimentos)

# Controle
plugins.TreeLayerControl(base_tree={...}, overlay_tree={...}).add_to(mapa)
```

---

### MarkerCluster Dinâmico

Agrupa marcadores próximos conforme nível de zoom:

**Parâmetros importantes:**
```python
MarkerCluster(
    name='Clusters',
    overlay=True,
    control=True,
    icon_create_function='''
        function(cluster) {
            var count = cluster.getChildCount();
            var c = ' marker-cluster-';
            if (count < 10) {
                c += 'small';  // Verde
            } else if (count < 30) {
                c += 'medium'; // Amarelo
            } else {
                c += 'large';  // Vermelho
            }
            return L.divIcon({
                html: '<div><span>' + count + '</span></div>',
                className: 'marker-cluster' + c,
                iconSize: new L.Point(40, 40)
            });
        }
    '''
)
```

**Vantagens:**
✅ Performance em navegadores (menos elementos DOM)  
✅ Visão clara de concentrações  
✅ Navegação intuitiva (clicar expande)  

**Desvantagens:**
❌ Pode ocultar outliers isolados  
❌ Dificulta comparação exata de quantidades  

---

### HeatMap (Mapa de Calor)

Visualiza densidade espacial usando gradiente de cores:

**Parâmetros do dashboard:**
```python
HeatMap(
    data=[[lat, lon, 1] for lat, lon in coordenadas],
    name='Densidade',
    min_opacity=0.3,
    max_zoom=13,
    max_val=1.0,
    radius=15,        # Raio de influência em pixels
    blur=10,          # Suavização
    gradient={        # Gradiente ColorBrewer
        '0.0': 'blue',
        '0.5': 'lime',
        '0.7': 'yellow',
        '1.0': 'red'
    }
).add_to(mapa)
```

**Interpretação:**
- **Azul/Verde** → 1-5 estabelecimentos na área
- **Amarelo** → 6-10 estabelecimentos
- **Laranja/Vermelho** → > 10 estabelecimentos (alta densidade)

---

## 📚 Referências e Leituras Adicionais

### Artigos Científicos

1. **Brewer, C. A., Hatchard, G. W., & Harrower, M. A. (2003).** 
   *ColorBrewer in Print: A Catalog of Color Schemes for Maps.*  
   Cartography and Geographic Information Science, 30(1), 5-32.  
   https://doi.org/10.1559/152304003100010929

2. **Harrower, M., & Brewer, C. A. (2003).**  
   *ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps.*  
   The Cartographic Journal, 40(1), 27-37.  
   https://doi.org/10.1179/000870403235002042

3. **Silva, A. P., & Barcellos, C. (2020).**  
   *Geoprocessamento aplicado à saúde pública no Brasil: revisão sistemática.*  
   Cadernos de Saúde Pública, 36(4), e00046719.

### Documentação Técnica

- **Folium Documentation:** https://python-visualization.github.io/folium/
- **ColorBrewer 2.0:** https://colorbrewer2.org/
- **GeoPandas User Guide:** https://geopandas.org/en/stable/
- **Matplotlib Colormaps:** https://matplotlib.org/stable/tutorials/colors/colormaps.html

### Tutoriais Recomendados

- **Python for Geographic Data Analysis (Tenkanen et al., 2023)**
- **Interactive Data Visualization with Folium (DataCamp)**
- **Spatial Analysis with Python (ESRI Training)**

---

## 👤 Suporte e Contato

### Reportar Problemas

**GitHub Issues:** [https://github.com/caetanoronan/analise-saude-concordia/issues](https://github.com/caetanoronan/analise-saude-concordia/issues)

**Informações necessárias:**
1. Descrição do erro
2. Mensagem de erro completa (se aplicável)
3. Sistema operacional e versão do Python
4. Saída de `pip list` (lista de pacotes instalados)

### Contribuir com o Projeto

Pull requests são bem-vindos! Áreas de interesse:

✅ Novos tipos de visualização  
✅ Otimizações de performance  
✅ Suporte a outras cidades/estados  
✅ Melhorias na documentação  
✅ Testes automatizados  

### Créditos

**Desenvolvido por:**  
Ronan Armando Caetano  
Graduando em Ciências Biológicas - UFSC  
Técnico em Geoprocessamento - IFSC  

**Orientação:**  
Universidade Federal de Santa Catarina (UFSC)

**Dados:**  
CNES/DataSUS - Ministério da Saúde  
IBGE - Instituto Brasileiro de Geografia e Estatística  
OpenStreetMap Contributors

**Tecnologias:**  
Python, Folium, Pandas, Matplotlib, ColorBrewer  

---

## 📜 Licença

Este projeto utiliza dados públicos do CNES/DataSUS e está licenciado sob **Creative Commons BY-SA 4.0**.

**Você é livre para:**
✅ Compartilhar - copiar e redistribuir  
✅ Adaptar - remixar, transformar e criar a partir do material  

**Sob as seguintes condições:**
📌 Atribuição - dar crédito apropriado  
📌 CompartilhaIgual - distribuir sob mesma licença  

---

**Última atualização:** Outubro 2025  
**Versão do Dashboard:** 2.0 (ColorBrewer Advanced)  
**Compatibilidade:** Python 3.8+, Folium 0.15+, Pandas 2.0+

---

