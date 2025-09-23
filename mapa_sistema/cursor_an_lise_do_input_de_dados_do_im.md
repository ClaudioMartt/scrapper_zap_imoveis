

## 🗺️ **Mapa da Aplicação - Sistema de Laudo Imobiliário**

### �� **Visão Geral do Fluxo:**
```
�� FORMULÁRIO → 🔍 TAVILY → �� IA → �� LAUDO
```

### �� **Fluxo Completo da Aplicação:**

#### **1. ENTRADA DE DADOS**
```
📱 app_laudo_completo.py
├── laudo_formulario.py (Coleta dados do imóvel)
│   ├── Número da Matrícula
│   ├── Cartório
│   ├── Área do Terreno
│   ├── Área Construída
│   ├── 🏘️ LOTEAMENTO/BAIRRO ← PARÂMETRO CHAVE
│   ├── Cidade
│   ├── Estado
│   └── Tipo de Construção
```

#### **2. PESQUISA DE LOCALIDADE (TAVILY)**
```
🔍 pesquisa_localidade_ia_final.py
├── PesquisaLocalidadeIAFinal.gerar_texto_pesquisa_localidade()
│   ├── 📍 Recebe: cidade + bairro (do formulário)
│   ├── 🔍 TAVILY API (Linha 47-52)
│   │   └── query = f"Informações sobre {bairro} em {cidade} São Paulo..."
│   │   └── response = self.agent.run(query) ← CHAMADA TAVILY
│   └── 📊 Retorna: dados brutos da internet
```

#### **3. TRATAMENTO PELA IA**
```
�� pesquisa_localidade_ia_final.py
├── _tratar_com_ia_final() (Linha 67-97)
│   ├── 📥 Recebe: dados brutos do Tavily
│   ├── 🧠 IA OPENAI (Linha 86)
│   │   └── prompt_tratamento = "Organize as informações brutas..."
│   │   └── resposta_tratada = self.agent.run(prompt_tratamento) ← CHAMADA IA
│   ├── 🧹 _extrair_texto_limpo() (Linha 99-124)
│   └── �� Retorna: texto organizado e profissional
```

### 🔍 **Detalhamento das Chamadas:**

#### **CHAMADA TAVILY (Pesquisa na Internet)**
```python
# Arquivo: pesquisa_localidade_ia_final.py
# Linha: 47-52

query = f"""Informações sobre {bairro} em {cidade} São Paulo: 
comércio, serviços, lazer, segurança e potencial econômico. 
Foque especificamente no bairro {bairro}."""

response = self.agent.run(query)  # ← CHAMADA TAVILY
```

**O que faz:**
- �� Busca informações REAIS na internet
- 📍 Usa o bairro informado no formulário
- ⏱️ Tempo: ~20 segundos
- 📊 Retorna: dados brutos com informações desatualizadas

#### **CHAMADA IA (Tratamento e Organização)**
```python
# Arquivo: pesquisa_localidade_ia_final.py
# Linha: 67-97

prompt_tratamento = f"""
Organize as informações brutas abaixo sobre o bairro {bairro} em {cidade} 
em um texto conciso e profissional para um laudo imobiliário.

DADOS BRUTOS:
{dados_brutos}

INSTRUÇÕES:
1. Organize em 3 seções: "Comércio, Lazer e Comodidade", "Segurança", 
   "Potencial Econômico e de Crescimento Imobiliário"
2. Máximo 5 linhas por seção
3. Linguagem concisa e profissional
4. Remova informações desnecessárias, repetições e caracteres especiais
5. Foque apenas em informações relevantes para avaliação imobiliária
6. Use linguagem clara e objetiva
"""

resposta_tratada = self.agent.run(prompt_tratamento)  # ← CHAMADA IA
```

**O que faz:**
- 🤖 Organiza dados brutos em texto profissional
- 📝 Limita a máximo 5 linhas por tópico
- �� Remove informações desnecessárias
- ⏱️ Tempo: ~10 segundos
- 📤 Retorna: texto limpo e estruturado

### 📊 **Fluxo de Dados Detalhado:**

```
┌─────────────────────────────────────────────────────────────┐
│                    📱 ENTRADA                               │
├─────────────────────────────────────────────────────────────┤
│ 1. Usuário preenche formulário                              │
│ 2. Sistema captura: cidade + bairro                        │
│ 3. Exemplo: "Taquarituba" + "Jardim Santa Virgínia"       │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                  🔍 TAVILY API                              │
├─────────────────────────────────────────────────────────────┤
│ 1. Query: "Informações sobre Jardim Santa Virgínia em      │
│    Taquarituba São Paulo: comércio, serviços..."           │
│ 2. Busca REAL na internet                                  │
│ 3. Retorna dados brutos com caracteres de escape           │
│ 4. Exemplo: "RunResponse content...Destacam-se..."         │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                    🤖 IA OPENAI                             │
├─────────────────────────────────────────────────────────────┤
│ 1. Recebe dados brutos                                     │
│ 2. Aplica prompt de organização                            │
│ 3. Estrutura em 3 seções                                   │
│ 4. Limita a 5 linhas por seção                            │
│ 5. Remove caracteres especiais                             │
│ 6. Retorna texto profissional                              │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                   📄 RESULTADO FINAL                       │
├─────────────────────────────────────────────────────────────┤
│ Comércio, Lazer e Comodidade:                              │
│ [Texto limpo e profissional sobre comércio]                │
│                                                             │
│ Segurança:                                                  │
│ [Texto limpo e profissional sobre segurança]               │
│                                                             │
│ Potencial Econômico e de Crescimento Imobiliário:         │
│ [Texto limpo e profissional sobre potencial]               │
└─────────────────────────────────────────────────────────────┘
```

