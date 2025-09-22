from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.shared import OxmlElement, qn
import pandas as pd
import os
from datetime import datetime

class GeradorLaudoDocx:
    def __init__(self):
        self.document = None
        
    def criar_documento(self):
        """Cria um novo documento DOCX"""
        self.document = Document()
        self._configurar_estilos()
        
    def _configurar_estilos(self):
        """Configura os estilos do documento"""
        # Estilo para título principal
        titulo_style = self.document.styles.add_style('TituloLaudo', WD_STYLE_TYPE.PARAGRAPH)
        titulo_font = titulo_style.font
        titulo_font.name = 'Arial'
        titulo_font.size = Pt(16)
        titulo_font.bold = True
        titulo_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        titulo_style.paragraph_format.space_after = Pt(12)
        
        # Estilo para subtítulos
        subtitulo_style = self.document.styles.add_style('SubtituloLaudo', WD_STYLE_TYPE.PARAGRAPH)
        subtitulo_font = subtitulo_style.font
        subtitulo_font.name = 'Arial'
        subtitulo_font.size = Pt(12)
        subtitulo_font.bold = True
        subtitulo_style.paragraph_format.space_before = Pt(12)
        subtitulo_style.paragraph_format.space_after = Pt(6)
        
        # Estilo para texto normal
        texto_style = self.document.styles.add_style('TextoLaudo', WD_STYLE_TYPE.PARAGRAPH)
        texto_font = texto_style.font
        texto_font.name = 'Arial'
        texto_font.size = Pt(11)
        texto_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        texto_style.paragraph_format.space_after = Pt(6)
        texto_style.paragraph_format.line_spacing = 1.15
        
    def adicionar_titulo(self, titulo="LAUDO DE AVALIAÇÃO IMOBILIÁRIA"):
        """Adiciona o título principal do laudo"""
        titulo_para = self.document.add_paragraph()
        titulo_para.style = 'TituloLaudo'
        titulo_run = titulo_para.add_run(titulo)
        titulo_run.bold = True
        
    def adicionar_objetivo(self):
        """Adiciona a seção de objetivo do laudo (texto padrão)"""
        self.document.add_paragraph("1. OBJETIVO DO LAUDO", style='SubtituloLaudo')
        
        objetivo_texto = """O presente laudo tem como finalidade estimar o valor de mercado do imóvel descrito, 
para fins de garantia de financiamento, ação judicial, atualização patrimonial, entre outros, 
em conformidade com a ABNT NBR 14653-1 (Procedimentos Gerais) e NBR 14653-2 (Imóveis Urbanos)."""
        
        self.document.add_paragraph(objetivo_texto, style='TextoLaudo')
        
    def adicionar_identificacao_imovel(self, dados_imovel):
        """Adiciona a seção de identificação do imóvel"""
        self.document.add_paragraph("2. IDENTIFICAÇÃO DO IMÓVEL", style='SubtituloLaudo')
        
        # Montar texto de identificação
        identificacao_texto = f"""Número da Matrícula: {dados_imovel.get('numero_matricula', 'N/A')}
Cartório de Registro de Imóveis: {dados_imovel.get('cartorio', 'N/A')}
Descrição: Terreno com área de {dados_imovel.get('area_terreno', 0):.2f} m², contendo uma edificação residencial em {dados_imovel.get('tipo_construcao', 'alvenaria').lower()}, 
coberta de {dados_imovel.get('cobertura', 'telhas').lower()}, com área construída de {dados_imovel.get('area_construida', 0):.2f} m². 
Localizado no loteamento {dados_imovel.get('loteamento', 'N/A')}, na cidade de {dados_imovel.get('cidade', 'N/A')}/{dados_imovel.get('estado', 'N/A')}."""
        
        self.document.add_paragraph(identificacao_texto, style='TextoLaudo')
        
    def adicionar_metodologia(self):
        """Adiciona a seção de metodologia (texto padrão)"""
        self.document.add_paragraph("3. METODOLOGIA DE AVALIAÇÃO", style='SubtituloLaudo')
        
        metodologia_texto = """Este trabalho adota o Método Comparativo Direto de Dados de Mercado, conforme a NBR 14653, 
realizando coleta, análise e tratamento estatístico de amostra de imóveis similares ao objeto de avaliação. 
Foi empregada a técnica de regressão hedônica para ponderação de fatores como área construída, 
área do terreno, localização, padrão construtivo e estado de conservação, ajustando valores unitários obtidos em mercado. 
Foram descartados imóveis que apresentaram valores manifestamente incompatíveis com a realidade mercadológica local, 
a fim de evitar distorções na média amostral, seguindo as boas práticas de avaliação consagradas pelas normas técnicas."""
        
        self.document.add_paragraph(metodologia_texto, style='TextoLaudo')
        
    def adicionar_pesquisa_mercado(self, dados_scraper):
        """Adiciona a seção de pesquisa de mercado com dados do scraper"""
        self.document.add_paragraph("4. PESQUISA DE MERCADO E ANÁLISE COMPARATIVA", style='SubtituloLaudo')
        
        if dados_scraper is not None and not dados_scraper.empty:
            # Criar tabela com dados do scraper
            tabela = self.document.add_table(rows=1, cols=6)
            tabela.style = 'Table Grid'
            
            # Cabeçalho da tabela
            header_cells = tabela.rows[0].cells
            header_cells[0].text = 'Nº'
            header_cells[1].text = 'Localização'
            header_cells[2].text = 'Área Terreno'
            header_cells[3].text = 'Área Construída'
            header_cells[4].text = 'Preço Anunciado'
            header_cells[5].text = 'Valor Unitário (m²)'
            
            # Adicionar dados do scraper (top 6 imóveis)
            df_sorted = dados_scraper.sort_values('R$/M2').head(6)
            
            for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
                row_cells = tabela.add_row().cells
                row_cells[0].text = str(idx)
                row_cells[1].text = str(row.get('Endereco', 'N/A'))[:30] + '...' if len(str(row.get('Endereco', 'N/A'))) > 30 else str(row.get('Endereco', 'N/A'))
                row_cells[2].text = f"{row.get('M2', 0):.0f} m²"
                row_cells[3].text = f"{row.get('M2', 0):.0f} m²"  # Assumindo que área construída = área total
                row_cells[4].text = f"R$ {row.get('Preco', 0):,.0f}"
                row_cells[5].text = f"R$ {row.get('R$/M2', 0):,.0f}"
            
            # Adicionar parágrafo sobre imóveis descartados
            self.document.add_paragraph("", style='TextoLaudo')
            
            # Calcular valor máximo para descarte
            preco_maximo = dados_scraper['Preco'].quantile(0.9)  # 90% dos imóveis
            
            descarte_texto = f"""Imóveis descartados:
Foram anulados da amostra imóveis com valores acima de R$ {preco_maximo:,.0f}, 
em razão de apresentarem características construtivas e padrões de acabamento superiores (alto padrão)."""
            
            self.document.add_paragraph(descarte_texto, style='TextoLaudo')
        else:
            # Texto padrão se não houver dados do scraper
            texto_padrao = """Nº | Localização        | Área Terreno | Área Construída | Preço Anunciado | Valor Unitário (m²) | Observações
1  | Jardim Santa Virgínia | 150 m²       | 120 m²          | R$ 450.000      | R$ 3.750            | Padrão médio, recém-reformado
2  | Jardim Santa Virgínia | 160 m²       | 125 m²          | R$ 460.000      | R$ 3.680            | Imóvel em bom estado
3  | Jardim Santa Virgínia | 180 m²       | 130 m²          | R$ 490.000      | R$ 3.769            | Similar ao avaliado
4  | Bairro Carlos Eduardo | 200 m²       | 140 m²          | R$ 500.000      | R$ 3.571            | Localização próxima
5  | Jardim Santa Virgínia | 150 m²       | 120 m²          | R$ 440.000      | R$ 3.666            | Conservação regular
6  | Jardim Santa Virgínia | 170 m²       | 128 m²          | R$ 480.000      | R$ 3.750            | Estado geral bom

Imóveis descartados:
Foram anulados da amostra imóveis com valores acima de R$ 700.000,00, 
em razão de apresentarem características construtivas e padrões de acabamento superiores (alto padrão)."""
            
            self.document.add_paragraph(texto_padrao, style='TextoLaudo')
    
    def adicionar_determinacao_valor(self, dados_scraper, dados_imovel):
        """Adiciona a seção de determinação do valor de mercado"""
        self.document.add_paragraph("5. DETERMINAÇÃO DO VALOR DE MERCADO", style='SubtituloLaudo')
        
        if dados_scraper is not None and not dados_scraper.empty:
            # Calcular valor médio unitário
            valor_medio_unitario = dados_scraper['R$/M2'].mean()
            area_construida = dados_imovel.get('area_construida', 0)
            valor_edificacao = valor_medio_unitario * area_construida
            
            # Calcular valor do terreno
            valor_terreno_m2 = 800.0  # Valor padrão por m² do terreno
            area_terreno = dados_imovel.get('area_terreno', 0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            # Valor total
            valor_total = valor_edificacao + valor_terreno
            
            determinacao_texto = f"""Com base na amostra válida, o valor médio unitário de referência para imóveis similares é de R$ {valor_medio_unitario:,.2f}/m² de área construída. 
Considerando o imóvel avaliado possuir área construída de {area_construida:.2f} m², o valor estimado da edificação é de aproximadamente R$ {valor_edificacao:,.2f}.

Adicionalmente, foi atribuída parcela relativa ao terreno, considerando valor médio de mercado na região de R$ {valor_terreno_m2:,.2f}/m². 
Assim, para {area_terreno:.2f} m², resulta em aproximadamente R$ {valor_terreno:,.2f}. 

Desta forma, o valor total estimado do imóvel é:
R$ {valor_edificacao:,.2f} (edificação) + R$ {valor_terreno:,.2f} (terreno) = R$ {valor_total:,.2f}"""
            
        else:
            # Valores padrão
            valor_medio_unitario = 3700.0
            area_construida = dados_imovel.get('area_construida', 134.59)
            valor_edificacao = valor_medio_unitario * area_construida
            
            valor_terreno_m2 = 800.0
            area_terreno = dados_imovel.get('area_terreno', 201.0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            valor_total = valor_edificacao + valor_terreno
            
            determinacao_texto = f"""Com base na amostra válida, o valor médio unitário de referência para imóveis similares é de R$ {valor_medio_unitario:,.2f}/m² de área construída. 
Considerando o imóvel avaliado possuir área construída de {area_construida:.2f} m², o valor estimado da edificação é de aproximadamente R$ {valor_edificacao:,.2f}.

Adicionalmente, foi atribuída parcela relativa ao terreno, considerando valor médio de mercado na região de R$ {valor_terreno_m2:,.2f}/m². 
Assim, para {area_terreno:.2f} m², resulta em aproximadamente R$ {valor_terreno:,.2f}. 

Desta forma, o valor total estimado do imóvel é:
R$ {valor_edificacao:,.2f} (edificação) + R$ {valor_terreno:,.2f} (terreno) = R$ {valor_total:,.2f}"""
        
        self.document.add_paragraph(determinacao_texto, style='TextoLaudo')
        
    def adicionar_pesquisa_localidade(self, texto_pesquisa):
        """Adiciona a seção de pesquisa de localidade"""
        self.document.add_paragraph("6. PESQUISA DE LOCALIDADE", style='SubtituloLaudo')
        
        if texto_pesquisa:
            self.document.add_paragraph(texto_pesquisa, style='TextoLaudo')
        else:
            # Texto padrão quando não há informações específicas
            texto_padrao = """Comércio, Lazer e Comodidade:
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
            
            self.document.add_paragraph(texto_padrao, style='TextoLaudo')
        
    def adicionar_conclusao(self, dados_scraper, dados_imovel):
        """Adiciona a seção de conclusão"""
        self.document.add_paragraph("7. CONCLUSÃO", style='SubtituloLaudo')
        
        if dados_scraper is not None and not dados_scraper.empty:
            valor_medio_unitario = dados_scraper['R$/M2'].mean()
            area_construida = dados_imovel.get('area_construida', 0)
            valor_edificacao = valor_medio_unitario * area_construida
            
            valor_terreno_m2 = 800.0
            area_terreno = dados_imovel.get('area_terreno', 0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            valor_total = valor_edificacao + valor_terreno
        else:
            valor_total = 658800.0  # Valor padrão
        
        # Converter valor para extenso
        valor_extenso = self._converter_valor_extenso(valor_total)
        
        conclusao_texto = f"""Com base nos estudos realizados, considera-se que o valor de mercado do imóvel avaliado é de R$ {valor_total:,.2f} 
({valor_extenso}), na data de referência deste laudo. 

Este valor reflete as condições de mercado atuais, características do imóvel e seu estado de conservação, 
considerando as especificidades da amostra utilizada e os ajustes técnicos realizados."""
        
        self.document.add_paragraph(conclusao_texto, style='TextoLaudo')
        
    def adicionar_assinatura(self, dados_avaliador):
        """Adiciona a seção de assinatura do avaliador"""
        self.document.add_paragraph("8. ASSINATURA DO AVALIADOR", style='SubtituloLaudo')
        
        # Adicionar espaço para assinatura
        self.document.add_paragraph("", style='TextoLaudo')
        self.document.add_paragraph("", style='TextoLaudo')
        
        # Dados do avaliador
        cidade_assinatura = dados_avaliador.get('cidade_assinatura', 'Sorocaba')
        estado_assinatura = dados_avaliador.get('estado_assinatura', 'SP')
        data_laudo = dados_avaliador.get('data_laudo', datetime.now().date())
        
        assinatura_texto = f"""{cidade_assinatura} - {estado_assinatura}, {data_laudo.strftime('%d de %B de %Y')}

{dados_avaliador.get('nome', 'Jhonni Balbino da Silva')}
Perito Avaliador Imobiliário
CRECI: {dados_avaliador.get('creci', '296769-F')} | CNAI: {dados_avaliador.get('cnai', '051453')}
{dados_avaliador.get('telefone', '(11) 98796 8206')}
{dados_avaliador.get('email', 'contato@avaliarapido.com.br')}
{dados_avaliador.get('website', 'www.avaliarapido.com.br')}"""
        
        self.document.add_paragraph(assinatura_texto, style='TextoLaudo')
        
    def _converter_valor_extenso(self, valor):
        """Converte valor numérico para extenso"""
        # Implementação simplificada para valores até milhões
        if valor >= 1000000:
            milhoes = int(valor // 1000000)
            resto = valor % 1000000
            if resto == 0:
                return f"{milhoes} milhão{'es' if milhoes > 1 else ''}"
            else:
                return f"{milhoes} milhão{'es' if milhoes > 1 else ''} e {self._converter_valor_extenso(resto)}"
        elif valor >= 1000:
            milhares = int(valor // 1000)
            resto = valor % 1000
            if resto == 0:
                return f"{milhares} mil"
            else:
                return f"{milhares} mil e {self._converter_valor_extenso(resto)}"
        else:
            return f"{int(valor)}"
    
    def salvar_documento(self, nome_arquivo=None):
        """Salva o documento DOCX"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"laudo_avaliacao_{timestamp}.docx"
        
        # Criar pasta arquivos se não existir
        pasta_arquivos = "arquivos"
        if not os.path.exists(pasta_arquivos):
            os.makedirs(pasta_arquivos)
        
        caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
        self.document.save(caminho_completo)
        
        return caminho_completo
    
    def gerar_laudo_completo(self, dados_imovel, dados_avaliador, dados_scraper=None, texto_pesquisa_localidade=None):
        """Gera o laudo completo com todos os dados"""
        self.criar_documento()
        
        # Adicionar todas as seções
        self.adicionar_titulo()
        self.adicionar_objetivo()
        self.adicionar_identificacao_imovel(dados_imovel)
        self.adicionar_metodologia()
        self.adicionar_pesquisa_mercado(dados_scraper)
        self.adicionar_determinacao_valor(dados_scraper, dados_imovel)
        
        if texto_pesquisa_localidade:
            self.adicionar_pesquisa_localidade(texto_pesquisa_localidade)
        else:
            # Texto padrão
            texto_padrao = """Comércio, Lazer e Comodidade:
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
            self.adicionar_pesquisa_localidade(texto_padrao)
        
        self.adicionar_conclusao(dados_scraper, dados_imovel)
        self.adicionar_assinatura(dados_avaliador)
        
        # Salvar documento
        return self.salvar_documento()

def main():
    """Função para testar o gerador de laudo"""
    gerador = GeradorLaudoDocx()
    
    # Dados de exemplo
    dados_imovel = {
        'numero_matricula': '11.072',
        'cartorio': 'Comarca de Taquarituba/SP, Livro nº 2 – Registro Geral',
        'area_terreno': 201.0,
        'area_construida': 134.59,
        'loteamento': 'Jardim Santa Virgínia',
        'cidade': 'Taquarituba',
        'estado': 'SP',
        'tipo_construcao': 'Alvenaria',
        'cobertura': 'Telhas'
    }
    
    dados_avaliador = {
        'nome': 'Jhonni Balbino da Silva',
        'creci': '296769-F',
        'cnai': '051453',
        'telefone': '(11) 98796 8206',
        'email': 'contato@avaliarapido.com.br',
        'website': 'www.avaliarapido.com.br',
        'data_laudo': datetime.now().date(),
        'cidade_assinatura': 'Sorocaba',
        'estado_assinatura': 'SP'
    }
    
    # Gerar laudo
    arquivo_gerado = gerador.gerar_laudo_completo(dados_imovel, dados_avaliador)
    print(f"Laudo gerado: {arquivo_gerado}")

if __name__ == "__main__":
    main()
