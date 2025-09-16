# 🏠 Scraper Zap Imóveis com Excel Automático

Este projeto foi atualizado para gerar automaticamente arquivos Excel formatados ao final do scraping, sem necessidade de interação do usuário.

## 📋 Funcionalidades

- ✅ **Scraping automático** do Zap Imóveis
- ✅ **Geração automática de Excel** formatado
- ✅ **6 abas de análise** detalhada dos dados
- ✅ **Formatação profissional** com cores e bordas
- ✅ **Estatísticas completas** dos imóveis coletados

## 🚀 Como Usar

### Opção 1: Execução Mais Simples
```bash
python executar_scraper.py
```
- Executa automaticamente com URL pré-configurada
- Processa 3 páginas por padrão
- Gera Excel automaticamente ao final

### Opção 2: Scraper Principal
```bash
python zap_scraper.py
```
- Permite inserir URL personalizada
- Permite escolher número de páginas
- Gera Excel automaticamente ao final

### Opção 3: Scraper Automático (Linha de Comando)
```bash
python scraper_automatico.py "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/" 5
```
- Execução via linha de comando
- Parâmetros: URL e número de páginas
- Gera Excel automaticamente ao final

### Opção 4: Menu Interativo
```bash
python exemplo_excel.py
```
- Menu com múltiplas opções
- Processar CSV existente
- Executar scraper completo
- Executar scraper automático

## 📊 Arquivos Gerados

Ao final da execução, são gerados automaticamente:

1. **📄 dados_final_YYYYMMDD-HHMMSS.csv** - Dados limpos em CSV
2. **📊 dados_zap_formatado_YYYYMMDD-HHMMSS.xlsx** - Excel formatado

## 📋 Abas do Excel

O arquivo Excel contém **6 abas** com análises detalhadas:

### 1. 📊 Dados Completos
- Todos os imóveis coletados
- Formatação profissional com cores alternadas
- Colunas: Descrição, Endereço, M², Quartos, Banheiros, Vagas, Preço, Condomínio, IPTU, R$/M²

### 2. 📈 Resumo Estatístico
- Métricas gerais dos dados
- Preços médios, mínimos e máximos
- Áreas médias e coeficientes de variação
- Estatísticas de quartos, banheiros e vagas

### 3. 💰 Análise de Preços
- Distribuição por faixas de preço
- Quantidade de imóveis por faixa
- Preços médios por faixa
- Área média por faixa de preço

### 4. 🏠 Análise de Áreas
- Distribuição por faixas de área
- Quantidade de imóveis por faixa
- Preços médios por faixa de área
- Análise de preço por m² por faixa

### 5. 🏆 Top Imóveis
- Top 10 melhores preços por m²
- Imóveis com melhor custo-benefício
- Ordenados por menor R$/M²

### 6. 🔍 Filtros Especiais
- Imóveis 3 quartos + 2 banheiros
- Imóveis com vaga de garagem
- Imóveis até R$ 200.000
- Imóveis 50-80m²

## 🎨 Formatação do Excel

- **Cabeçalhos coloridos** em azul
- **Títulos destacados** em azul escuro
- **Linhas alternadas** em cinza claro
- **Bordas** em todas as células
- **Formatação de moeda** para preços
- **Números formatados** para áreas
- **Colunas ajustadas** automaticamente

## 📦 Dependências

Certifique-se de ter instalado:
```bash
pip install -r requirements.txt
```

Principais dependências:
- pandas
- openpyxl (para Excel)
- selenium
- undetected-chromedriver
- beautifulsoup4

## 🔧 Configuração

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute um dos scripts:**
   ```bash
   python executar_scraper.py
   ```

3. **Aguarde a conclusão** - o Excel será gerado automaticamente!

## 📝 Exemplo de Uso

```python
from zap_scraper import ZapScraper

# Criar scraper
scraper = ZapScraper()

# Executar análise (gera Excel automaticamente)
df = scraper.analisar_site("https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/", 5)

# O Excel já foi gerado automaticamente!
```

## 🎯 Vantagens

- ✅ **Zero interação** - execução totalmente automática
- ✅ **Excel profissional** - formatação de alta qualidade
- ✅ **Análises completas** - 6 abas com diferentes visões
- ✅ **Fácil de usar** - apenas execute o script
- ✅ **Dados organizados** - CSV + Excel formatado

## 🚨 Notas Importantes

- O Chrome deve estar instalado no sistema
- Para parar o scraping, feche o navegador
- Os arquivos são salvos na pasta atual
- O Excel é gerado automaticamente ao final do processo

## 📞 Suporte

Em caso de problemas:
1. Verifique se o Chrome está instalado
2. Confirme se todas as dependências estão instaladas
3. Teste com uma URL válida do Zap Imóveis
4. Verifique se há espaço em disco suficiente
