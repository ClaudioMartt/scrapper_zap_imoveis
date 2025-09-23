import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeFinal:
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
        """Gera texto de pesquisa REAL usando Tavily com texto final limpo"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_final"
            if cache_key in self.cache:
                print("📋 Usando dados do cache")
                return self.cache[cache_key]
            
            # Verificar se Tavily está configurado
            if not self.agent:
                print("⚠️ Tavily não configurado, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
            
            print(f"🔍 Pesquisando informações REAIS para {bairro}, {cidade}...")
            start_time = time.time()
            
            # Query simples e direta
            query = f"""Informações sobre {bairro} em {cidade} São Paulo: comércio, serviços, lazer, segurança e potencial econômico. Foque especificamente no bairro {bairro}."""
            
            # Executar pesquisa REAL
            response = self.agent.run(query)
            tempo_pesquisa = time.time() - start_time
            
            print(f"⏱️ Pesquisa REAL concluída em {tempo_pesquisa:.1f} segundos")
            
            # Verificar se a resposta é válida
            if response and str(response).strip():
                # Processar resposta real com limpeza final
                texto_final = self._processar_resposta_final(str(response), cidade, bairro)
                
                if texto_final and len(texto_final) > 50:
                    self.cache[cache_key] = texto_final
                    print("✅ Informações reais obtidas e processadas com sucesso!")
                    return texto_final
                else:
                    print("⚠️ Resposta muito curta, usando texto padrão")
                    return self._gerar_texto_padrao_fallback(cidade, bairro)
            else:
                print("⚠️ Resposta vazia, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro na pesquisa real: {e}")
            return self._gerar_texto_padrao_fallback(cidade, bairro)
    
    def _processar_resposta_final(self, texto, cidade, bairro):
        """Processa a resposta do Tavily com limpeza final"""
        if not texto:
            return ""
        
        # Limpeza extrema de texto desnecessário
        texto = self._limpar_texto_extremo(texto)
        
        # Extrair informações essenciais
        secoes = self._extrair_informacoes_essenciais(texto, cidade, bairro)
        
        # Montar texto final conciso (máximo 5 linhas por seção)
        texto_final = ""
        
        if secoes['comercio']:
            texto_final += f"Comércio, Lazer e Comodidade:\n{secoes['comercio']}\n\n"
        
        if secoes['seguranca']:
            texto_final += f"Segurança:\n{secoes['seguranca']}\n\n"
        
        if secoes['potencial']:
            texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{secoes['potencial']}\n\n"
        
        # Se não conseguiu extrair seções específicas, usar texto geral resumido
        if not texto_final.strip():
            texto_resumido = self._resumir_texto_essencial(texto, 300)
            texto_final = f"Informações sobre {bairro}, {cidade}:\n{texto_resumido}"
        
        return texto_final.strip()
    
    def _limpar_texto_extremo(self, texto):
        """Limpeza extrema removendo tudo que não é relevante"""
        if not texto:
            return ""
        
        # Remover textos desnecessários
        texto = str(texto)
        
        # Remover completamente textos indesejados
        textos_remover = [
            'RunResponse content', 'content', 'name=None', 'tool_call_id=None', 'to...',
            'Visão Geral do Bairro', 'Destacam-se', 'apresenta uma perspectiva',
            'enquanto alguns', 'relatam que', 'contribuem para', 'fazem do bairro',
            'Esta centralidade', 'com variações de', 'dependendo da localização',
            'Vamos explorar cada um desses aspectos', 'Como consultórios',
            'Considerações Finais Em resumo', 'Na fácil acesso',
            'As percepções sobre', 'são misturadas', 'mencionam preocupações',
            'A qualidade das ruas', 'foram também citadas'
        ]
        
        for texto_remover in textos_remover:
            texto = texto.replace(texto_remover, ' ')
        
        # Remover caracteres de escape e formatação
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
        texto = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', texto)
        
        # Remover valores monetários incompletos
        texto = re.sub(r'R\s*\$\s*000', 'R$ valores variados', texto)
        texto = re.sub(r'R\s*\$\s*525', '', texto)
        texto = re.sub(r'R\s*\$\s*\d+\.000', 'R$ valores variados', texto)
        
        # Limpar espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto)
        texto = texto.strip()
        
        return texto
    
    def _extrair_informacoes_essenciais(self, texto, cidade, bairro):
        """Extrai apenas informações essenciais com máximo de 5 linhas cada"""
        secoes = {
            'comercio': '',
            'seguranca': '',
            'potencial': ''
        }
        
        texto_lower = texto.lower()
        
        # Palavras-chave específicas para cada seção
        palavras_comercio = ['comércio', 'mercado', 'supermercado', 'padaria', 'farmácia', 'posto', 'banco', 'loja', 'shopping', 'restaurante', 'comercial', 'serviços', 'centro comercial']
        palavras_seguranca = ['segurança', 'criminalidade', 'violência', 'policial', 'crime', 'roubo', 'furto', 'homicídio', 'policiamento', 'presença policial', 'assaltos']
        palavras_potencial = ['crescimento', 'investimento', 'desenvolvimento', 'valorização', 'econômico', 'imobiliário', 'aluguel', 'preços', 'valores', 'imóveis']
        
        # Extrair seções com foco em informações essenciais
        for secao, palavras in [('comercio', palavras_comercio), ('seguranca', palavras_seguranca), ('potencial', palavras_potencial)]:
            informacoes_encontradas = []
            
            for palavra in palavras:
                if palavra in texto_lower:
                    inicio = texto_lower.find(palavra)
                    if inicio != -1:
                        # Pegar contexto menor para evitar repetições
                        inicio_contexto = max(0, inicio - 30)
                        fim_contexto = min(len(texto), inicio + 150)
                        contexto = texto[inicio_contexto:fim_contexto]
                        
                        contexto_limpo = self._limpar_contexto_final(contexto)
                        if contexto_limpo and len(contexto_limpo) > 15:
                            informacoes_encontradas.append(contexto_limpo)
            
            # Combinar informações e limitar a 5 linhas
            if informacoes_encontradas:
                texto_combinado = ' '.join(informacoes_encontradas[:1])  # Apenas 1 contexto por seção
                secoes[secao] = self._limitar_linhas_final(texto_combinado, 5)
        
        return secoes
    
    def _limpar_contexto_final(self, contexto):
        """Limpa um contexto específico de forma final"""
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
            'As percepções sobre', 'são misturadas', 'mencionam preocupações',
            'A qualidade das ruas', 'foram também citadas'
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
    
    def _limitar_linhas_final(self, texto, max_linhas):
        """Limita o texto a um número máximo de linhas de forma rigorosa"""
        if not texto:
            return ""
        
        # Dividir em sentenças
        sentencas = re.split(r'[.!?]+', texto)
        sentencas = [s.strip() for s in sentencas if s.strip()]
        
        # Pegar apenas as primeiras sentenças necessárias
        texto_limite = []
        palavras_totais = 0
        palavras_por_linha = 12  # Aproximadamente 12 palavras por linha
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
    
    def _resumir_texto_essencial(self, texto, max_chars):
        """Resume o texto de forma essencial"""
        if len(texto) <= max_chars:
            return texto
        
        # Tentar quebrar em frase completa
        texto_resumido = texto[:max_chars]
        ultimo_ponto = texto_resumido.rfind('.')
        
        if ultimo_ponto > max_chars * 0.7:
            return texto_resumido[:ultimo_ponto + 1]
        else:
            return texto_resumido + "..."
    
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
    """Teste da versão final"""
    print("🚀 TESTE DA PESQUISA FINAL")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeFinal()
    
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
        print("\n✅ Resultado FINAL:")
        print("=" * 50)
        print(texto)
        print("=" * 50)
    else:
        print("\n⚠️ Nenhuma informação encontrada")

if __name__ == "__main__":
    main()
