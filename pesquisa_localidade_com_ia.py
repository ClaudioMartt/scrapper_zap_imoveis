import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeComIA:
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
            cache_key = f"{cidade}_{bairro}_ia"
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
                texto_tratado = self._tratar_com_ia(str(response), cidade, bairro)
                
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
    
    def _tratar_com_ia(self, dados_brutos, cidade, bairro):
        """Submete os dados brutos à IA para tratamento e organização"""
        try:
            # Prompt específico para a IA organizar os dados
            prompt_ia = f"""
            Você é um especialista em análise de localidades. Organize as informações brutas abaixo sobre o bairro {bairro} em {cidade} em um texto conciso e profissional para um laudo imobiliário.

            DADOS BRUTOS:
            {dados_brutos}

            INSTRUÇÕES:
            1. Organize em 3 seções: "Comércio, Lazer e Comodidade", "Segurança", "Potencial Econômico e de Crescimento Imobiliário"
            2. Máximo 5 linhas por seção
            3. Linguagem concisa e profissional
            4. Remova informações desnecessárias, repetições e caracteres especiais
            5. Foque apenas em informações relevantes para avaliação imobiliária
            6. Use linguagem clara e objetiva
            7. Se não houver informações específicas sobre o bairro, use informações gerais da cidade

            FORMATO ESPERADO:
            Comércio, Lazer e Comodidade:
            [Texto conciso sobre comércio e serviços]

            Segurança:
            [Texto conciso sobre segurança]

            Potencial Econômico e de Crescimento Imobiliário:
            [Texto conciso sobre potencial econômico]

            Responda APENAS com o texto organizado, sem explicações adicionais.
            """
            
            # Usar a IA para tratar os dados
            if self.agent and self.agent.model:
                resposta_ia = self.agent.model.invoke(prompt_ia)
                
                if resposta_ia and str(resposta_ia).strip():
                    texto_limpo = self._limpar_resposta_ia(str(resposta_ia))
                    return texto_limpo
                else:
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"❌ Erro no tratamento pela IA: {e}")
            return None
    
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
    """Teste da versão com IA"""
    print("🚀 TESTE DA PESQUISA COM IA")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeComIA()
    
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
