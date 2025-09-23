# 🏠 Sistema de Laudo de Avaliação Imobiliária

## 📋 Descrição
Sistema completo para geração de laudos de avaliação imobiliária em formato DOCX, integrando:
- Scraping de dados do Zap Imóveis
- Formulário para coleta de dados específicos do imóvel
- Pesquisa de localidade via APIs Agno e Tavily
- Geração automática de laudo DOCX seguindo modelo padrão

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com suas chaves de API:
```
TAVILY_API_KEY=sua_chave_tavily_aqui
```

### 3. Executar Sistema Principal
```bash
streamlit run app_laudo_completo.py
```

### 4. Executar Componentes Individuais (Opcional)

#### Testar Formulário
```bash
streamlit run laudo_formulario.py
```

#### Testar Pesquisa de Localidade
```bash
python pesquisa_localidade.py
```

#### Testar Gerador DOCX
```bash
python gerador_laudo_docx.py
```

## 📁 Estrutura do Sistema

### Arquivos Principais
- `app_laudo_completo.py` - Aplicação principal integrada
- `laudo_formulario.py` - Formulário para coleta de dados
- `pesquisa_localidade.py` - Integração com APIs Agno/Tavily
- `gerador_laudo_docx.py` - Gerador de documento DOCX
- `zap_scraper.py` - Scraper do Zap Imóveis (existente)

### Arquivos de Suporte
- `requirements.txt` - Dependências do projeto
- `INSTRUCOES_LAUDO.md` - Este arquivo de instruções

## 🔄 Fluxo do Sistema

1. **Coleta de Dados**: Usuário insere URL do Zap Imóveis
2. **Scraping**: Sistema coleta dados de imóveis similares
3. **Formulário**: Usuário preenche dados específicos do imóvel e avaliador
4. **Pesquisa Localidade**: Sistema gera informações da região (instantâneo)
5. **Geração de Arquivos**: Sistema gera laudo DOCX, PDF e Excel formatado
6. **Download**: Usuário baixa todos os arquivos gerados

## 📊 Dados Coletados pelo Scraper

- Descrição do imóvel
- Endereço
- Área (m²)
- Preço
- Preço por m²
- Quartos, banheiros, vagas
- Taxas (condomínio, IPTU)

## 📋 Dados do Formulário

### Dados do Imóvel
- Número da matrícula
- Cartório de registro
- Área do terreno
- Área construída
- Loteamento/bairro
- Cidade/estado
- Tipo de construção
- Descrição detalhada do imóvel

### Dados do Avaliador
- Nome completo
- CRECI
- CNAI
- Telefone
- E-mail
- Website
- Data do laudo
- Cidade/estado da assinatura

## 📄 Estrutura do Laudo DOCX

1. **Título**: LAUDO DE AVALIAÇÃO IMOBILIÁRIA
2. **Objetivo**: Texto padrão conforme ABNT
3. **Identificação**: Dados específicos do imóvel
4. **Metodologia**: Texto padrão sobre método comparativo
5. **Pesquisa de Mercado**: Tabela com dados do scraper
6. **Determinação do Valor**: Cálculos baseados nos dados
7. **Pesquisa de Localidade**: Informações via APIs
8. **Conclusão**: Valor final estimado
9. **Assinatura**: Dados do avaliador

## 🛠️ Funcionalidades

### Scraping Inteligente
- Detecção automática de duplicatas
- Remoção de outliers
- Análise estatística dos dados
- Geração de Excel formatado

### Formulário Inteligente
- Validação automática de campos obrigatórios
- Interface intuitiva com abas organizadas
- Preview dos dados coletados

### Pesquisa de Localidade
- **Super Rápida**: Geração instantânea de informações (0.00 segundos)
- Informações pré-definidas para cidades conhecidas
- Texto personalizado por cidade e bairro
- Formato estruturado seguindo modelo padrão
- Cache inteligente para evitar reprocessamento
- Opção de pular pesquisa para máxima velocidade

### Geração de Arquivos
- **Laudo DOCX**: Template profissional seguindo modelo padrão
- **Laudo PDF**: Versão em PDF com formatação elegante e cores
- **Excel Formatado**: Análise completa com 6 abas de dados
- Cálculos automáticos de valores
- Formatação adequada para documentos oficiais
- Conversão de valores para extenso
- Botões de download para todos os formatos (DOCX, PDF, Excel)

## ⚠️ Observações Importantes

1. **Chaves de API**: Configure as chaves das APIs Agno e Tavily no arquivo `.env`
2. **Chrome**: O sistema requer Google Chrome instalado para o scraping
3. **Internet**: Necessária conexão com internet para scraping e APIs
4. **Dados**: Os dados coletados são salvos na pasta `arquivos/`
5. **Backup**: Sempre faça backup dos dados importantes

## 🔧 Solução de Problemas

### Erro de Chrome
- Verifique se o Google Chrome está instalado
- Atualize o Chrome para a versão mais recente

### Erro de API
- Verifique se as chaves de API estão corretas no `.env`
- Confirme se há créditos disponíveis nas APIs

### Erro de Dependências
- Execute `pip install -r requirements.txt`
- Verifique se todas as dependências foram instaladas

### Erro de Permissões
- Verifique se tem permissão para escrever na pasta `arquivos/`
- Execute como administrador se necessário

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

## 📝 Licença

Este sistema foi desenvolvido para uso interno e deve seguir as políticas de uso da empresa.
