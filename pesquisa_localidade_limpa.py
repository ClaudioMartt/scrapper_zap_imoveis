import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeLimpa:
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
        """Gera texto de pesquisa REAL usando Tavily com texto limpo"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_limpo"
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
                # Processar resposta real com limpeza avançada
                texto_limpo = self._limpar_resposta_completa(str(response), cidade, bairro)
                
                if texto_limpo and len(texto_limpo) > 50:
                    self.cache[cache_key] = texto_limpo
                    print("✅ Informações reais obtidas e limpas com sucesso!")
                    return texto_limpo
                else:
                    print("⚠️ Resposta muito curta, usando texto padrão")
                    return self._gerar_texto_padrao_fallback(cidade, bairro)
            else:
                print("⚠️ Resposta vazia, usando texto padrão")
                return self._gerar_texto_padrao_fallback(cidade, bairro)
                
        except Exception as e:
            print(f"❌ Erro na pesquisa real: {e}")
            return self._gerar_texto_padrao_fallback(cidade, bairro)
    
    def _limpar_resposta_completa(self, texto, cidade, bairro):
        """Limpa completamente a resposta do Tavily"""
        if not texto:
            return ""
        
        # Limpeza básica
        texto = str(texto)
        
        # Remover caracteres de escape e formatação
        texto = texto.replace('\\n', ' ')
        texto = texto.replace('\n', ' ')
        texto = texto.replace('\\"', '"')
        texto = texto.replace('\\', ' ')
        
        # Remover formatação markdown
        texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)  # **texto** -> texto
        texto = re.sub(r'\*([^*]+)\*', r'\1', texto)      # *texto* -> texto
        texto = re.sub(r'###?\s*', '', texto)             # ### -> vazio
        texto = re.sub(r'##\s*', '', texto)               # ## -> vazio
        texto = re.sub(r'#\s*', '', texto)                # # -> vazio
        
        # Remover listas markdown
        texto = re.sub(r'-\s*', '• ', texto)
        texto = re.sub(r'\d+\.\s*', '• ', texto)
        
        # Remover URLs e links
        texto = re.sub(r'http[s]?://[^\s]+', '', texto)
        texto = re.sub(r'\([^)]*\.html[^)]*\)', '', texto)
        texto = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', texto)
        
        # Remover caracteres especiais desnecessários
        texto = re.sub(r'[^\w\s\.,!?•\-áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]', ' ', texto)
        
        # Limpar espaços múltiplos
        texto = re.sub(r'\s+', ' ', texto)
        texto = texto.strip()
        
        # Dividir em seções
        secoes = self._extrair_secoes_limpas(texto, cidade, bairro)
        
        # Montar texto final estruturado
        texto_final = ""
        
        if secoes['comercio']:
            texto_final += f"Comércio, Lazer e Comodidade:\n{secoes['comercio']}\n\n"
        
        if secoes['seguranca']:
            texto_final += f"Segurança:\n{secoes['seguranca']}\n\n"
        
        if secoes['potencial']:
            texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{secoes['potencial']}\n\n"
        
        # Se não conseguiu extrair seções, usar texto geral limpo
        if not texto_final.strip():
            texto_resumido = self._resumir_texto(texto, 600)
            texto_final = f"Informações sobre {bairro}, {cidade}:\n{texto_resumido}"
        
        return texto_final.strip()
    
    def _extrair_secoes_limpas(self, texto, cidade, bairro):
        """Extrai seções específicas do texto limpo"""
        secoes = {
            'comercio': '',
            'seguranca': '',
            'potencial': ''
        }
        
        texto_lower = texto.lower()
        
        # Palavras-chave para cada seção
        palavras_comercio = ['comércio', 'mercado', 'supermercado', 'padaria', 'farmácia', 'posto', 'banco', 'loja', 'shopping', 'restaurante', 'comercial']
        palavras_seguranca = ['segurança', 'criminalidade', 'violência', 'policial', 'crime', 'roubo', 'furto', 'homicídio', 'policiamento']
        palavras_potencial = ['crescimento', 'investimento', 'desenvolvimento', 'valorização', 'econômico', 'imobiliário', 'crescimento', 'expansão']
        
        # Extrair seções
        for secao, palavras in [('comercio', palavras_comercio), ('seguranca', palavras_seguranca), ('potencial', palavras_potencial)]:
            for palavra in palavras:
                if palavra in texto_lower:
                    # Buscar contexto ao redor da palavra
                    inicio = texto_lower.find(palavra)
                    if inicio != -1:
                        # Pegar contexto maior para ter mais informações
                        inicio_contexto = max(0, inicio - 150)
                        fim_contexto = min(len(texto), inicio + 400)
                        contexto = texto[inicio_contexto:fim_contexto]
                        
                        # Limpar o contexto
                        contexto_limpo = self._limpar_contexto(contexto)
                        if contexto_limpo and len(contexto_limpo) > 30:
                            secoes[secao] += contexto_limpo + " "
        
        # Limpar e limitar tamanho das seções
        for key in secoes:
            secoes[key] = secoes[key].strip()
            # Remover repetições
            secoes[key] = self._remover_repeticoes(secoes[key])
            # Limitar tamanho
            if len(secoes[key]) > 350:
                secoes[key] = secoes[key][:350] + "..."
        
        return secoes
    
    def _limpar_contexto(self, contexto):
        """Limpa um contexto específico"""
        if not contexto:
            return ""
        
        # Limpeza básica
        contexto = contexto.strip()
        contexto = re.sub(r'\s+', ' ', contexto)
        
        # Capitalizar primeira letra
        if contexto:
            contexto = contexto[0].upper() + contexto[1:]
        
        # Adicionar ponto final se necessário
        if contexto and not contexto.endswith(('.', '!', '?')):
            contexto += "."
        
        return contexto
    
    def _remover_repeticoes(self, texto):
        """Remove repetições excessivas no texto"""
        if not texto:
            return ""
        
        palavras = texto.split()
        texto_limpo = []
        palavras_anteriores = set()
        
        for palavra in palavras:
            palavra_limpa = palavra.lower().strip('.,!?')
            if palavra_limpa not in palavras_anteriores or len(palavras_anteriores) > 20:
                texto_limpo.append(palavra)
                palavras_anteriores.add(palavra_limpa)
                if len(palavras_anteriores) > 50:  # Resetar a cada 50 palavras
                    palavras_anteriores.clear()
        
        return ' '.join(texto_limpo)
    
    def _resumir_texto(self, texto, max_chars):
        """Resume o texto para o tamanho máximo especificado"""
        if len(texto) <= max_chars:
            return texto
        
        # Tentar quebrar em frase completa
        texto_resumido = texto[:max_chars]
        ultimo_ponto = texto_resumido.rfind('.')
        
        if ultimo_ponto > max_chars * 0.7:  # Se encontrou ponto em pelo menos 70% do texto
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
    """Teste da versão limpa"""
    print("🚀 TESTE DA PESQUISA LIMPA")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeLimpa()
    
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
        print("\n✅ Resultado LIMPO:")
        print("=" * 50)
        print(texto)
        print("=" * 50)
    else:
        print("\n⚠️ Nenhuma informação encontrada")

if __name__ == "__main__":
    main()
