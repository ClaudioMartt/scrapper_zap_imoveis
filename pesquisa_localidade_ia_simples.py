import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeIASimples:
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
        
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera texto de pesquisa REAL usando Tavily + IA para tratamento"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_ia_simples"
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
                print("🤖 Tratando dados com IA integrada...")
                
                # Tratar com IA integrada
                texto_tratado = self._tratar_com_ia_integrada(str(response), cidade, bairro)
                
                if texto_tratado and len(texto_tratado) > 50:
                    self.cache[cache_key] = texto_tratado
                    print("✅ Informações tratadas com sucesso!")
                    return texto_tratado
                else:
                    print("⚠️ Não foi possível tratar os dados, usando texto padrão")
                    return self._gerar_texto_padrao_fallback(cidade, bairro)
            else:
                print("⚠️ Resposta vazia, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro na pesquisa real: {e}")
            return self._gerar_texto_padrao_fallback(cidade, bairro)
    
    def _tratar_com_ia_integrada(self, dados_brutos, cidade, bairro):
        """Trata os dados usando IA integrada no próprio agente"""
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
            resposta_tratada = self.agent_tavily.run(prompt_tratamento)
            
            if resposta_tratada and str(resposta_tratada).strip():
                texto_limpo = self._limpar_resposta_final(str(resposta_tratada))
                return texto_limpo
            else:
                print("⚠️ Agente não retornou resposta válida, usando limpeza manual")
                return self._limpeza_manual_avancada(dados_brutos, cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro no tratamento pela IA: {e}")
            print("⚠️ Usando limpeza manual avançada como fallback")
            return self._limpeza_manual_avancada(dados_brutos, cidade, bairro)
    
    def _limpeza_manual_avancada(self, dados_brutos, cidade, bairro):
        """Limpeza manual avançada quando a IA não está disponível"""
        try:
            # Limpeza básica
            texto = str(dados_brutos)
            
            # Remover textos desnecessários
            textos_remover = [
                'RunResponse content', 'content', 'name=None', 'tool_call_id=None', 'to...',
                'Visão Geral do Bairro', 'Destacam-se', 'apresenta uma perspectiva',
                'enquanto alguns', 'relatam que', 'contribuem para', 'fazem do bairro',
                'Esta centralidade', 'com variações de', 'dependendo da localização',
                'Vamos explorar cada um desses aspectos', 'Como consultórios',
                'Considerações Finais Em resumo', 'Na fácil acesso',
                'As percepções sobre', 'são misturadas', 'mencionam preocupações'
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
            
            # Remover formatação markdown
            texto = re.sub(r'###?\s*', '', texto)
            texto = re.sub(r'##\s*', '', texto)
            texto = re.sub(r'#\s*', '', texto)
            texto = re.sub(r'-\s*', '', texto)
            texto = re.sub(r'\d+\.\s*', '', texto)
            
            # Remover URLs e links
            texto = re.sub(r'http[s]?://[^\s]+', '', texto)
            texto = re.sub(r'\([^)]*\.html[^)]*\)', '', texto)
            
            # Limpar espaços múltiplos
            texto = re.sub(r'\s+', ' ', texto)
            texto = texto.strip()
            
            # Dividir em seções inteligentes
            secoes = self._dividir_em_secoes_inteligentes(texto, cidade, bairro)
            
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
    
    def _dividir_em_secoes_inteligentes(self, texto, cidade, bairro):
        """Divide o texto em seções de forma inteligente"""
        secoes = {
            'comercio': '',
            'seguranca': '',
            'potencial': ''
        }
        
        texto_lower = texto.lower()
        
        # Palavras-chave específicas para cada seção
        palavras_comercio = ['comércio', 'mercado', 'supermercado', 'padaria', 'farmácia', 'posto', 'banco', 'loja', 'shopping', 'restaurante', 'comercial', 'serviços']
        palavras_seguranca = ['segurança', 'criminalidade', 'violência', 'policial', 'crime', 'roubo', 'furto', 'homicídio', 'policiamento', 'assaltos']
        palavras_potencial = ['crescimento', 'investimento', 'desenvolvimento', 'valorização', 'econômico', 'imobiliário', 'aluguel', 'preços', 'valores', 'imóveis']
        
        # Extrair seções com contexto inteligente
        for secao, palavras in [('comercio', palavras_comercio), ('seguranca', palavras_seguranca), ('potencial', palavras_potencial)]:
            melhor_contexto = ""
            melhor_score = 0
            
            for palavra in palavras:
                if palavra in texto_lower:
                    inicio = texto_lower.find(palavra)
                    if inicio != -1:
                        # Pegar contexto ao redor da palavra
                        inicio_contexto = max(0, inicio - 100)
                        fim_contexto = min(len(texto), inicio + 300)
                        contexto = texto[inicio_contexto:fim_contexto]
                        
                        # Limpar contexto
                        contexto_limpo = self._limpar_contexto_inteligente(contexto)
                        
                        # Calcular score baseado na relevância
                        score = self._calcular_score_relevancia(contexto_limpo, palavras)
                        
                        if score > melhor_score:
                            melhor_score = score
                            melhor_contexto = contexto_limpo
            
            if melhor_contexto:
                secoes[secao] = self._limitar_linhas_inteligente(melhor_contexto, 5)
        
        return secoes
    
    def _limpar_contexto_inteligente(self, contexto):
        """Limpa um contexto de forma inteligente"""
        if not contexto:
            return ""
        
        # Limpeza básica
        contexto = contexto.strip()
        contexto = re.sub(r'\s+', ' ', contexto)
        
        # Remover frases desnecessárias
        frases_remover = [
            'apresenta uma perspectiva', 'enquanto alguns moradores',
            'relatam que a presença', 'contribuem para uma sensação',
            'Esta centralidade e diversidade', 'fazem do bairro um lugar',
            'com variações de', 'dependendo da localização',
            'Vamos explorar cada um desses aspectos', 'Como consultórios',
            'Considerações Finais Em resumo', 'Na fácil acesso',
            'As percepções sobre', 'são misturadas', 'mencionam preocupações'
        ]
        
        for frase in frases_remover:
            contexto = contexto.replace(frase, ' ')
        
        # Capitalizar primeira letra
        if contexto:
            contexto = contexto[0].upper() + contexto[1:]
        
        # Adicionar ponto final se necessário
        if contexto and not contexto.endswith(('.', '!', '?')):
            contexto += "."
        
        return contexto
    
    def _calcular_score_relevancia(self, texto, palavras_chave):
        """Calcula score de relevância do texto"""
        if not texto:
            return 0
        
        score = 0
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                score += 1
        
        # Bonus por tamanho adequado
        if 50 <= len(texto) <= 300:
            score += 2
        
        return score
    
    def _limitar_linhas_inteligente(self, texto, max_linhas):
        """Limita o texto a um número máximo de linhas de forma inteligente"""
        if not texto:
            return ""
        
        # Dividir em sentenças
        sentencas = re.split(r'[.!?]+', texto)
        sentencas = [s.strip() for s in sentencas if s.strip()]
        
        # Pegar apenas as sentenças mais relevantes
        texto_limite = []
        palavras_totais = 0
        palavras_por_linha = 12
        palavras_maximas = max_linhas * palavras_por_linha
        
        for sentenca in sentencas:
            if sentenca:
                palavras_sentenca = len(sentenca.split())
                if palavras_totais + palavras_sentenca <= palavras_maximas:
                    texto_limite.append(sentenca)
                    palavras_totais += palavras_sentenca
                else:
                    break
        
        resultado = '. '.join(texto_limite)
        if resultado and not resultado.endswith('.'):
            resultado += '.'
        
        return resultado
    
    def _limpar_resposta_final(self, texto):
        """Limpa a resposta final"""
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
        
        if self.agent_tavily:
            print("✅ Configuração correta!")
            return True
        else:
            print("❌ Erro na configuração do agente")
            return False

def main():
    """Teste da versão com IA simples"""
    print("🚀 TESTE DA PESQUISA COM IA SIMPLES")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeIASimples()
    
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
