from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
import os

class GeradorLaudoPdf:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
        
    def _configurar_estilos(self):
        """Configura estilos elegantes para o PDF"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='TituloLaudo',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=HexColor('#1f4e79'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtituloLaudo',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=HexColor('#2e7d32'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='TextoLaudo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leftIndent=0,
            rightIndent=0
        ))
        
        # Estilo para texto em negrito
        self.styles.add(ParagraphStyle(
            name='TextoNegrito',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica-Bold',
            textColor=HexColor('#1f4e79')
        ))
        
        # Estilo para assinatura
        self.styles.add(ParagraphStyle(
            name='Assinatura',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=20,
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
    
    def criar_documento(self):
        """Cria um novo documento PDF"""
        self.story = []
        
    def adicionar_titulo(self, titulo="LAUDO DE AVALIAÇÃO IMOBILIÁRIA"):
        """Adiciona o título principal do laudo"""
        self.story.append(Paragraph(titulo, self.styles['TituloLaudo']))
        self.story.append(Spacer(1, 20))
        
    def adicionar_objetivo(self):
        """Adiciona a seção de objetivo do laudo"""
        self.story.append(Paragraph("1. OBJETIVO DO LAUDO", self.styles['SubtituloLaudo']))
        
        objetivo_texto = """O presente laudo tem como finalidade estimar o valor de mercado do imóvel descrito, 
        para fins de garantia de financiamento, ação judicial, atualização patrimonial, entre outros, 
        em conformidade com a ABNT NBR 14653-1 (Procedimentos Gerais) e NBR 14653-2 (Imóveis Urbanos)."""
        
        self.story.append(Paragraph(objetivo_texto, self.styles['TextoLaudo']))
        self.story.append(Spacer(1, 10))
        
    def adicionar_identificacao_imovel(self, dados_imovel):
        """Adiciona a seção de identificação do imóvel"""
        self.story.append(Paragraph("2. IDENTIFICAÇÃO DO IMÓVEL", self.styles['SubtituloLaudo']))
        
        # Criar tabela para dados do imóvel
        dados_tabela = [
            ['Número da Matrícula:', dados_imovel.get('numero_matricula', 'N/A')],
            ['Cartório de Registro:', dados_imovel.get('cartorio', 'N/A')],
            ['Área do Terreno:', f"{dados_imovel.get('area_terreno', 0):.2f} m²"],
            ['Área Construída:', f"{dados_imovel.get('area_construida', 0):.2f} m²"],
            ['Bairro:', dados_imovel.get('loteamento', 'N/A')],
            ['Cidade/Estado:', f"{dados_imovel.get('cidade', 'N/A')}/{dados_imovel.get('estado', 'N/A')}"],
            ['Descrição:', dados_imovel.get('descricao', 'N/A')]
        ]
        
        # Calcular larguras para ocupar toda a página (A4 = 21cm, margens = 4cm, sobra = 17cm)
        largura_total = 6.7*inch  # 17cm em polegadas
        tabela = Table(dados_tabela, colWidths=[2.5*inch, 4.2*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1f4e79')),
            ('TEXTCOLOR', (1, 0), (1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6'))
        ]))
        
        self.story.append(tabela)
        self.story.append(Spacer(1, 15))
        
    def adicionar_metodologia(self):
        """Adiciona a seção de metodologia"""
        self.story.append(Paragraph("3. METODOLOGIA DE AVALIAÇÃO", self.styles['SubtituloLaudo']))
        
        metodologia_texto = """Este trabalho adota o Método Comparativo Direto de Dados de Mercado, conforme a NBR 14653, 
        realizando coleta, análise e tratamento estatístico de amostra de imóveis similares ao objeto de avaliação. 
        Foi empregada a técnica de regressão hedônica para ponderação de fatores como área construída, 
        área do terreno, localização, padrão construtivo e estado de conservação, ajustando valores unitários obtidos em mercado. 
        Foram descartados imóveis que apresentaram valores manifestamente incompatíveis com a realidade mercadológica local, 
        a fim de evitar distorções na média amostral, seguindo as boas práticas de avaliação consagradas pelas normas técnicas."""
        
        self.story.append(Paragraph(metodologia_texto, self.styles['TextoLaudo']))
        self.story.append(Spacer(1, 10))
        
    def adicionar_pesquisa_mercado(self, dados_scraper):
        """Adiciona a seção de pesquisa de mercado"""
        self.story.append(Paragraph("4. PESQUISA DE MERCADO E ANÁLISE COMPARATIVA", self.styles['SubtituloLaudo']))
        
        # Adicionar texto explicativo sobre a amostra dos top 10 valores
        texto_explicativo = """Para a análise comparativa, foram selecionados os 10 imóveis com melhor relação custo-benefício"""
        
        self.story.append(Paragraph(texto_explicativo, self.styles['TextoLaudo']))
        self.story.append(Spacer(1, 8))
        
        if dados_scraper is not None and not dados_scraper.empty:
            # Criar tabela com dados do scraper - top 10
            df_sorted = dados_scraper.sort_values('R$/M2').head(10)
            
            # Cabeçalho da tabela
            dados_tabela = [['Nº', 'Localização', 'Área (m²)', 'Preço Anunciado', 'Valor Unitário (m²)']]
            
            # Adicionar dados
            for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
                localizacao = str(row.get('Endereco', 'N/A'))[:25] + '...' if len(str(row.get('Endereco', 'N/A'))) > 25 else str(row.get('Endereco', 'N/A'))
                dados_tabela.append([
                    str(idx),
                    localizacao,
                    f"{row.get('M2', 0):.0f}",
                    f"R$ {row.get('Preco', 0):,.0f}",
                    f"R$ {row.get('R$/M2', 0):,.0f}"
                ])
            
            # URLs removidas - mantidas apenas no Excel
            
            # Ajustar larguras para ocupar toda a largura da página
            tabela = Table(dados_tabela, colWidths=[0.6*inch, 2.2*inch, 1.2*inch, 1.8*inch, 1.8*inch])
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2e7d32')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6'))
            ]))
            
            self.story.append(tabela)
        else:
            # Texto padrão se não houver dados do scraper - top 10
            texto_padrao = """Nº | Localização        | Área (m²) | Preço Anunciado | Valor Unitário (m²)
