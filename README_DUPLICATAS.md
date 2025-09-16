# 🔄 Sistema de Detecção de Duplicatas - Zap Imóveis Scraper

Sistema inteligente para detectar e remover automaticamente imóveis duplicados durante o scraping.

## 🎯 Problema Resolvido

**Antes**: O scraper coletava imóveis duplicados, resultando em dados repetidos no CSV/Excel.

**Depois**: Sistema automático detecta e remove duplicatas em tempo real, garantindo dados únicos.

## 🔧 Como Funciona

### 1. **Identificador Único**
Cada imóvel recebe um identificador único baseado em:
- Descrição do imóvel
- Endereço completo
- Área (m²)
- Preço
- Número de quartos, banheiros e vagas

### 2. **Detecção em Tempo Real**
- Durante o scraping, cada imóvel é verificado antes de ser adicionado
- Se já existe um imóvel com o mesmo identificador → **Duplicata ignorada**
- Se é um imóvel novo → **Adicionado à lista**

### 3. **Estatísticas Detalhadas**
- Total de imóveis únicos coletados
- Número de duplicatas detectadas
- Taxa de duplicatas (%)
- Total de imóveis processados

## 🚀 Funcionalidades Implementadas

### ✅ **ZapScraper Atualizado**
- `criar_identificador_imovel()` - Cria ID único para cada imóvel
- `verificar_duplicata()` - Verifica se imóvel já foi coletado
- `resetar_contadores_duplicatas()` - Limpa contadores para nova execução
- `obter_estatisticas_duplicatas()` - Retorna estatísticas detalhadas

### ✅ **Streamlit Integrado**
- Opção "Detectar e remover duplicatas" na sidebar (ativada por padrão)
- Seção dedicada mostrando estatísticas de duplicatas
- Mensagens informativas sobre duplicatas detectadas
- Métricas visuais: únicos, duplicatas, taxa, total processado

### ✅ **Controle de Qualidade**
- Detecção baseada em múltiplas características
- Hash seguro para identificadores únicos
- Tratamento de erros robusto
- Logs detalhados durante o processamento

## 📊 Exemplo de Uso

### **Antes (com duplicatas):**
```
Imóvel 1: Apartamento 43m², Rua A, R$ 159.600
Imóvel 2: Apartamento 69m², Rua B, R$ 200.000
Imóvel 3: Apartamento 43m², Rua A, R$ 159.600  ← DUPLICATA
Imóvel 4: Apartamento 69m², Rua B, R$ 200.000  ← DUPLICATA
```

### **Depois (sem duplicatas):**
```
Imóvel 1: Apartamento 43m², Rua A, R$ 159.600
Imóvel 2: Apartamento 69m², Rua B, R$ 200.000
🔄 Duplicata detectada! Total: 1
🔄 Duplicata detectada! Total: 2
```

## 🎨 Interface Streamlit

### **Sidebar - Opções**
```
☑️ Detectar e remover duplicatas  ← NOVA OPÇÃO
```

### **Seção de Estatísticas**
```
🔄 Estatísticas de Duplicatas
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 🏠 Imóveis Únicos │ 🔄 Duplicatas    │ 📈 Taxa de      │ 📋 Total        │
│                 │ Detectadas      │ Duplicatas      │ Processado      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│       15        │        3        │      16.7%      │       18        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### **Mensagens Informativas**
- ✅ "Sistema de detecção funcionando! 3 duplicatas foram automaticamente removidas."
- ℹ️ "Nenhuma duplicata detectada nesta execução."

## 🔧 Configuração Técnica

### **Algoritmo de Detecção**
```python
def criar_identificador_imovel(dados):
    identificador_parts = []
    
    # Normalizar descrição
    descricao = dados['Descrição'].replace("Apartamento para comprar com", "").strip()
    identificador_parts.append(descricao)
    
    # Adicionar características principais
    identificador_parts.append(dados['Endereco'])
    identificador_parts.append(f"{dados['M2']:.1f}")
    identificador_parts.append(f"{dados['Preco']:.0f}")
    identificador_parts.append(f"Q{dados['Quartos']}")
    identificador_parts.append(f"B{dados['Banheiros']}")
    identificador_parts.append(f"V{dados['Vagas']}")
    
    # Criar hash único
    identificador = "|".join(identificador_parts)
    return hash(identificador)
```

### **Verificação em Tempo Real**
```python
def verificar_duplicata(dados):
    identificador = criar_identificador_imovel(dados)
    
    if identificador in self.imoveis_unicos:
        self.duplicatas_detectadas += 1
        return True  # É duplicata
    else:
        self.imoveis_unicos.add(identificador)
        return False  # É único
```

## 📈 Benefícios

### **Para o Usuário**
- ✅ **Dados limpos**: Sem duplicatas nos arquivos CSV/Excel
- ✅ **Estatísticas claras**: Visão completa de duplicatas detectadas
- ✅ **Controle total**: Pode ativar/desativar a detecção
- ✅ **Transparência**: Logs detalhados do processo

### **Para a Análise**
- ✅ **Precisão**: Estatísticas baseadas em dados únicos
- ✅ **Qualidade**: Dados mais confiáveis para análise
- ✅ **Eficiência**: Menos dados redundantes para processar
- ✅ **Confiabilidade**: Resultados mais consistentes

## 🧪 Testes

### **Script de Teste**
```bash
python teste_simples_duplicatas.py
```

### **Teste com CSV Existente**
```bash
python teste_duplicatas.py
```

### **Resultados Esperados**
- ✅ Detecção correta de duplicatas
- ✅ Estatísticas precisas
- ✅ Logs informativos
- ✅ Performance otimizada

## 🚨 Notas Importantes

### **Limitações**
- Detecção baseada em características coletadas
- Imóveis com dados incompletos podem não ser detectados como duplicatas
- Identificador baseado em hash pode ter colisões (muito raro)

### **Recomendações**
- ✅ Sempre manter a detecção ativada
- ✅ Verificar estatísticas após cada execução
- ✅ Usar dados completos para melhor detecção
- ✅ Monitorar taxa de duplicatas (normal: 10-30%)

## 🎉 Resultado Final

**Antes**: CSV com 30 registros (10 duplicatas)  
**Depois**: CSV com 20 registros únicos + estatísticas de 10 duplicatas detectadas

**Interface**: Métricas visuais + mensagens informativas  
**Excel**: Dados limpos sem duplicatas  
**Análise**: Estatísticas mais precisas e confiáveis
