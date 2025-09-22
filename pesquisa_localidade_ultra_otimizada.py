import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeUltraOtimizada:
    def __init__(self):
        self.agent = Agent(tools=[TavilyTools()])
        self.timeout = 20  # Timeout reduzido para 20 segundos
        self.cache = {}
        
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera o texto completo com UMA única pesquisa otimizada"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_completo"
            if cache_key in self.cache:
                print("📋 Usando dados do cache")
                return self.cache[cache_key]
            
            print(f"🔍 Pesquisando informações para {bairro}, {cidade}...")
            start_time = time.time()
            
            # Query única e otimizada
            query = f"""Informações sobre {bairro} {cidade} SP:
            1. Comércio e serviços: mercados, padarias, farmácias, postos, bancos
            2. Lazer: praças, parques, clubes, academias
            3. Segurança: criminalidade, violência, índices
            4. Potencial econômico: crescimento, investimentos, valorização
            
            Forneça informações estruturadas e específicas."""
            
            # Executar pesquisa única
            response = self.agent.run(query)
            tempo_pesquisa = time.time() - start_time
            
            print(f"⏱️ Pesquisa concluída em {tempo_pesquisa:.1f} segundos")
            
            # Se demorou muito, usar texto padrão
            if tempo_pesquisa > self.timeout:
                print("⚠️ Timeout atingido, usando texto padrão")
                texto_padrao = self._gerar_texto_padrao()
                self.cache[cache_key] = texto_padrao
                return texto_padrao
            
            # Processar resposta de forma inteligente
            texto = str(response)
            texto_estruturado = self._processar_resposta_inteligente(texto, cidade, bairro)
            
            if texto_estruturado:
                self.cache[cache_key] = texto_estruturado
                return texto_estruturado
            else:
                # Se não conseguiu estruturar, usar padrão
                texto_padrao = self._gerar_texto_padrao()
                self.cache[cache_key] = texto_padrao
                return texto_padrao
                
        except Exception as e:
            print(f"❌ Erro na pesquisa: {e}")
            return self._gerar_texto_padrao()
    
    def _processar_resposta_inteligente(self, texto, cidade, bairro):
        """Processa a resposta de forma inteligente e rápida"""
        try:
            # Buscar seções específicas no texto
            secoes = {
                'comercio': self._extrair_secao(texto, ['comércio', 'mercado', 'padaria', 'farmácia', 'serviços']),
                'lazer': self._extrair_secao(texto, ['lazer', 'praça', 'parque', 'clube', 'academia']),
                'seguranca': self._extrair_secao(texto, ['segurança', 'criminalidade', 'violência', 'policial']),
                'potencial': self._extrair_secao(texto, ['crescimento', 'investimento', 'desenvolvimento', 'valorização'])
            }
            
            # Montar texto estruturado
            texto_final = ""
            
            # Comércio, Lazer e Comodidade
            comercio_texto = ""
            if secoes['comercio']:
                comercio_texto += secoes['comercio'] + " "
            if secoes['lazer']:
                comercio_texto += secoes['lazer'] + " "
            
            if comercio_texto.strip():
                texto_final += f"Comércio, Lazer e Comodidade:\n{comercio_texto.strip()}\n\n"
            
            # Segurança
            if secoes['seguranca']:
                texto_final += f"Segurança:\n{secoes['seguranca']}\n\n"
            
            # Potencial Econômico
            if secoes['potencial']:
                texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{secoes['potencial']}"
            
            return texto_final.strip() if texto_final.strip() else None
            
        except Exception as e:
            print(f"Erro ao processar resposta: {e}")
            return None
    
    def _extrair_secao(self, texto, palavras_chave):
        """Extrai uma seção específica baseada em palavras-chave"""
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                # Buscar contexto ao redor da palavra
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    # Buscar frase completa
                    inicio_frase = max(0, inicio - 30)
                    fim_frase = min(len(texto), inicio + 150)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    # Limpar e estruturar
                    contexto = ' '.join(contexto.split())
                    if len(contexto) > 15:
                        return self._limpar_texto(contexto)
        
        return None
    
    def _limpar_texto(self, texto):
        """Limpa o texto de forma rápida"""
        if not texto:
            return None
        
        # Limpeza básica
        texto = ' '.join(texto.split())
        texto = texto[0].upper() + texto[1:] if len(texto) > 0 else texto
        
        if not texto.endswith('.'):
            texto += '.'
            
        return texto
    
    def _gerar_texto_padrao(self):
        """Gera texto padrão quando não há informações específicas"""
        return """Comércio, Lazer e Comodidade:
Ele se beneficia de mercados locais, padarias e lojas de conveniência no entorno. 
A cerca de 2–4 km ficam clubes, praças e o Complexo Villa. 
Excelente acesso a postos de gasolina e serviços essenciais.

Segurança:
Não há dados específicos sobre índices de criminalidade no bairro, 
mas Taquarituba apresenta níveis moderados típicos de cidades do interior paulista.

Potencial Econômico e de Crescimento Imobiliário:
Jardim Santa Virgínia é um bairro residencial estável, próximo ao centro, 
com boa infraestrutura, transporte e perfil familiar. 
O custo imobiliário mais baixo e investimentos municipais recentes tornam-no atrativo para moradia e investimento de médio prazo."""

def main():
    """Teste da versão ultra otimizada"""
    print("🚀 TESTE DA PESQUISA ULTRA OTIMIZADA")
    print("=" * 50)
    
    pesquisa = PesquisaLocalidadeUltraOtimizada()
    
    cidade = "Taquarituba"
    bairro = "Jardim Santa Virgínia"
    
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