### 🏗️ **Arquitetura da Aplicação:**

#### **Arquivos Principais:**
```
📁 zapImoveis/
├── 📱 app_laudo_completo.py          ← APLICAÇÃO PRINCIPAL
├── 📋 laudo_formulario.py            ← FORMULÁRIO DE ENTRADA
├── 🔍 pesquisa_localidade_ia_final.py ← PESQUISA + IA
├── 📄 gerador_laudo_docx.py          ← GERAÇÃO DE LAUDOS
├── 📊 excel_formatter.py             ← FORMATAÇÃO EXCEL
└── 🔧 .env                           ← CONFIGURAÇÃO DE CHAVES
```

#### **Dependências Externas:**
```
🔑 CHAVES DE API (.env)
├── TAVILY_API_KEY=tvly-dev-...      ← PESQUISA NA INTERNET
├── OPENAI_API_KEY=sk-proj-...       ← TRATAMENTO DE TEXTO
└── GROQ_API_KEY=gsk_...             ← ALTERNATIVA (não usada)
```

### ⚡ **Pontos de Integração:**

#### **1. Captura do Bairro (Formulário → Pesquisa)**
```python
# app_laudo_completo.py linha 147
bairro = dados_imovel.get('loteamento', 'Jardim Santa Virgínia')

# pesquisa_localidade_ia_final.py linha 47
query = f"""Informações sobre {bairro} em {cidade} São Paulo..."""
```

#### **2. Tavily → IA (Dados Brutos → Texto Limpo)**
```python
# pesquisa_localidade_ia_final.py linha 47
response = self.agent.run(query)  # ← TAVILY

# pesquisa_localidade_ia_final.py linha 86
resposta_tratada = self.agent.run(prompt_tratamento)  # ← IA
```

#### **3. IA → Laudo (Texto → Documento)**
```python
# app_laudo_completo.py linha 172
texto_pesquisa = self.pesquisa_localidade.gerar_texto_pesquisa_localidade(cidade, bairro)

# app_laudo_completo.py linha 228
self.gerador_docx.gerar_laudo_completo(
    dados_imovel=dados_imovel,
    dados_avaliador=dados_avaliador,
    dados_scraper=dados_scraper,
    texto_pesquisa_localidade=texto_pesquisa  # ← TEXTO TRATADO PELA IA
)
```

### 🎯 **Resumo do Processo:**

1. **📱 ENTRADA**: Usuário informa bairro no formulário
2. **🔍 TAVILY**: Sistema pesquisa informações reais na internet
3. **🤖 IA**: Dados brutos são tratados e organizados pela IA
4. **📄 LAUDO**: Texto profissional é inserido no laudo final

### **⏱️ Tempo Total: ~30 segundos**
- Tavily: ~20 segundos
- IA: ~10 segundos

### **✅ Resultado:**
- ✅ Pesquisa real na internet
- ✅ Texto profissional e organizado
- ✅ Máximo 5 linhas por tópico
- ✅ Linguagem adequada para laudos

**O sistema agora funciona como um pipeline completo: Formulário → Tavily → IA → Laudo!** 🎉

```plaintext
�� FORMULÁRIO → 🔍 TAVILY → �� IA → �� LAUDO
```

```plaintext
📱 app_laudo_completo.py
├── laudo_formulario.py (Coleta dados do imóvel)
│   ├── Número da Matrícula
│   ├── Cartório
│   ├── Área do Terreno
│   ├── Área Construída
│   ├── 🏘️ LOTEAMENTO/BAIRRO ← PARÂMETRO CHAVE
│   ├── Cidade
│   ├── Estado
│   └── Tipo de Construção
```

```plaintext
🔍 pesquisa_localidade_ia_final.py
├── PesquisaLocalidadeIAFinal.gerar_texto_pesquisa_localidade()
│   ├── 📍 Recebe: cidade + bairro (do formulário)
│   ├── 🔍 TAVILY API (Linha 47-52)
│   │   └── query = f"Informações sobre {bairro} em {cidade} São Paulo..."
│   │   └── response = self.agent.run(query) ← CHAMADA TAVILY
│   └── 📊 Retorna: dados brutos da internet
```

```plaintext
�� pesquisa_localidade_ia_final.py
├── _tratar_com_ia_final() (Linha 67-97)
│   ├── 📥 Recebe: dados brutos do Tavily
│   ├── 🧠 IA OPENAI (Linha 86)
│   │   └── prompt_tratamento = "Organize as informações brutas..."
│   │   └── resposta_tratada = self.agent.run(prompt_tratamento) ← CHAMADA IA
│   ├── 🧹 _extrair_texto_limpo() (Linha 99-124)
│   └── �� Retorna: texto organizado e profissional
```

