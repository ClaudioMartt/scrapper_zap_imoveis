import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeIARobusta:
    def __init__(self):
        """Inicializa a pesquisa com verificação de chaves"""
        self.timeout = 30
        self.cache = {}
        
        # Verificar se as chaves estão configuradas
        self.tavily_key = os.getenv('TAVILY_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if not self.tavily_key or self.tavily_key == 'sua_chave_tavily_aqui':
            print("⚠️ AVISO: TAVILY_API_KEY não configurada!")
            self.agent_tavily = None
        else:
            try:
                model_tavily = OpenAIChat(id="gpt-4o-mini")
                self.agent_tavily = Agent(tools=[TavilyTools()])
                self.agent_tavily.model = model_tavily
                print("✅ Tavily configurado corretamente!")
                
            except Exception as e:
                print(f"❌ Erro ao configurar Tavily: {e}")
                self.agent_tavily = None
        
        # Configurar IA para tratamento
        if not self.openai_key or self.openai_key == 'sua_chave_openai_aqui':
            print("⚠️ AVISO: OPENAI_API_KEY não configurada!")
            self.model_ia = None
        else:
            try:
                self.model_ia = OpenAIChat(id="gpt-4o-mini")
                print("✅ IA para tratamento configurada!")
                
            except Exception as e:
                print(f"❌ Erro ao configurar IA: {e}")
                self.model_ia = None
        
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera texto de pesquisa REAL usando Tavily + IA para tratamento"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_ia_robusta"
            if cache_key in self.cache:
                print("📋 Usando dados do cache")
                return self.cache[cache_key]
            
            # Verificar se Tavily está configurado
            if not self.agent_tavily:
                print("⚠️ Tavily não configurado, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
            
            print(f"🔍 Pesquisando informações REAIS para {bairro}, {cidade}...")
            start_time = time.time()
            
            # Query simples e direta para o Tavily
            query = f"""Informações sobre {bairro} em {cidade} São Paulo: comércio, serviços, lazer, segurança e potencial econômico. Foque especificamente no bairro {bairro}."""
            
            # Executar pesquisa REAL no Tavily
            response = self.agent_tavily.run(query)
            tempo_pesquisa = time.time() - start_time
            
            print(f"⏱️ Pesquisa REAL concluída em {tempo_pesquisa:.1f} segundos")
            
            # Verificar se a resposta é válida
            if response and str(response).strip():
                print("🤖 Submetendo dados à IA para tratamento e organização...")
                
                # Submeter à IA para tratamento e organização
                texto_tratado = self._tratar_com_ia_robusta(str(response), cidade, bairro)
                
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
    
    def _tratar_com_ia_robusta(self, dados_brutos, cidade, bairro):
        """Submete os dados brutos à IA para tratamento e organização"""
        try:
            # Verificar se a IA está configurada
            if not self.model_ia:
                print("⚠️ IA não configurada, usando limpeza manual")
                return self._limpeza_manual(dados_brutos)
            
            # Prompt específico para a IA organizar os dados
            prompt_ia = f"""
Você é um especialista em análise de localidades para laudos imobiliários. 

ORGANIZE as informações brutas abaixo sobre o bairro {bairro} em {cidade} em um texto conciso e profissional.

DADOS BRUTOS:
{dados_brutos}

REGRAS:
1. Organize em 3 seções: "Comércio, Lazer e Comodidade", "Segurança", "Potencial Econômico e de Crescimento Imobiliário"
2. Máximo 5 linhas por seção
3. Linguagem concisa e profissional
4. Remova informações desnecessárias, repetições e caracteres especiais
5. Foque apenas em informações relevantes para avaliação imobiliária
6. Use linguagem clara e objetiva
7. Se não houver informações específicas sobre o bairro, use informações gerais da cidade

FORMATO:
Comércio, Lazer e Comodidade:
[Texto conciso sobre comércio e serviços]

Segurança:
[Texto conciso sobre segurança]

Potencial Econômico e de Crescimento Imobiliário:
[Texto conciso sobre potencial econômico]

Responda APENAS com o texto organizado, sem explicações adicionais.
"""
            
            # Usar a IA para tratar os dados
            resposta_ia = self.model_ia.invoke(prompt_ia)
            
            if resposta_ia and str(resposta_ia).strip():
                texto_limpo = self._limpar_resposta_ia(str(resposta_ia))
                return texto_limpo
            else:
                print("⚠️ IA não retornou resposta válida, usando limpeza manual")
                return self._limpeza_manual(dados_brutos)
                
        except Exception as e:
            print(f"❌ Erro no tratamento pela IA: {e}")
            print("⚠️ Usando limpeza manual como fallback")
            return self._limpeza_manual(dados_brutos)
    
    def _limpeza_manual(self, dados_brutos):
        """Limpeza manual quando a IA não está disponível"""
        try:
            # Limpeza básica
            texto = str(dados_brutos)
            
            # Remover textos desnecessários
            textos_remover = [
                'RunResponse content', 'content', 'name=None', 'tool_call_id=None', 'to...',
                'Visão Geral do Bairro', 'Destacam-se', 'apresenta uma perspectiva',
                'enquanto alguns', 'relatam que', 'contribuem para', 'fazem do bairro',
                'Esta centralidade', 'com variações de', 'dependendo da localização'
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
            secoes = self._dividir_em_secoes_basicas(texto)
            
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
    
    def _dividir_em_secoes_basicas(self, texto):
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
    
    def _limpar_resposta_ia(self, texto):
        """Limpa a resposta da IA"""
        if not texto:
            return ""
        
        # Limpeza básica
        texto = str(texto).strip()
        
        # Remover caracteres de escape
        texto = texto.replace('\\n', '\n')
        texto = texto.replace('\\"', '"')
        
        # Remover formatação markdown se houver
        texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)
        texto = re.sub(r'\*([^*]+)\*', r'\1', texto)
        
        # Limpar espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto)
        texto = re.sub(r' \n', '\n', texto)
        
        return texto.strip()
    
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

"""
    
    def verificar_configuracao(self):
        """Verifica se a configuração está correta"""
        print("🔍 Verificando configuração...")
        
        if not self.tavily_key or self.tavily_key == 'sua_chave_tavily_aqui':
            print("❌ TAVILY_API_KEY não configurada!")
            return False
        
        if not self.openai_key or self.openai_key == 'sua_chave_openai_aqui':
            print("❌ OPENAI_API_KEY não configurada!")
            return False
        
        if self.agent_tavily and self.model_ia:
            print("✅ Configuração correta!")
            return True
        else:
            print("❌ Erro na configuração")
            return False

def main():
    """Teste da versão com IA robusta"""
    print("🚀 TESTE DA PESQUISA COM IA ROBUSTA")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeIARobusta()
    
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
        print("\n✅ Resultado TRATADO PELA IA:")
        print("=" * 50)
        print(texto)
        print("=" * 50)
    else:
        print("\n⚠️ Nenhuma informação encontrada")

if __name__ == "__main__":
    main()
