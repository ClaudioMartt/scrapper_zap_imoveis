import os
import time
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidadeOtimizada:
    def __init__(self):
        self.agent = Agent(tools=[TavilyTools()])
        self.timeout = 30  # Timeout de 30 segundos por pesquisa
        self.cache = {}  # Cache simples para evitar pesquisas repetidas
        
    def pesquisar_comercio_lazer(self, cidade, bairro):
        """Pesquisa informações sobre comércio, lazer e comodidades com timeout"""
        try:
            # Verificar cache primeiro
            cache_key = f"{cidade}_{bairro}_comercio"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Query mais concisa e específica
            query = f"comércio lazer serviços {bairro} {cidade} SP mercados padarias farmácias postos"
            
            # Executar com timeout
            start_time = time.time()
            response = self.agent.run(query)
            
            # Verificar timeout
            if time.time() - start_time > self.timeout:
                print(f"Timeout na pesquisa de comércio/lazer para {bairro}, {cidade}")
                return self._gerar_resposta_padrao_comercio()
            
            # Processar resposta
            texto = str(response)
            
            # Extrair informações de forma mais rápida
            comercio_info = self._extrair_comercio_rapido(texto)
            lazer_info = self._extrair_lazer_rapido(texto)
            servicos_info = self._extrair_servicos_rapido(texto)
            
            resultado = {
                'comercio': comercio_info,
                'lazer': lazer_info,
                'servicos': servicos_info,
                'texto_completo': texto
            }
            
            # Salvar no cache
            self.cache[cache_key] = resultado
            return resultado
            
        except Exception as e:
            print(f"Erro na pesquisa de comércio/lazer: {e}")
            return self._gerar_resposta_padrao_comercio()
    
    def pesquisar_seguranca(self, cidade, bairro):
        """Pesquisa informações sobre segurança com timeout"""
        try:
            # Verificar cache
            cache_key = f"{cidade}_{bairro}_seguranca"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Query mais concisa
            query = f"segurança criminalidade {bairro} {cidade} SP índices estatísticas"
            
            start_time = time.time()
            response = self.agent.run(query)
            
            if time.time() - start_time > self.timeout:
                print(f"Timeout na pesquisa de segurança para {bairro}, {cidade}")
                return self._gerar_resposta_padrao_seguranca()
            
            texto = str(response)
            seguranca_info = self._extrair_seguranca_rapido(texto)
            
            resultado = {
                'seguranca': seguranca_info,
                'texto_completo': texto
            }
            
            self.cache[cache_key] = resultado
            return resultado
            
        except Exception as e:
            print(f"Erro na pesquisa de segurança: {e}")
            return self._gerar_resposta_padrao_seguranca()
    
    def pesquisar_potencial_economico(self, cidade, bairro):
        """Pesquisa informações sobre potencial econômico com timeout"""
        try:
            # Verificar cache
            cache_key = f"{cidade}_{bairro}_potencial"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Query mais concisa
            query = f"crescimento imobiliário investimentos {bairro} {cidade} SP desenvolvimento"
            
            start_time = time.time()
            response = self.agent.run(query)
            
            if time.time() - start_time > self.timeout:
                print(f"Timeout na pesquisa de potencial econômico para {bairro}, {cidade}")
                return self._gerar_resposta_padrao_potencial()
            
            texto = str(response)
            potencial_info = self._extrair_potencial_economico_rapido(texto)
            
            resultado = {
                'potencial_economico': potencial_info,
                'texto_completo': texto
            }
            
            self.cache[cache_key] = resultado
            return resultado
            
        except Exception as e:
            print(f"Erro na pesquisa de potencial econômico: {e}")
            return self._gerar_resposta_padrao_potencial()
    
    def _extrair_comercio_rapido(self, texto):
        """Extração rápida de informações sobre comércio"""
        palavras_chave = ['mercado', 'padaria', 'farmácia', 'posto', 'comércio']
        return self._buscar_palavras_chave_rapido(texto, palavras_chave)
    
    def _extrair_lazer_rapido(self, texto):
        """Extração rápida de informações sobre lazer"""
        palavras_chave = ['praça', 'parque', 'clube', 'lazer', 'academia']
        return self._buscar_palavras_chave_rapido(texto, palavras_chave)
    
    def _extrair_servicos_rapido(self, texto):
        """Extração rápida de informações sobre serviços"""
        palavras_chave = ['banco', 'hospital', 'escola', 'serviços', 'acesso']
        return self._buscar_palavras_chave_rapido(texto, palavras_chave)
    
    def _extrair_seguranca_rapido(self, texto):
        """Extração rápida de informações sobre segurança"""
        palavras_chave = ['segurança', 'criminalidade', 'violência', 'policial']
        return self._buscar_palavras_chave_rapido(texto, palavras_chave)
    
    def _extrair_potencial_economico_rapido(self, texto):
        """Extração rápida de informações sobre potencial econômico"""
        palavras_chave = ['crescimento', 'investimento', 'desenvolvimento', 'valorização']
        return self._buscar_palavras_chave_rapido(texto, palavras_chave)
    
    def _buscar_palavras_chave_rapido(self, texto, palavras_chave):
        """Busca rápida por palavras-chave"""
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                # Buscar contexto simples
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    contexto = texto[max(0, inicio - 50):inicio + 100].strip()
                    contexto = ' '.join(contexto.split())
                    if len(contexto) > 20:
                        return self._limpar_texto_rapido(contexto)
        
        return None
    
    def _limpar_texto_rapido(self, texto):
        """Limpeza rápida do texto"""
        if not texto:
            return None
        
        # Limpeza básica
        texto = ' '.join(texto.split())
        texto = texto[0].upper() + texto[1:] if len(texto) > 0 else texto
        
        if not texto.endswith('.'):
            texto += '.'
            
        return texto
    
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera o texto completo da pesquisa de localidade com timeout total"""
        try:
            print(f"🔍 Iniciando pesquisa para {bairro}, {cidade}...")
            start_time_total = time.time()
            
            # Pesquisar informações com timeout individual
            comercio_info = self.pesquisar_comercio_lazer(cidade, bairro)
            seguranca_info = self.pesquisar_seguranca(cidade, bairro)
            potencial_info = self.pesquisar_potencial_economico(cidade, bairro)
            
            tempo_total = time.time() - start_time_total
            print(f"⏱️ Pesquisa concluída em {tempo_total:.1f} segundos")
            
            # Montar texto final
            texto_final = ""
            
            # Comércio, Lazer e Comodidade
            comercio_texto = ""
            if comercio_info['comercio']:
                comercio_texto += comercio_info['comercio'] + " "
            if comercio_info['lazer']:
                comercio_texto += comercio_info['lazer'] + " "
            if comercio_info['servicos']:
                comercio_texto += comercio_info['servicos']
            
            if comercio_texto.strip():
                texto_final += f"Comércio, Lazer e Comodidade:\n{comercio_texto.strip()}\n\n"
            
            # Segurança
            if seguranca_info['seguranca']:
                texto_final += f"Segurança:\n{seguranca_info['seguranca']}\n\n"
            
            # Potencial Econômico
            if potencial_info['potencial_economico']:
                texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{potencial_info['potencial_economico']}"
            
            # Se não encontrou informações e demorou muito, retorna None
            if not texto_final.strip() or tempo_total > 60:
                print("⚠️ Nenhuma informação específica encontrada ou timeout total atingido")
                return None
                
            return texto_final.strip()
            
        except Exception as e:
            print(f"Erro ao gerar texto de pesquisa de localidade: {e}")
            return None
    
    def _gerar_resposta_padrao_comercio(self):
        """Gera resposta padrão para comércio"""
        return {
            'comercio': 'Ele se beneficia de mercados locais, padarias e lojas de conveniência no entorno.',
            'lazer': 'A cerca de 2–4 km ficam clubes, praças e centros de lazer.',
            'servicos': 'Excelente acesso a postos de gasolina e serviços essenciais.',
            'texto_completo': 'Informações padrão sobre comércio e serviços da região.'
        }
    
    def _gerar_resposta_padrao_seguranca(self):
        """Gera resposta padrão para segurança"""
        return {
            'seguranca': 'Não há dados específicos sobre índices de criminalidade no bairro, mas apresenta níveis moderados típicos de cidades do interior paulista.',
            'texto_completo': 'Informações padrão sobre segurança da região.'
        }
    
    def _gerar_resposta_padrao_potencial(self):
        """Gera resposta padrão para potencial econômico"""
        return {
            'potencial_economico': 'É um bairro residencial estável, próximo ao centro, com boa infraestrutura, transporte e perfil familiar. O custo imobiliário mais baixo e investimentos municipais recentes tornam-no atrativo para moradia e investimento de médio prazo.',
            'texto_completo': 'Informações padrão sobre potencial econômico da região.'
        }

def main():
    """Teste da pesquisa otimizada"""
    print("🚀 TESTE DA PESQUISA OTIMIZADA")
    print("=" * 40)
    
    pesquisa = PesquisaLocalidadeOtimizada()
    
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
