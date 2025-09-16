# 🏠 Zap Imóveis Scraper - Streamlit com Excel

Interface web moderna e intuitiva para extrair dados de imóveis do Zap Imóveis com **geração automática de Excel formatado**.

## 🆕 Novidades - Excel Integrado

✅ **Excel Automático**: Gera arquivo Excel formatado automaticamente  
✅ **6 Abas de Análise**: Dados completos, estatísticas, análises por faixas  
✅ **Formatação Profissional**: Cores, bordas, formatação de moeda  
✅ **Download Direto**: Baixe CSV e Excel diretamente da interface  

## 🚀 Como Usar

### 1. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Streamlit
```bash
streamlit run app.py
```

### 3. Usar a Interface

1. **🔗 Cole a URL** do Zap Imóveis na caixa de texto
2. **⚙️ Configure** as opções na sidebar:
   - Número de páginas (1-20)
   - Timeout (10-60 segundos)
   - Remover outliers ✅
   - Gerar gráficos ✅
   - **Gerar Excel formatado** ✅ ← **NOVA OPÇÃO**
3. **🚀 Clique** em "Iniciar Scraping"
4. **⏳ Aguarde** o processamento automático
5. **📥 Baixe** os arquivos CSV e Excel gerados

## 📊 Funcionalidades do Excel

### 🎨 Formatação Profissional
- **Cabeçalhos coloridos** em azul
- **Títulos destacados** em azul escuro
- **Linhas alternadas** em cinza claro
- **Bordas** em todas as células
- **Formatação de moeda** para preços
- **Números formatados** para áreas
- **Colunas ajustadas** automaticamente

### 📋 6 Abas de Análise

#### 1. 📊 Dados Completos
- Todos os imóveis coletados
- Formatação profissional
- Colunas: Descrição, Endereço, M², Quartos, Banheiros, Vagas, Preço, Condomínio, IPTU, R$/M²

#### 2. 📈 Resumo Estatístico
- Total de imóveis
- Preço médio, mínimo e máximo
- Área média, mínima e máxima
- Preço por m² médio, mínimo e máximo
- Mediana e desvio padrão
- Coeficiente de variação
- Quartos, banheiros e vagas médios

#### 3. 💰 Análise de Preços
- Distribuição por faixas de preço:
  - Até R$ 100k
  - R$ 100k-200k
  - R$ 200k-300k
  - R$ 300k-400k
  - R$ 400k-500k
  - Acima de R$ 500k
- Quantidade, preços médios e área média por faixa

#### 4. 🏠 Análise de Áreas
- Distribuição por faixas de área:
  - Até 40m²
  - 40-60m²
  - 60-80m²
  - 80-100m²
  - 100-120m²
  - Acima de 120m²
- Quantidade, área média e preços por faixa

#### 5. 🏆 Top Imóveis
- Top 10 melhores preços por m²
- Imóveis com melhor custo-benefício
- Ordenados por menor R$/M²

#### 6. 🔍 Filtros Especiais
- **Imóveis 3 Quartos + 2 Banheiros**
- **Imóveis com Vaga de Garagem**
- **Imóveis até R$ 200.000**
- **Imóveis 50-80m²**

## 🎯 Interface Streamlit

### 📱 Design Responsivo
- Interface moderna e intuitiva
- Layout centralizado e organizado
- Cores e gradientes profissionais
- Botões e componentes estilizados

### ⚙️ Configurações na Sidebar
- **Número máximo de páginas**: 1-20 (padrão: 5)
- **Timeout**: 10-60 segundos (padrão: 30)
- **Remover outliers**: ✅ (padrão: ativado)
- **Gerar gráficos**: ✅ (padrão: ativado)
- **Gerar Excel formatado**: ✅ (padrão: ativado) ← **NOVO**

### 📊 Visualizações
- **Métricas principais**: Total, preço médio, área média, coeficiente de variação
- **Tabela interativa**: Com filtros por localidade, quartos e faixa de preço
- **Gráficos Plotly**:
  - Histograma de preços por m²
  - Boxplot de preços por m²
  - Scatter plot: Área vs Preço

### 💾 Download de Arquivos
- **📄 CSV**: Dados brutos em formato CSV
- **📊 Excel**: Arquivo formatado com 6 abas de análise
- **MIME types corretos** para download automático
- **Botões separados** para cada tipo de arquivo

## 🔧 Configuração Técnica

### Dependências Principais
```python
streamlit>=1.28.0
pandas>=1.5.0
openpyxl>=3.1.0  # Para Excel
plotly>=5.15.0   # Para gráficos
```

### Estrutura de Arquivos
```
├── app.py                    # Interface Streamlit principal
├── zap_scraper.py           # Scraper principal
├── excel_formatter.py       # Formatador de Excel
├── requirements.txt          # Dependências
└── README_STREAMLIT_EXCEL.md # Esta documentação
```

## 🎨 Exemplo de Uso

```python
# No app.py do Streamlit:

from excel_formatter import ExcelFormatter

def executar_scraping(url, max_paginas, gerar_excel=True):
    # ... scraping dos dados ...
    
    if gerar_excel:
        excel_formatter = ExcelFormatter()
        excel_file = excel_formatter.gerar_excel_formatado(df)
        
        # Botão de download
        with open(excel_file, 'rb') as f:
            st.download_button(
                label="📥 Baixar Excel Formatado",
                data=f.read(),
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
```

## 🚨 Notas Importantes

- **Chrome obrigatório**: O Chrome deve estar instalado no sistema
- **Excel automático**: Ativado por padrão na interface
- **Arquivos temporários**: Salvos na pasta atual do projeto
- **Timeout configurável**: Ajustável na sidebar (10-60 segundos)
- **Outliers**: Removidos automaticamente por padrão

## 🎉 Vantagens

✅ **Interface moderna** e intuitiva  
✅ **Excel profissional** com 6 abas de análise  
✅ **Download direto** da interface web  
✅ **Configurações flexíveis** na sidebar  
✅ **Visualizações interativas** com Plotly  
✅ **Processamento automático** sem intervenção manual  
✅ **Formatação profissional** do Excel  
✅ **Filtros especiais** para diferentes tipos de imóveis  

## 📞 Suporte

Em caso de problemas:
1. Verifique se o Chrome está instalado
2. Confirme se todas as dependências estão instaladas
3. Teste com uma URL válida do Zap Imóveis
4. Verifique se há espaço em disco suficiente
5. Ative a opção "Gerar Excel formatado" na sidebar
