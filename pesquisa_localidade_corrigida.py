import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeCorrigida:
    def __init__(self):
        """Inicializa a pesquisa com verificação de chaves"""
        self.timeout = 30
        self.cache = {}
        
        # Verificar se as chaves estão configuradas
        self.tavily_key = os.getenv('TAVILY_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if not self.tavily_key or self.tavily_key == 'sua_chave_tavily_aqui':
            print("⚠️ AVISO: TAVILY_API_KEY não configurada!")
            print("📝 Configure sua chave no arquivo .env")
            self.agent = None
        else:
            try:
                # Configurar modelo OpenAI
                model = OpenAIChat(id="gpt-4o-mini")
                
                # Criar agente com Tavily
                self.agent = Agent(tools=[TavilyTools()])
                self.agent.model = model
                print("✅ Tavily configurado corretamente!")
                
            except Exception as e:
                print(f"❌ Erro ao configurar Tavily: {e}")
                self.agent = None
        
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera texto de pesquisa REAL usando Tavily"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_real"
            if cache_key in self.cache:
                print("📋 Usando dados do cache")
                return self.cache[cache_key]
            
            # Verificar se Tavily está configurado
            if not self.agent:
                print("⚠️ Tavily não configurado, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
            
            print(f"🔍 Pesquisando informações REAIS para {bairro}, {cidade}...")
            start_time = time.time()
            
            # Query otimizada para busca real
            query = f"""Pesquise informações específicas e atualizadas sobre o bairro {bairro} na cidade {cidade}.
        
            

            Foque em:
            1. COMÉRCIO E SERVIÇOS: mercados, supermercados, padarias, farmácias, postos de gasolina, bancos, lojas de conveniência
            2. LAZER: praças, parques, clubes, academias, centros de lazer, restaurantes
            3. SEGURANÇA: índices de criminalidade, violência, presença policial, sensação de segurança
            4. POTENCIAL ECONÔMICO: crescimento, investimentos, valorização imobiliária, desenvolvimento



            Forneça informações específicas e atuais sobre {bairro}, {cidade}. Se não encontrar informações específicas sobre o bairro, forneça informações sobre a cidade {cidade} em geral."""
            
            # Executar pesquisa REAL
            response = self.agent.run(query)
            tempo_pesquisa = time.time() - start_time
            
            print(f"⏱️ Pesquisa REAL concluída em {tempo_pesquisa:.1f} segundos")
            
            # Verificar se a resposta é válida
            if response and str(response).strip():
                # Processar resposta real
                texto_estruturado = self._processar_resposta_real(str(response), cidade, bairro)
                
                if texto_estruturado and len(texto_estruturado) > 100:  # Verificar se tem conteúdo substancial
                    self.cache[cache_key] = texto_estruturado
                    print("✅ Informações reais obtidas com sucesso!")
                    return texto_estruturado
                else:
                    print("⚠️ Resposta muito curta, usando texto padrão")
                    return self._gerar_texto_padrao_fallback(cidade, bairro)
            else:
                print("⚠️ Resposta vazia, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro na pesquisa real: {e}")
            return self._gerar_texto_padrao_fallback(cidade, bairro)
    
    def _processar_resposta_real(self, texto, cidade, bairro):
        """Processa a resposta real do Tavily"""
        try:
            # Limpar e estruturar o texto
            texto_limpo = self._limpar_texto_resposta(texto)
            
            # Dividir o texto em seções baseado em palavras-chave
            secoes = self._dividir_em_secoes(texto_limpo, cidade, bairro)
            
            # Montar texto estruturado e limpo
            texto_final = ""
            
            # Comércio e Serviços
            if secoes['comercio']:
                texto_final += f"Comércio, Lazer e Comodidade:\n{secoes['comercio']}\n\n"
            
            # Segurança
            if secoes['seguranca']:
                texto_final += f"Segurança:\n{secoes['seguranca']}\n\n"
            
            # Potencial Econômico
            if secoes['potencial']:
                texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{secoes['potencial']}\n\n"
            
            # Se não conseguiu extrair seções específicas, usar o texto completo limpo
            if not texto_final.strip():
                texto_resumido = texto_limpo[:800] + "..." if len(texto_limpo) > 800 else texto_limpo
                texto_final = f"Informações sobre {bairro}, {cidade}:\n{texto_resumido}"
            
            return texto_final.strip()
            
        except Exception as e:
            print(f"Erro ao processar resposta real: {e}")
            return None
    
    def _dividir_em_secoes(self, texto, cidade, bairro):
        """Divide o texto em seções específicas"""
        secoes = {
            'comercio': '',
            'seguranca': '',
            'potencial': ''
        }
        
        texto_lower = texto.lower()
        
        # Palavras-chave para cada seção
        palavras_comercio = ['comércio', 'mercado', 'supermercado', 'padaria', 'farmácia', 'posto', 'banco', 'loja', 'shopping', 'restaurante']
        palavras_seguranca = ['segurança', 'criminalidade', 'violência', 'policial', 'crime', 'roubo', 'furto', 'homicídio']
        palavras_potencial = ['crescimento', 'investimento', 'desenvolvimento', 'valorização', 'econômico', 'imobiliário']
        
        # Extrair seção de comércio
        for palavra in palavras_comercio:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    contexto = texto[max(0, inicio-100):min(len(texto), inicio+300)]
                    secoes['comercio'] += self._limpar_e_formatar_texto(contexto) + " "
        
        # Extrair seção de segurança
        for palavra in palavras_seguranca:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    contexto = texto[max(0, inicio-100):min(len(texto), inicio+300)]
                    secoes['seguranca'] += self._limpar_e_formatar_texto(contexto) + " "
        
        # Extrair seção de potencial
        for palavra in palavras_potencial:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    contexto = texto[max(0, inicio-100):min(len(texto), inicio+300)]
                    secoes['potencial'] += self._limpar_e_formatar_texto(contexto) + " "
        
        # Limpar e limitar tamanho das seções
        for key in secoes:
            secoes[key] = secoes[key].strip()
            if len(secoes[key]) > 400:
                secoes[key] = secoes[key][:400] + "..."
        
        return secoes
    
    def _limpar_e_formatar_texto(self, texto):
        """Limpa e formata um trecho de texto"""
        if not texto:
            return ""
        
        # Aplicar limpeza básica
        texto = self._limpar_texto_resposta(texto)
        
        # Remover repetições excessivas
        palavras = texto.split()
        texto_limpo = []
        for i, palavra in enumerate(palavras):
            if i == 0 or palavra.lower() != palavras[i-1].lower():
                texto_limpo.append(palavra)
        
        return ' '.join(texto_limpo)
    
    def _extrair_secao_real(self, texto, palavras_chave):
        """Extrai seção específica da resposta real"""
        texto_lower = texto.lower()
        secoes_encontradas = []
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                # Buscar contexto ao redor da palavra
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    # Buscar frase completa
                    inicio_frase = max(0, inicio - 50)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    # Limpar e estruturar
                    contexto = ' '.join(contexto.split())
                    if len(contexto) > 20:
                        secoes_encontradas.append(self._limpar_texto_resposta(contexto))
        
        return ' '.join(secoes_encontradas[:2]) if secoes_encontradas else None
    
    def _limpar_texto_resposta(self, texto):
        """Limpa o texto da resposta real"""
        if not texto:
            return ""
        
        # Remover caracteres de escape e formatação markdown
        texto = texto.replace('\\n', ' ')
        texto = texto.replace('\n', ' ')
        texto = texto.replace('**', '')
        texto = texto.replace('*', '')
        texto = texto.replace('###', '')
        texto = texto.replace('##', '')
        texto = texto.replace('#', '')
        texto = texto.replace('- ', '• ')
        texto = texto.replace('  ', ' ')
        
        # Remover URLs e links
        texto = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', texto)
        texto = re.sub(r'\([^)]*\.html[^)]*\)', '', texto)
        
        # Limpar espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto)
        texto = texto.strip()
        
        # Capitalizar primeira letra
        if texto:
            texto = texto[0].upper() + texto[1:]
        
        # Adicionar ponto final se não tiver
        if texto and not texto.endswith(('.', '!', '?')):
            texto += '.'
        
        return texto
    
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
            print("📝 Configure sua chave no arquivo .env")
            print("🔗 Obtenha uma chave gratuita em: https://tavily.com/")
            return False
        
        if not self.openai_key or self.openai_key == 'sua_chave_openai_aqui':
            print("❌ OPENAI_API_KEY não configurada!")
            print("📝 Configure sua chave no arquivo .env")
            return False
        
        if self.agent:
            print("✅ Configuração correta!")
            return True
        else:
            print("❌ Erro na configuração do agente")
            return False

def main():
    """Teste da versão corrigida"""
    print("🚀 TESTE DA PESQUISA CORRIGIDA")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeCorrigida()
    
    # Verificar configuração
    if not pesquisa.verificar_configuracao():
        print("\n⚠️ Configure as chaves de API para testar a pesquisa real")
        return
    
    cidade = "Taquarituba"
    bairro = "Jardim Santa Virgínia"
    
    print(f"\n📍 Testando pesquisa real: {bairro}, {cidade}")
    
    start_time = time.time()
    texto = pesquisa.gerar_texto_pesquisa_localidade(cidade, bairro)
    total_time = time.time() - start_time
    
    print(f"\n⏱️ Tempo total: {total_time:.1f} segundos")
    
    if texto:
        print("\n✅ Resultado:")
        print(texto)
    else:
        print("\n⚠️ Nenhuma informação encontrada")

if __name__ == "__main__":
    main()
