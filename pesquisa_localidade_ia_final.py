import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeIAFinal:
    def __init__(self):
        """Inicializa a pesquisa com verificação de chaves"""
        self.timeout = 30
        self.cache = {}
        
        # Verificar se as chaves estão configuradas
        self.tavily_key = os.getenv('TAVILY_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if not self.tavily_key or self.tavily_key == 'sua_chave_tavily_aqui':
            print("⚠️ AVISO: TAVILY_API_KEY não configurada!")
            self.agent = None
        else:
            try:
                model = OpenAIChat(id="gpt-4o-mini")
                self.agent = Agent(tools=[TavilyTools()])
                self.agent.model = model
                print("✅ Tavily configurado corretamente!")
                
            except Exception as e:
                print(f"❌ Erro ao configurar Tavily: {e}")
                self.agent = None
        
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera texto de pesquisa REAL usando Tavily + IA para tratamento"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_ia_final"
            if cache_key in self.cache:
                print("📋 Usando dados do cache")
                return self.cache[cache_key]
            
            # Verificar se Tavily está configurado
            if not self.agent:
                print("⚠️ Tavily não configurado, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
            
            print(f"🔍 Pesquisando informações REAIS para {bairro}, {cidade}...")
            start_time = time.time()
            
            # Query simples e direta para o Tavily
            query = f"""Informações sobre {bairro} em {cidade} São Paulo: comércio, serviços, lazer, segurança e potencial econômico. Foque especificamente no bairro {bairro}."""
            
            # Executar pesquisa REAL no Tavily
            response = self.agent.run(query)
            tempo_pesquisa = time.time() - start_time
            
            print(f"⏱️ Pesquisa REAL concluída em {tempo_pesquisa:.1f} segundos")
            
            # Verificar se a resposta é válida
            if response and str(response).strip():
                print("🤖 Submetendo dados à IA para tratamento e organização...")
                
                # Submeter à IA para tratamento e organização
                texto_tratado = self._tratar_com_ia_final(str(response), cidade, bairro)
                
                if texto_tratado and len(texto_tratado) > 50:
                    self.cache[cache_key] = texto_tratado
                    print("✅ Informações tratadas pela IA com sucesso!")
                    return texto_tratado
                else:
                    print("⚠️ IA não conseguiu tratar os dados, usando texto padrão")
                    return self._gerar_texto_padrao_fallback(cidade, bairro)
            else:
                print("⚠️ Resposta vazia, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro na pesquisa real: {e}")
            return self._gerar_texto_padrao_fallback(cidade, bairro)
    
    def _tratar_com_ia_final(self, dados_brutos, cidade, bairro):
        """Submete os dados brutos à IA para tratamento e organização"""
        try:
            # Usar o mesmo agente para tratar os dados
            prompt_tratamento = f"""
Organize as informações brutas abaixo sobre o bairro {bairro} em {cidade} em um texto conciso e profissional para um laudo imobiliário.

DADOS BRUTOS:
{dados_brutos}

INSTRUÇÕES:
1. Organize em 3 seções: "Comércio, Lazer e Comodidade", "Segurança", "Potencial Econômico e de Crescimento Imobiliário"
2. Máximo 5 linhas por seção
3. Linguagem concisa e profissional
4. Remova informações desnecessárias, repetições e caracteres especiais
5. Foque apenas em informações relevantes para avaliação imobiliária
6. Use linguagem clara e objetiva

FORMATO:
Comércio, Lazer e Comodidade:
[Texto conciso sobre comércio e serviços]

Segurança:
[Texto conciso sobre segurança]

Potencial Econômico e de Crescimento Imobiliário:
[Texto conciso sobre potencial econômico]

Responda APENAS com o texto organizado.
"""
            
            # Usar o agente para tratar os dados
            resposta_tratada = self.agent.run(prompt_tratamento)
            
            if resposta_tratada and str(resposta_tratada).strip():
                texto_limpo = self._extrair_texto_limpo(str(resposta_tratada))
                return texto_limpo
            else:
                print("⚠️ Agente não retornou resposta válida, usando limpeza manual")
                return self._limpeza_manual_fallback(dados_brutos, cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro no tratamento pela IA: {e}")
            print("⚠️ Usando limpeza manual como fallback")
            return self._limpeza_manual_fallback(dados_brutos, cidade, bairro)
    
    def _extrair_texto_limpo(self, resposta_ia):
        """Extrai apenas o texto limpo da resposta da IA"""
        if not resposta_ia:
            return ""
        
        # Converter para string
        texto = str(resposta_ia)
        
        # Procurar pelo conteúdo limpo entre as seções
        # Padrão: "Comércio, Lazer e Comodidade:" até o final
        inicio = texto.find("Comércio, Lazer e Comodidade:")
        
        if inicio != -1:
            # Pegar o texto a partir do início das seções
            texto_limpo = texto[inicio:]
            
            # Remover metadados e informações técnicas
            texto_limpo = re.sub(r'RunResponse\(content=\'', '', texto_limpo)
            texto_limpo = re.sub(r'\', content_type=.*', '', texto_limpo)
            texto_limpo = re.sub(r'Message\(role=.*', '', texto_limpo)
            texto_limpo = re.sub(r'metrics=.*', '', texto_limpo)
            texto_limpo = re.sub(r'created_at=.*', '', texto_limpo)
            
            # Limpar caracteres de escape
            texto_limpo = texto_limpo.replace('\\n', '\n')
            texto_limpo = texto_limpo.replace('\\"', '"')
            texto_limpo = texto_limpo.replace('\\', '')
            
            # Limpar espaços múltiplos
            texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
            texto_limpo = re.sub(r' \n', '\n', texto_limpo)
            
            return texto_limpo.strip()
        
        return texto
    
    def _limpeza_manual_fallback(self, dados_brutos, cidade, bairro):
        """Limpeza manual quando a IA não está disponível"""
        try:
            # Limpeza básica
            texto = str(dados_brutos)
            
            # Remover textos desnecessários
            textos_remover = [
                'RunResponse content', 'content', 'name=None', 'tool_call_id=None', 'to...',
                'Visão Geral do Bairro', 'Destacam-se', 'apresenta uma perspectiva',
                'enquanto alguns', 'relatam que', 'contribuem para', 'fazem do bairro'
            ]
            
            for texto_remover in textos_remover:
                texto = texto.replace(texto_remover, ' ')
            
            # Remover caracteres de escape
            texto = texto.replace('\\n', ' ')
            texto = texto.replace('\n', ' ')
            texto = texto.replace('\\"', '"')
            texto = texto.replace('\\', ' ')
            texto = texto.replace('•', '')
            texto = texto.replace('**', '')
            texto = texto.replace('*', '')
            
            # Limpar espaços múltiplos
            texto = re.sub(r'\s+', ' ', texto)
            texto = texto.strip()
            
            # Dividir em seções básicas
            secoes = self._dividir_em_secoes_basicas(texto, cidade, bairro)
            
            # Montar texto final
            texto_final = ""
            
            if secoes['comercio']:
                texto_final += f"Comércio, Lazer e Comodidade:\n{secoes['comercio']}\n\n"
            
            if secoes['seguranca']:
                texto_final += f"Segurança:\n{secoes['seguranca']}\n\n"
            
            if secoes['potencial']:
                texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{secoes['potencial']}\n\n"
            
            return texto_final.strip()
            
        except Exception as e:
            print(f"❌ Erro na limpeza manual: {e}")
            return None
    
    def _dividir_em_secoes_basicas(self, texto, cidade, bairro):
        """Divide o texto em seções básicas"""
        secoes = {
            'comercio': '',
            'seguranca': '',
            'potencial': ''
        }
        
        texto_lower = texto.lower()
        
        # Palavras-chave para cada seção
        palavras_comercio = ['comércio', 'mercado', 'supermercado', 'padaria', 'farmácia', 'posto', 'banco', 'loja', 'shopping', 'restaurante']
        palavras_seguranca = ['segurança', 'criminalidade', 'violência', 'policial', 'crime', 'roubo', 'furto', 'homicídio']
        palavras_potencial = ['crescimento', 'investimento', 'desenvolvimento', 'valorização', 'econômico', 'imobiliário', 'aluguel', 'preços']
        
        # Extrair seções
        for secao, palavras in [('comercio', palavras_comercio), ('seguranca', palavras_seguranca), ('potencial', palavras_potencial)]:
            for palavra in palavras:
                if palavra in texto_lower:
                    inicio = texto_lower.find(palavra)
                    if inicio != -1:
                        contexto = texto[max(0, inicio-50):min(len(texto), inicio+200)]
                        contexto = contexto.strip()
                        if contexto and len(contexto) > 20:
                            secoes[secao] += contexto + " "
                            break  # Pegar apenas o primeiro contexto encontrado
        
        # Limitar tamanho das seções
        for key in secoes:
            secoes[key] = secoes[key].strip()
            if len(secoes[key]) > 300:
                secoes[key] = secoes[key][:300] + "..."
        
        return secoes
    
    def _gerar_texto_padrao_fallback(self, cidade, bairro):
        """Texto padrão quando não consegue fazer pesquisa real"""
        return f"""Comércio, Lazer e Comodidade:
{bairro} em {cidade} oferece comércio local e serviços essenciais básicos. 
Disponibilidade de mercados, padarias e farmácias no entorno da região.

Segurança:
{cidade} apresenta níveis de segurança típicos da região. 
{bairro} mantém características de segurança compatíveis com o perfil da cidade.

Potencial Econômico e de Crescimento Imobiliário:
{bairro} em {cidade} possui potencial de desenvolvimento baseado na 
localização e infraestrutura disponível na região.

⚠️ NOTA: Informações gerais - configure a chave TAVILY_API_KEY para obter dados específicos e atualizados."""
    
    def verificar_configuracao(self):
        """Verifica se a configuração está correta"""
        print("🔍 Verificando configuração...")
        
        if not self.tavily_key or self.tavily_key == 'sua_chave_tavily_aqui':
            print("❌ TAVILY_API_KEY não configurada!")
            return False
        
        if not self.openai_key or self.openai_key == 'sua_chave_openai_aqui':
            print("❌ OPENAI_API_KEY não configurada!")
            return False
        
        if self.agent:
            print("✅ Configuração correta!")
            return True
        else:
            print("❌ Erro na configuração do agente")
            return False

def main():
    """Teste da versão com IA final"""
    print("🚀 TESTE DA PESQUISA COM IA FINAL")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeIAFinal()
    
    # Verificar configuração
    if not pesquisa.verificar_configuracao():
        print("\n⚠️ Configure as chaves de API para testar a pesquisa real")
        return
    
    cidade = "São Paulo"
    bairro = "Consolação"
    
    print(f"\n📍 Testando pesquisa real: {bairro}, {cidade}")
    
    start_time = time.time()
    texto = pesquisa.gerar_texto_pesquisa_localidade(cidade, bairro)
    total_time = time.time() - start_time
    
    print(f"\n⏱️ Tempo total: {total_time:.1f} segundos")
    
    if texto:
        print("\n✅ Resultado TRATADO COM IA:")
        print("=" * 50)
        print(texto)
        print("=" * 50)
    else:
        print("\n⚠️ Nenhuma informação encontrada")

if __name__ == "__main__":
    main()