```python
# Arquivo: pesquisa_localidade_ia_final.py
# Linha: 47-52

query = f"""Informações sobre {bairro} em {cidade} São Paulo: 
comércio, serviços, lazer, segurança e potencial econômico. 
Foque especificamente no bairro {bairro}."""

response = self.agent.run(query)  # ← CHAMADA TAVILY
```

```python
# Arquivo: pesquisa_localidade_ia_final.py
# Linha: 67-97

prompt_tratamento = f"""
Organize as informações brutas abaixo sobre o bairro {bairro} em {cidade} 
em um texto conciso e profissional para um laudo imobiliário.

DADOS BRUTOS:
{dados_brutos}

INSTRUÇÕES:
1. Organize em 3 seções: "Comércio, Lazer e Comodidade", "Segurança", 
   "Potencial Econômico e de Crescimento Imobiliário"
2. Máximo 5 linhas por seção
3. Linguagem concisa e profissional
4. Remova informações desnecessárias, repetições e caracteres especiais
5. Foque apenas em informações relevantes para avaliação imobiliária
6. Use linguagem clara e objetiva
"""

resposta_tratada = self.agent.run(prompt_tratamento)  # ← CHAMADA IA
```

```plaintext
┌─────────────────────────────────────────────────────────────┐
│                    📱 ENTRADA                               │
├─────────────────────────────────────────────────────────────┤
│ 1. Usuário preenche formulário                              │
│ 2. Sistema captura: cidade + bairro                        │
│ 3. Exemplo: "Taquarituba" + "Jardim Santa Virgínia"       │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                  🔍 TAVILY API                              │
├─────────────────────────────────────────────────────────────┤
│ 1. Query: "Informações sobre Jardim Santa Virgínia em      │
│    Taquarituba São Paulo: comércio, serviços..."           │
│ 2. Busca REAL na internet                                  │
│ 3. Retorna dados brutos com caracteres de escape           │
│ 4. Exemplo: "RunResponse content...Destacam-se..."         │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                    🤖 IA OPENAI                             │
├─────────────────────────────────────────────────────────────┤
│ 1. Recebe dados brutos                                     │
│ 2. Aplica prompt de organização                            │
│ 3. Estrutura em 3 seções                                   │
│ 4. Limita a 5 linhas por seção                            │
│ 5. Remove caracteres especiais                             │
│ 6. Retorna texto profissional                              │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                   📄 RESULTADO FINAL                       │
├─────────────────────────────────────────────────────────────┤
│ Comércio, Lazer e Comodidade:                              │
│ [Texto limpo e profissional sobre comércio]                │
│                                                             │
│ Segurança:                                                  │
│ [Texto limpo e profissional sobre segurança]               │
│                                                             │
│ Potencial Econômico e de Crescimento Imobiliário:         │
│ [Texto limpo e profissional sobre potencial]               │
└─────────────────────────────────────────────────────────────┘
```

```plaintext
📁 zapImoveis/
├── 📱 app_laudo_completo.py          ← APLICAÇÃO PRINCIPAL
├── 📋 laudo_formulario.py            ← FORMULÁRIO DE ENTRADA
├── 🔍 pesquisa_localidade_ia_final.py ← PESQUISA + IA
├── 📄 gerador_laudo_docx.py          ← GERAÇÃO DE LAUDOS
├── 📊 excel_formatter.py             ← FORMATAÇÃO EXCEL
└── 🔧 .env                           ← CONFIGURAÇÃO DE CHAVES
```

```plaintext
🔑 CHAVES DE API (.env)
├── TAVILY_API_KEY=tvly-dev-...      ← PESQUISA NA INTERNET
├── OPENAI_API_KEY=sk-proj-...       ← TRATAMENTO DE TEXTO
└── GROQ_API_KEY=gsk_...             ← ALTERNATIVA (não usada)
```

```python
# app_laudo_completo.py linha 147
bairro = dados_imovel.get('loteamento', 'Jardim Santa Virgínia')

# pesquisa_localidade_ia_final.py linha 47
query = f"""Informações sobre {bairro} em {cidade} São Paulo..."""
```

```python
# pesquisa_localidade_ia_final.py linha 47
response = self.agent.run(query)  # ← TAVILY

# pesquisa_localidade_ia_final.py linha 86
resposta_tratada = self.agent.run(prompt_tratamento)  # ← IA
```

```python
# app_laudo_completo.py linha 172
texto_pesquisa = self.pesquisa_localidade.gerar_texto_pesquisa_localidade(cidade, bairro)

# app_laudo_completo.py linha 228
self.gerador_docx.gerar_laudo_completo(
    dados_imovel=dados_imovel,
    dados_avaliador=dados_avaliador,
    dados_scraper=dados_scraper,
    texto_pesquisa_localidade=texto_pesquisa  # ← TEXTO TRATADO PELA IA
)
```

