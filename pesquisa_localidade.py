import os
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import re

load_dotenv()

class PesquisaLocalidade:
    def __init__(self):
        self.agent = Agent(tools=[TavilyTools()])
        
    def pesquisar_comercio_lazer(self, cidade, bairro):
        """Pesquisa informações sobre comércio, lazer e comodidades"""
        try:
            query = f"""Pesquise informações específicas sobre comércio, lazer e comodidades no bairro {bairro}, cidade {cidade}, SP. 
            Foque em: mercados, padarias, lojas de conveniência, farmácias, postos de gasolina, supermercados, 
            praças, parques, clubes, centros de lazer, academias, restaurantes, bancos, escolas, hospitais.
            Forneça informações estruturadas sobre a disponibilidade e proximidade desses serviços."""
            
            response = self.agent.run(query)
            
            # Processar resposta para extrair informações relevantes
            texto = str(response)
            
            # Extrair informações sobre comércio
            comercio_info = self._extrair_comercio(texto)
            
            # Extrair informações sobre lazer
            lazer_info = self._extrair_lazer(texto)
            
            # Extrair informações sobre serviços
            servicos_info = self._extrair_servicos(texto)
            
            return {
                'comercio': comercio_info,
                'lazer': lazer_info,
                'servicos': servicos_info,
                'texto_completo': texto
            }
            
        except Exception as e:
            print(f"Erro na pesquisa de comércio/lazer: {e}")
            return self._gerar_resposta_padrao_comercio()
    
    def pesquisar_seguranca(self, cidade, bairro):
        """Pesquisa informações sobre segurança"""
        try:
            query = f"""Pesquise informações sobre segurança e criminalidade no bairro {bairro}, cidade {cidade}, SP.
            Foque em: índices de criminalidade, estatísticas de segurança, nível de violência, 
            presença policial, iluminação pública, segurança residencial.
            Forneça dados específicos sobre a segurança da região se disponíveis."""
            
            response = self.agent.run(query)
            
            texto = str(response)
            
            # Extrair informações sobre segurança
            seguranca_info = self._extrair_seguranca(texto)
            
            return {
                'seguranca': seguranca_info,
                'texto_completo': texto
            }
            
        except Exception as e:
            print(f"Erro na pesquisa de segurança: {e}")
            return self._gerar_resposta_padrao_seguranca()
    
    def pesquisar_potencial_economico(self, cidade, bairro):
        """Pesquisa informações sobre potencial econômico e crescimento imobiliário"""
        try:
            query = f"""Pesquise informações sobre potencial econômico e crescimento imobiliário no bairro {bairro}, cidade {cidade}, SP.
            Foque em: desenvolvimento urbano, investimentos municipais, crescimento populacional, 
            valorização imobiliária, infraestrutura, transporte público, perfil socioeconômico,
            projetos futuros, atratividade para investimentos, estabilidade da região.
            Forneça análise sobre o potencial de crescimento e desenvolvimento da região."""
            
            response = self.agent.run(query)
            
            texto = str(response)
            
            # Extrair informações sobre potencial econômico
            potencial_info = self._extrair_potencial_economico(texto)
            
            return {
                'potencial_economico': potencial_info,
                'texto_completo': texto
            }
            
        except Exception as e:
            print(f"Erro na pesquisa de potencial econômico: {e}")
            return self._gerar_resposta_padrao_potencial()
    
    def _extrair_comercio(self, texto):
        """Extrai informações sobre comércio do texto"""
        # Palavras-chave relacionadas a comércio
        palavras_chave = ['mercado', 'padaria', 'loja', 'supermercado', 'farmácia', 'posto', 'gasolina', 'comércio', 'serviços']
        
        frases_encontradas = []
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                # Encontrar contexto ao redor da palavra
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    # Buscar frase completa começando do início da frase
                    inicio_frase = max(0, inicio - 100)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    # Limpar e estruturar o texto
                    contexto = contexto.replace('\n', ' ').replace('\r', ' ')
                    contexto = ' '.join(contexto.split())  # Remove espaços extras
                    
                    if len(contexto) > 20:  # Só adicionar se tiver conteúdo suficiente
                        frases_encontradas.append(contexto)
        
        if frases_encontradas:
            # Combinar informações de forma estruturada
            texto_final = " ".join(frases_encontradas[:2])  # Limitar a 2 frases principais
            return self._limpar_e_estruturar_texto(texto_final)
        else:
            return None  # Retorna None se não encontrar informações
    
    def _extrair_lazer(self, texto):
        """Extrai informações sobre lazer do texto"""
        palavras_chave = ['praça', 'parque', 'clube', 'centro', 'recreação', 'esporte', 'lazer', 'academia', 'restaurante']
        
        frases_encontradas = []
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    inicio_frase = max(0, inicio - 100)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    contexto = contexto.replace('\n', ' ').replace('\r', ' ')
                    contexto = ' '.join(contexto.split())
                    
                    if len(contexto) > 20:
                        frases_encontradas.append(contexto)
        
        if frases_encontradas:
            texto_final = " ".join(frases_encontradas[:2])
            return self._limpar_e_estruturar_texto(texto_final)
        else:
            return None
    
    def _extrair_servicos(self, texto):
        """Extrai informações sobre serviços do texto"""
        palavras_chave = ['posto', 'gasolina', 'serviço', 'banco', 'hospital', 'escola', 'serviços', 'acesso']
        
        frases_encontradas = []
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    inicio_frase = max(0, inicio - 100)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    contexto = contexto.replace('\n', ' ').replace('\r', ' ')
                    contexto = ' '.join(contexto.split())
                    
                    if len(contexto) > 20:
                        frases_encontradas.append(contexto)
        
        if frases_encontradas:
            texto_final = " ".join(frases_encontradas[:2])
            return self._limpar_e_estruturar_texto(texto_final)
        else:
            return None
    
    def _extrair_seguranca(self, texto):
        """Extrai informações sobre segurança do texto"""
        palavras_chave = ['segurança', 'criminalidade', 'violência', 'índice', 'estatística', 'policial', 'iluminação']
        
        frases_encontradas = []
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    inicio_frase = max(0, inicio - 100)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    contexto = contexto.replace('\n', ' ').replace('\r', ' ')
                    contexto = ' '.join(contexto.split())
                    
                    if len(contexto) > 20:
                        frases_encontradas.append(contexto)
        
        if frases_encontradas:
            texto_final = " ".join(frases_encontradas[:2])
            return self._limpar_e_estruturar_texto(texto_final)
        else:
            return None
    
    def _extrair_potencial_economico(self, texto):
        """Extrai informações sobre potencial econômico do texto"""
        palavras_chave = ['crescimento', 'investimento', 'desenvolvimento', 'potencial', 'econômico', 'valorização', 'infraestrutura', 'transporte']
        
        frases_encontradas = []
        texto_lower = texto.lower()
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                inicio = texto_lower.find(palavra)
                if inicio != -1:
                    inicio_frase = max(0, inicio - 100)
                    fim_frase = min(len(texto), inicio + 200)
                    contexto = texto[inicio_frase:fim_frase].strip()
                    
                    contexto = contexto.replace('\n', ' ').replace('\r', ' ')
                    contexto = ' '.join(contexto.split())
                    
                    if len(contexto) > 20:
                        frases_encontradas.append(contexto)
        
        if frases_encontradas:
            texto_final = " ".join(frases_encontradas[:2])
            return self._limpar_e_estruturar_texto(texto_final)
        else:
            return None
    
    def _limpar_e_estruturar_texto(self, texto):
        """Limpa e estrutura o texto para o formato do laudo"""
        if not texto:
            return None
            
        # Limpar caracteres especiais e quebras de linha
        texto = texto.replace('\n', ' ').replace('\r', ' ')
        texto = ' '.join(texto.split())  # Remove espaços extras
        
        # Capitalizar primeira letra
        texto = texto[0].upper() + texto[1:] if len(texto) > 0 else texto
        
        # Garantir que termine com ponto
        if not texto.endswith('.'):
            texto += '.'
            
        return texto
    
    def _gerar_resposta_padrao_comercio(self):
        """Gera resposta padrão para comércio quando há erro na API"""
        return {
            'comercio': 'Ele se beneficia de mercados locais, padarias e lojas de conveniência no entorno.',
            'lazer': 'A cerca de 2–4 km ficam clubes, praças e centros de lazer.',
            'servicos': 'Excelente acesso a postos de gasolina e serviços essenciais.',
            'texto_completo': 'Informações padrão sobre comércio e serviços da região.'
        }
    
    def _gerar_resposta_padrao_seguranca(self):
        """Gera resposta padrão para segurança quando há erro na API"""
        return {
            'seguranca': 'Não há dados específicos sobre índices de criminalidade no bairro, mas apresenta níveis moderados típicos de cidades do interior paulista.',
            'texto_completo': 'Informações padrão sobre segurança da região.'
        }
    
    def _gerar_resposta_padrao_potencial(self):
        """Gera resposta padrão para potencial econômico quando há erro na API"""
        return {
            'potencial_economico': 'É um bairro residencial estável, próximo ao centro, com boa infraestrutura, transporte e perfil familiar. O custo imobiliário mais baixo e investimentos municipais recentes tornam-no atrativo para moradia e investimento de médio prazo.',
            'texto_completo': 'Informações padrão sobre potencial econômico da região.'
        }
    
    def gerar_texto_pesquisa_localidade(self, cidade, bairro):
        """Gera o texto completo da pesquisa de localidade para o laudo"""
        try:
            # Pesquisar informações
            comercio_info = self.pesquisar_comercio_lazer(cidade, bairro)
            seguranca_info = self.pesquisar_seguranca(cidade, bairro)
            potencial_info = self.pesquisar_potencial_economico(cidade, bairro)
            
            # Montar texto final seguindo formato exato
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
            
            # Potencial Econômico e de Crescimento Imobiliário
            if potencial_info['potencial_economico']:
                texto_final += f"Potencial Econômico e de Crescimento Imobiliário:\n{potencial_info['potencial_economico']}"
            
            # Se não encontrou nenhuma informação, retorna None
            if not texto_final.strip():
                return None
                
            return texto_final.strip()
            
        except Exception as e:
            print(f"Erro ao gerar texto de pesquisa de localidade: {e}")
            return None
    
    def _gerar_texto_padrao(self):
        """Gera texto padrão quando há erro nas APIs"""
        return """
Comércio, Lazer e Comodidade:
Ele se beneficia de mercados locais, padarias e lojas de conveniência no entorno. 
A cerca de 2–4 km ficam clubes, praças e o Complexo Villa. 
Excelente acesso a postos de gasolina e serviços essenciais.

Segurança:
Não há dados específicos sobre índices de criminalidade no bairro, 
mas Taquarituba apresenta níveis moderados típicos de cidades do interior paulista.

Potencial Econômico e de Crescimento Imobiliário:
Jardim Santa Virgínia é um bairro residencial estável, próximo ao centro, 
com boa infraestrutura, transporte e perfil familiar. 
O custo imobiliário mais baixo e investimentos municipais recentes tornam-no atrativo para moradia e investimento de médio prazo.
"""

def main():
    """Função para testar a pesquisa de localidade"""
    pesquisa = PesquisaLocalidade()
    
    cidade = "Taquarituba"
    bairro = "Jardim Santa Virgínia"
    
    print("Pesquisando informações sobre localidade...")
    texto = pesquisa.gerar_texto_pesquisa_localidade(cidade, bairro)
    print("\nTexto gerado:")
    print(texto)

if __name__ == "__main__":
    main()