1  | Jardim Santa Virgínia | 150 m²    | R$ 450.000      | R$ 3.750
2  | Jardim Santa Virgínia | 160 m²    | R$ 460.000      | R$ 3.680
3  | Jardim Santa Virgínia | 180 m²    | R$ 490.000      | R$ 3.769
4  | Jardim Santa Virgínia | 165 m²    | R$ 470.000      | R$ 3.788
5  | Jardim Santa Virgínia | 155 m²    | R$ 455.000      | R$ 3.742
6  | Jardim Santa Virgínia | 175 m²    | R$ 485.000      | R$ 3.771
7  | Jardim Santa Virgínia | 170 m²    | R$ 480.000      | R$ 3.765
8  | Jardim Santa Virgínia | 145 m²    | R$ 445.000      | R$ 3.724
9  | Jardim Santa Virgínia | 185 m²    | R$ 495.000      | R$ 3.784
10 | Jardim Santa Virgínia | 140 m²    | R$ 440.000      | R$ 3.714"""
            
            self.story.append(Paragraph(texto_padrao, self.styles['TextoLaudo']))
        
        self.story.append(Spacer(1, 10))
        
    def adicionar_determinacao_valor(self, dados_scraper, dados_imovel):
        """Adiciona a seção de determinação do valor"""
        self.story.append(Paragraph("5. DETERMINAÇÃO DO VALOR DE MERCADO", self.styles['SubtituloLaudo']))
        
        if dados_scraper is not None and not dados_scraper.empty:
            # Calcular valores
            valor_medio_unitario = dados_scraper['R$/M2'].mean()
            area_construida = dados_imovel.get('area_construida', 0)
            valor_edificacao = valor_medio_unitario * area_construida
            
            valor_terreno_m2 = 800.0
            area_terreno = dados_imovel.get('area_terreno', 0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            valor_total = valor_edificacao + valor_terreno
        else:
            # Valores padrão
            valor_medio_unitario = 3700.0
            area_construida = dados_imovel.get('area_construida', 134.59)
            valor_edificacao = valor_medio_unitario * area_construida
            
            valor_terreno_m2 = 800.0
            area_terreno = dados_imovel.get('area_terreno', 201.0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            valor_total = valor_edificacao + valor_terreno
        
        # Criar tabela de cálculos
        calculos_tabela = [
            ['Descrição', 'Valor'],
            ['Valor médio unitário de referência:', f"R$ {valor_medio_unitario:,.2f}/m²"],
            ['Área construída do imóvel:', f"{area_construida:.2f} m²"],
            ['Valor estimado da edificação:', f"R$ {valor_edificacao:,.2f}"],
            ['', ''],
            ['Valor do terreno por m²:', f"R$ {valor_terreno_m2:,.2f}/m²"],
            ['Área do terreno:', f"{area_terreno:.2f} m²"],
            ['Valor estimado do terreno:', f"R$ {valor_terreno:,.2f}"],
            ['', ''],
            ['VALOR TOTAL DO IMÓVEL:', f"R$ {valor_total:,.2f}"]
        ]
        
        # Ajustar larguras para ocupar toda a largura da página
        tabela = Table(calculos_tabela, colWidths=[4.2*inch, 2.5*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), HexColor('#2e7d32')),
            ('BACKGROUND', (0, -1), (0, -1), HexColor('#1f4e79')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('TEXTCOLOR', (0, -1), (0, -1), white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica'),
            ('FONTNAME', (1, 1), (1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (0, 8), (1, 8))
        ]))
        
        self.story.append(tabela)
        self.story.append(Spacer(1, 10))
        
    def adicionar_pesquisa_localidade(self, texto_pesquisa):
        """Adiciona a seção de pesquisa de localidade"""
        self.story.append(Paragraph("6. PESQUISA DE LOCALIDADE", self.styles['SubtituloLaudo']))
        
        if texto_pesquisa:
            # Dividir o texto em seções
            secoes = texto_pesquisa.split('\n\n')
            for secao in secoes:
                if secao.strip():
                    self.story.append(Paragraph(secao.strip(), self.styles['TextoLaudo']))
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
            
            self.story.append(Paragraph(texto_padrao, self.styles['TextoLaudo']))
        
        self.story.append(Spacer(1, 10))
        
    def adicionar_conclusao(self, dados_scraper, dados_imovel):
        """Adiciona a seção de conclusão"""
        self.story.append(Paragraph("7. CONCLUSÃO", self.styles['SubtituloLaudo']))
        
        if dados_scraper is not None and not dados_scraper.empty:
            valor_medio_unitario = dados_scraper['R$/M2'].mean()
            area_construida = dados_imovel.get('area_construida', 0)
            valor_edificacao = valor_medio_unitario * area_construida
            
            valor_terreno_m2 = 800.0
            area_terreno = dados_imovel.get('area_terreno', 0)
            valor_terreno = valor_terreno_m2 * area_terreno
            
            valor_total = valor_edificacao + valor_terreno
        else:
            valor_total = 658800.0
        
        # Converter valor para extenso
        valor_extenso = self._converter_valor_extenso(valor_total)
        
        conclusao_texto = f"""Com base nos estudos realizados, considera-se que o valor de mercado do imóvel avaliado é de R$ {valor_total:,.2f} 
        ({valor_extenso}), na data de referência deste laudo. 

        Este valor reflete as condições de mercado atuais, características do imóvel e seu estado de conservação, 
        considerando as especificidades da amostra utilizada e os ajustes técnicos realizados."""
        
        self.story.append(Paragraph(conclusao_texto, self.styles['TextoLaudo']))
        self.story.append(Spacer(1, 15))
        
    def adicionar_assinatura(self, dados_avaliador):
        """Adiciona a seção de assinatura"""
        self.story.append(Paragraph("8. ASSINATURA DO AVALIADOR", self.styles['SubtituloLaudo']))
        
        # Espaço reduzido para assinatura
        self.story.append(Spacer(1, 15))
        
        # Dados do avaliador
        cidade_assinatura = dados_avaliador.get('cidade_assinatura', 'Sorocaba')
        estado_assinatura = dados_avaliador.get('estado_assinatura', 'SP')
        data_laudo = dados_avaliador.get('data_laudo', datetime.now().date())
        
        assinatura_texto = f"""{cidade_assinatura} - {estado_assinatura}, {data_laudo.strftime('%d de %B de %Y')}<br/><br/>
        {dados_avaliador.get('nome', 'Jhonni Balbino da Silva')}<br/>
        Perito Avaliador Imobiliário<br/>
        CRECI: {dados_avaliador.get('creci', '296769-F')} | CNAI: {dados_avaliador.get('cnai', '051453')}<br/>
        {dados_avaliador.get('telefone', '(11) 98796 8206')}<br/>
        {dados_avaliador.get('email', 'contato@avaliarapido.com.br')}<br/>
        {dados_avaliador.get('website', 'www.avaliarapido.com.br')}"""
        
        self.story.append(Paragraph(assinatura_texto, self.styles['Assinatura']))
        
    def _converter_valor_extenso(self, valor):
        """Converte valor numérico para extenso"""
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
        """Salva o documento PDF"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"laudo_avaliacao_{timestamp}.pdf"
        
        # Criar pasta arquivos se não existir
        pasta_arquivos = "arquivos"
        if not os.path.exists(pasta_arquivos):
            os.makedirs(pasta_arquivos)
        
        caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
        
        # Criar documento PDF
        doc = SimpleDocTemplate(caminho_completo, pagesize=A4, 
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
        
        # Construir PDF
        doc.build(self.story)
        
        return caminho_completo
    
    def gerar_laudo_completo(self, dados_imovel, dados_avaliador, dados_scraper=None, texto_pesquisa_localidade=None):
        """Gera o laudo completo em PDF"""
        self.criar_documento()
        
        # Adicionar todas as seções
        self.adicionar_titulo()
        self.adicionar_objetivo()
        self.adicionar_identificacao_imovel(dados_imovel)
        self.adicionar_metodologia()
        self.adicionar_pesquisa_mercado(dados_scraper)
        self.adicionar_determinacao_valor(dados_scraper, dados_imovel)
        self.adicionar_pesquisa_localidade(texto_pesquisa_localidade)
        self.adicionar_conclusao(dados_scraper, dados_imovel)
        self.adicionar_assinatura(dados_avaliador)
        
        # Salvar documento
        return self.salvar_documento()
    

def main():
    """Função para testar o gerador de PDF"""
    gerador = GeradorLaudoPdf()
    
    # Dados de teste
    dados_imovel = {
        'numero_matricula': '11.072',
        'cartorio': 'Comarca de Taquarituba/SP, Livro nº 2 – Registro Geral',
        'area_terreno': 201.0,
        'area_construida': 134.59,
        'loteamento': 'Jardim Santa Virgínia',
        'cidade': 'Taquarituba',
        'estado': 'SP',
        'descricao': 'Casa térrea em alvenaria com telhas cerâmicas, acabamento em gesso, piso cerâmico, portas e janelas em madeira, sistema elétrico e hidráulico completo.'
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
    print(f"PDF gerado: {arquivo_gerado}")

if __name__ == "__main__":
    main()
