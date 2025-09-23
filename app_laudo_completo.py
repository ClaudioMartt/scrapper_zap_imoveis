import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# Importar módulos criados
from zap_scraper import ZapScraper
from laudo_formulario import LaudoFormulario
from pesquisa_localidade_ia_final import PesquisaLocalidadeIAFinal
from gerador_laudo_docx import GeradorLaudoDocx
from gerador_laudo_pdf import GeradorLaudoPdf
from excel_formatter import ExcelFormatter

class AppLaudoCompleto:
    def __init__(self):
        self.scraper = ZapScraper()
        self.formulario = LaudoFormulario()
        self.pesquisa_localidade = PesquisaLocalidadeIAFinal()
        self.gerador_docx = GeradorLaudoDocx()
        self.gerador_pdf = GeradorLaudoPdf()
        self.excel_formatter = ExcelFormatter()
        
    def configurar_pagina(self):
        """Configura a página do Streamlit"""
        st.set_page_config(
            page_title="Sistema de Laudo Imobiliário",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # CSS personalizado
        st.markdown("""
        <style>
            .main-header {
                text-align: center;
                padding: 2rem 0;
                background: linear-gradient(90deg, #1f4e79 0%, #2e7d32 100%);
                color: white;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .step-container {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #2e7d32;
            }
            .success-box {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 1rem;
                margin: 1rem 0;
            }
            .info-box {
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                border-radius: 5px;
                padding: 1rem;
                margin: 1rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def mostrar_cabecalho(self):
        """Mostra o cabeçalho da aplicação"""
        st.markdown("""
        <div class="main-header">
            <h1>🏠 Sistema de Laudo de Avaliação Imobiliária</h1>
            <p>Sistema completo para coleta de dados, análise de mercado e geração de laudos DOCX</p>
        </div>
        """, unsafe_allow_html=True)
    
    def mostrar_progresso(self, etapa_atual, total_etapas):
        """Mostra a barra de progresso"""
        progresso = etapa_atual / total_etapas
        st.progress(progresso)
        st.caption(f"Etapa {etapa_atual} de {total_etapas}")
    
    def executar_scraping(self, url):
        """Executa o scraping de dados"""
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.header("🔍 Etapa 1: Coleta de Dados do Mercado")
        
        with st.spinner("Executando scraping... Isso pode levar alguns minutos."):
            try:
                # Executar scraping
                df_resultado = self.scraper.extrair_dados_pagina(url, max_paginas=5)
                
                if df_resultado is not None and not df_resultado.empty:
                    st.success(f"✅ Dados coletados com sucesso! {len(df_resultado)} imóveis encontrados.")
                    
                    # Mostrar estatísticas básicas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Imóveis", len(df_resultado))
                    with col2:
                        preco_medio = df_resultado['R$/M2'].mean()
                        st.metric("Preço Médio (R$/m²)", f"R$ {preco_medio:,.2f}")
                    with col3:
                        area_media = df_resultado['M2'].mean()
                        st.metric("Área Média", f"{area_media:.1f} m²")
                    
                    # Mostrar preview dos dados
                    st.subheader("📊 Preview dos Dados Coletados")
                    st.dataframe(df_resultado.head(10), use_container_width=True)
                    
                    return df_resultado
                else:
                    st.error("❌ Nenhum dado foi coletado. Verifique a URL e tente novamente.")
                    return None
                    
            except Exception as e:
                st.error(f"❌ Erro durante o scraping: {str(e)}")
                return None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def mostrar_formulario_dados(self):
        """Mostra o formulário para coleta de dados do imóvel e avaliador"""
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.header("📋 Etapa 2: Dados do Imóvel e Avaliador")
        
        # Criar abas para organizar o formulário
        tab1, tab2, tab3 = st.tabs(["🏠 Dados do Imóvel", "👤 Dados do Avaliador", "📅 Data e Localização"])
        
        with tab1:
            self.formulario.mostrar_formulario_imovel()
        
        with tab2:
            self.formulario.mostrar_formulario_avaliador()
        
        with tab3:
            self.formulario.mostrar_formulario_data()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def executar_pesquisa_localidade(self, dados_imovel):
        """Executa a pesquisa de localidade usando APIs"""
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.header("🌍 Etapa 3: Pesquisa de Localidade")
        
        cidade = dados_imovel.get('cidade', 'Taquarituba')
        bairro = dados_imovel.get('loteamento', 'Jardim Santa Virgínia')
        
        # Opção para pular a pesquisa
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"🔍 Pesquisando informações sobre {bairro}, {cidade}")
        
        with col2:
            pular_pesquisa = st.button("⏭️ Pular Pesquisa", help="Usar texto padrão para economizar tempo")
        
        if pular_pesquisa:
            st.warning("⚠️ Pesquisa de localidade pulada.")
            st.info("Será utilizado texto padrão no laudo.")
            return None
        
        # Verificar se há problemas com as APIs
        if not hasattr(self.pesquisa_localidade, 'agent') or not self.pesquisa_localidade.agent:
            st.warning("⚠️ APIs não configuradas. Usando texto padrão.")
            st.info("Será utilizado texto padrão no laudo.")
            return None
        
        try:
            # Adicionar barra de progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Iniciando pesquisa...")
            progress_bar.progress(25)
            
            # Executar pesquisa com timeout implícito
            texto_pesquisa = self.pesquisa_localidade.gerar_texto_pesquisa_localidade(cidade, bairro)
            
            progress_bar.progress(100)
            status_text.text("✅ Pesquisa concluída!")
            
            if texto_pesquisa:
                st.success("✅ Pesquisa de localidade concluída!")
                
                # Mostrar preview do texto
                st.subheader("📝 Preview da Pesquisa de Localidade")
                st.text_area("Texto gerado:", texto_pesquisa, height=200, disabled=True)
            else:
                st.warning("⚠️ Não foram encontradas informações específicas sobre a localidade.")
                st.info("Será utilizado texto padrão no laudo.")
            
            return texto_pesquisa
            
        except Exception as e:
            st.warning(f"⚠️ Erro na pesquisa de localidade: {str(e)}")
            st.info("Usando texto padrão para a pesquisa de localidade.")
            return None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def gerar_excel_formatado(self, dados_scraper):
        """Gera o arquivo Excel formatado com dados do scraper"""
        try:
            # Criar pasta arquivos se não existir
            pasta_arquivos = "arquivos"
            if not os.path.exists(pasta_arquivos):
                os.makedirs(pasta_arquivos)
            
            # Gerar Excel formatado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_excel = f'dados_zap_formatado_{timestamp}.xlsx'
            caminho_excel = os.path.join(pasta_arquivos, filename_excel)
            
            excel_file = self.excel_formatter.gerar_excel_formatado(dados_scraper, caminho_excel)
            
            if excel_file:
                return excel_file
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao gerar Excel: {e}")
            return None
    
    def gerar_laudo_docx(self, dados_scraper, dados_imovel, dados_avaliador, texto_pesquisa):
        """Gera os laudos em DOCX e PDF"""
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.header("📄 Etapa 4: Geração dos Arquivos")
        
        with st.spinner("Gerando arquivos..."):
            try:
                # Gerar laudo DOCX
                arquivo_docx = self.gerador_docx.gerar_laudo_completo(
                    dados_imovel=dados_imovel,
                    dados_avaliador=dados_avaliador,
                    dados_scraper=dados_scraper,
                    texto_pesquisa_localidade=texto_pesquisa
                )
                
                # Gerar laudo PDF
                arquivo_pdf = self.gerador_pdf.gerar_laudo_completo(
                    dados_imovel=dados_imovel,
                    dados_avaliador=dados_avaliador,
                    dados_scraper=dados_scraper,
                    texto_pesquisa_localidade=texto_pesquisa
                )
                
                # Gerar Excel formatado
                arquivo_excel = self.gerar_excel_formatado(dados_scraper)
                
                
                # Sempre mostrar os botões de download se pelo menos um arquivo foi gerado
                if arquivo_docx or arquivo_pdf or arquivo_excel:
                    st.success("✅ Arquivos gerados com sucesso!")
                    
                    # Salvar os arquivos no session_state para persistência
                    st.session_state.arquivo_docx_gerado = arquivo_docx
                    st.session_state.arquivo_pdf_gerado = arquivo_pdf
                    st.session_state.arquivo_excel_gerado = arquivo_excel
                    st.session_state.arquivos_gerados = True
                    
                    # Criar 3 colunas para os botões
                    col1, col2, col3 = st.columns(3)
                    
                    # Botão DOCX
                    with col1:
                        if arquivo_docx:
                            st.subheader("📄 Laudo DOCX")
                            tamanho_docx = os.path.getsize(arquivo_docx) / 1024
                            st.info(f"📁 {os.path.basename(arquivo_docx)}")
                            st.info(f"💾 {tamanho_docx:.1f} KB")
                            
                            with open(arquivo_docx, 'rb') as f:
                                st.download_button(
                                    label="📥 Baixar DOCX",
                                    data=f.read(),
                                    file_name=os.path.basename(arquivo_docx),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    type="primary",
                                    use_container_width=True,
                                    key="download_docx"
                                )
                        else:
                            st.subheader("📄 Laudo DOCX")
                            st.error("❌ Erro na geração")
                    
                    # Botão PDF
                    with col2:
                        if arquivo_pdf:
                            st.subheader("📋 Laudo PDF")
                            tamanho_pdf = os.path.getsize(arquivo_pdf) / 1024
                            st.info(f"📁 {os.path.basename(arquivo_pdf)}")
                            st.info(f"💾 {tamanho_pdf:.1f} KB")
                            
                            with open(arquivo_pdf, 'rb') as f:
                                st.download_button(
                                    label="📥 Baixar PDF",
                                    data=f.read(),
                                    file_name=os.path.basename(arquivo_pdf),
                                    mime="application/pdf",
                                    type="primary",
                                    use_container_width=True,
                                    key="download_pdf"
                                )
                        else:
                            st.subheader("📋 Laudo PDF")
                            st.error("❌ Erro na geração")
                    
                    # Botão Excel
                    with col3:
                        if arquivo_excel:
                            st.subheader("📊 Excel Formatado")
                            tamanho_excel = os.path.getsize(arquivo_excel) / 1024
                            st.info(f"📁 {os.path.basename(arquivo_excel)}")
                            st.info(f"💾 {tamanho_excel:.1f} KB")
                            
                            with open(arquivo_excel, 'rb') as f:
                                st.download_button(
                                    label="📥 Baixar Excel",
                                    data=f.read(),
                                    file_name=os.path.basename(arquivo_excel),
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    type="secondary",
                                    use_container_width=True,
                                    key="download_excel"
                                )
                        else:
                            st.subheader("📊 Excel Formatado")
                            st.error("❌ Erro na geração")
                    
                    return arquivo_docx, arquivo_pdf, arquivo_excel
                    
                else:
                    st.error("❌ Erro ao gerar os arquivos")
                    return None, None, None
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar arquivos: {str(e)}")
                return None, None, None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def mostrar_botoes_download_persistentes(self):
        """Mostra os botões de download de forma persistente"""
        if hasattr(st.session_state, 'arquivos_gerados') and st.session_state.arquivos_gerados:
            arquivo_docx = st.session_state.get('arquivo_docx_gerado')
            arquivo_pdf = st.session_state.get('arquivo_pdf_gerado')
            arquivo_excel = st.session_state.get('arquivo_excel_gerado')
            
            if arquivo_docx or arquivo_pdf or arquivo_excel:
                st.markdown('<div class="step-container">', unsafe_allow_html=True)
                st.header("📥 Downloads Disponíveis")
                st.info("💡 Os arquivos foram gerados com sucesso! Use os botões abaixo para baixar:")
                
                # Criar 3 colunas para os botões
                col1, col2, col3 = st.columns(3)
                
                # Gerar keys únicas baseadas no timestamp
                timestamp = int(time.time())
                
                # Botão DOCX
                with col1:
                    if arquivo_docx and os.path.exists(arquivo_docx):
                        st.subheader("📄 Laudo DOCX")
                        tamanho_docx = os.path.getsize(arquivo_docx) / 1024
                        st.info(f"📁 {os.path.basename(arquivo_docx)}")
                        st.info(f"💾 {tamanho_docx:.1f} KB")
                        
                        with open(arquivo_docx, 'rb') as f:
                            st.download_button(
                                label="📥 Baixar DOCX",
                                data=f.read(),
                                file_name=os.path.basename(arquivo_docx),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                type="primary",
                                use_container_width=True,
                                key=f"download_docx_persistent_{timestamp}"
                            )
                    else:
                        st.subheader("📄 Laudo DOCX")
                        st.error("❌ Arquivo não encontrado")
                
                # Botão PDF
                with col2:
                    if arquivo_pdf and os.path.exists(arquivo_pdf):
                        st.subheader("📋 Laudo PDF")
                        tamanho_pdf = os.path.getsize(arquivo_pdf) / 1024
                        st.info(f"📁 {os.path.basename(arquivo_pdf)}")
                        st.info(f"💾 {tamanho_pdf:.1f} KB")
                        
                        with open(arquivo_pdf, 'rb') as f:
                            st.download_button(
                                label="📥 Baixar PDF",
                                data=f.read(),
                                file_name=os.path.basename(arquivo_pdf),
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True,
                                key=f"download_pdf_persistent_{timestamp}"
                            )
                    else:
                        st.subheader("📋 Laudo PDF")
                        st.error("❌ Arquivo não encontrado")
                
                # Botão Excel
                with col3:
                    if arquivo_excel and os.path.exists(arquivo_excel):
                        st.subheader("📊 Excel Formatado")
                        tamanho_excel = os.path.getsize(arquivo_excel) / 1024
                        st.info(f"📁 {os.path.basename(arquivo_excel)}")
                        st.info(f"💾 {tamanho_excel:.1f} KB")
                        
                        with open(arquivo_excel, 'rb') as f:
                            st.download_button(
                                label="📥 Baixar Excel",
                                data=f.read(),
                                file_name=os.path.basename(arquivo_excel),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                type="secondary",
                                use_container_width=True,
                                key=f"download_excel_persistent_{timestamp}"
                            )
                    else:
                        st.subheader("📊 Excel Formatado")
                        st.error("❌ Arquivo não encontrado")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    def mostrar_botoes_download_atuais(self):
        """Mostra botões APENAS para os arquivos da análise atual"""
        arquivo_docx = st.session_state.get('arquivo_docx')
        arquivo_pdf = st.session_state.get('arquivo_pdf')
        arquivo_excel = st.session_state.get('arquivo_excel')
        
        if arquivo_docx or arquivo_pdf or arquivo_excel:
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.header("📥 Downloads da Análise Atual")
            st.info("💡 Use os botões abaixo para baixar os arquivos da análise atual:")
            
            # Criar colunas baseadas no número de arquivos
            arquivos_atuais = []
            if arquivo_docx: arquivos_atuais.append(('DOCX', arquivo_docx))
            if arquivo_pdf: arquivos_atuais.append(('PDF', arquivo_pdf))
            if arquivo_excel: arquivos_atuais.append(('Excel', arquivo_excel))
            
            if len(arquivos_atuais) == 1:
                col1, col2, col3 = st.columns([1, 1, 1])
                colunas = [col1]
            elif len(arquivos_atuais) == 2:
                col1, col2 = st.columns(2)
                colunas = [col1, col2]
            else:
                col1, col2, col3 = st.columns(3)
                colunas = [col1, col2, col3]
            
            # Mostrar botões para cada arquivo atual
            for i, (tipo, caminho_arquivo) in enumerate(arquivos_atuais):
                if i < len(colunas):
                    with colunas[i]:
                        if os.path.exists(caminho_arquivo):
                            if tipo == "DOCX":
                                st.subheader("📄 Laudo DOCX")
                                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                cor = "primary"
                            elif tipo == "PDF":
                                st.subheader("📋 Laudo PDF")
                                mime = "application/pdf"
                                cor = "primary"
                            else:  # Excel
                                st.subheader("📊 Excel Formatado")
                                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                cor = "secondary"
                            
                            tamanho = os.path.getsize(caminho_arquivo) / 1024
                            st.info(f"📁 {os.path.basename(caminho_arquivo)}")
                            st.info(f"💾 {tamanho:.1f} KB")
                            
                            # Botão de download com key única
                            key_unica = f"download_atual_{tipo.lower()}_{int(time.time() * 1000) % 100000}"
                            with open(caminho_arquivo, 'rb') as f:
                                st.download_button(
                                    label=f"📥 Baixar {tipo}",
                                    data=f.read(),
                                    file_name=os.path.basename(caminho_arquivo),
                                    mime=mime,
                                    type=cor,
                                    use_container_width=True,
                                    key=key_unica
                                )
                        else:
                            st.subheader(f"📄 {tipo}")
                            st.error("❌ Arquivo não encontrado")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    
    def mostrar_resumo_final(self, dados_scraper, dados_imovel, dados_avaliador, arquivo_docx, arquivo_pdf, arquivo_excel):
        """Mostra o resumo final do processo"""
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.header("🎉 Processo Concluído com Sucesso!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Resumo dos Dados")
            if dados_scraper is not None:
                st.write(f"**Imóveis analisados:** {len(dados_scraper)}")
                st.write(f"**Preço médio por m²:** R$ {dados_scraper['R$/M2'].mean():,.2f}")
                st.write(f"**Área média:** {dados_scraper['M2'].mean():.1f} m²")
            
            st.write(f"**Imóvel avaliado:** {dados_imovel.get('loteamento', 'N/A')}, {dados_imovel.get('cidade', 'N/A')}")
            st.write(f"**Área construída:** {dados_imovel.get('area_construida', 0):.2f} m²")
            st.write(f"**Área do terreno:** {dados_imovel.get('area_terreno', 0):.2f} m²")
        
        with col2:
            st.subheader("📄 Arquivos Gerados")
            if arquivo_docx:
                st.write(f"**Laudo DOCX:** {os.path.basename(arquivo_docx)}")
            if arquivo_pdf:
                st.write(f"**Laudo PDF:** {os.path.basename(arquivo_pdf)}")
            if arquivo_excel:
                st.write(f"**Excel:** {os.path.basename(arquivo_excel)}")
            st.write(f"**Avaliador:** {dados_avaliador.get('nome', 'N/A')}")
            st.write(f"**CRECI:** {dados_avaliador.get('creci', 'N/A')}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def executar_fluxo_completo(self):
        """Executa o fluxo completo do sistema"""
        # Mostrar cabeçalho
        self.mostrar_cabecalho()
        
        # Etapa 1: URL e Scraping
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.header("🚀 Iniciar Processo")
        
        url_input = st.text_input(
            "URL do Zap Imóveis",
            placeholder="Cole aqui a URL do Zap Imóveis...",
            help="URL da busca de imóveis no Zap Imóveis"
        )
        
        if st.button("🔍 Iniciar Scraping", disabled=not url_input, type="primary"):
            if "zapimoveis.com.br" not in url_input:
                st.error("⚠️ Por favor, insira uma URL válida do Zap Imóveis")
            else:
                # Executar scraping
                dados_scraper = self.executar_scraping(url_input)
                
                if dados_scraper is not None:
                    st.session_state.dados_scraper = dados_scraper
                    st.session_state.etapa_atual = 2
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Verificar se temos dados do scraper
        if 'dados_scraper' in st.session_state:
            dados_scraper = st.session_state.dados_scraper
            
            # Mostrar progresso
            self.mostrar_progresso(2, 4)
            
            # Etapa 2: Formulário
            self.mostrar_formulario_dados()
            
            # Botão para validar e continuar
            if st.button("✅ Validar Dados e Continuar", type="primary"):
                erros = self.formulario.validar_dados()
                
                if erros:
                    st.error("❌ Erros encontrados:")
                    for erro in erros:
                        st.write(f"- {erro}")
                else:
                    st.success("✅ Todos os dados foram preenchidos corretamente!")
                    dados_completos = self.formulario.obter_dados_completos()
                    st.session_state.dados_imovel = dados_completos['imovel']
                    st.session_state.dados_avaliador = dados_completos['avaliador']
                    st.session_state.etapa_atual = 3
                    st.rerun()
            
            # Verificar se temos dados do formulário
            if 'dados_imovel' in st.session_state and 'dados_avaliador' in st.session_state:
                dados_imovel = st.session_state.dados_imovel
                dados_avaliador = st.session_state.dados_avaliador
                
                # Mostrar progresso
                self.mostrar_progresso(3, 4)
                
                # Etapa 3: Pesquisa de Localidade (apenas se não foi feita ainda)
                if 'texto_pesquisa' not in st.session_state:
                    texto_pesquisa = self.executar_pesquisa_localidade(dados_imovel)
                    st.session_state.texto_pesquisa = texto_pesquisa
                else:
                    texto_pesquisa = st.session_state.texto_pesquisa
                    st.info("✅ Pesquisa de localidade já realizada anteriormente.")
                
                # Botão para gerar arquivos (apenas se ainda não foram gerados)
                if 'arquivo_docx' not in st.session_state and 'arquivo_pdf' not in st.session_state and 'arquivo_excel' not in st.session_state:
                    if st.button("📄 Gerar Laudos DOCX, PDF e Excel", type="primary"):
                        # Mostrar progresso
                        self.mostrar_progresso(4, 4)
                        
                        # Etapa 4: Gerar Arquivos
                        arquivo_docx, arquivo_pdf, arquivo_excel = self.gerar_laudo_docx(
                            dados_scraper, dados_imovel, dados_avaliador, texto_pesquisa
                        )
                        
                        if arquivo_docx or arquivo_pdf or arquivo_excel:
                            st.session_state.arquivo_docx = arquivo_docx
                            st.session_state.arquivo_pdf = arquivo_pdf
                            st.session_state.arquivo_excel = arquivo_excel
                            st.session_state.etapa_atual = 5
                            st.rerun()
                else:
                    st.success("✅ Arquivos já foram gerados! Use os botões de download abaixo.")
                
                # Verificar se temos arquivos gerados da análise atual
                if 'arquivo_docx' in st.session_state or 'arquivo_pdf' in st.session_state or 'arquivo_excel' in st.session_state:
                    # Mostrar resumo final
                    self.mostrar_resumo_final(
                        dados_scraper, dados_imovel, dados_avaliador, 
                        st.session_state.get('arquivo_docx'), 
                        st.session_state.get('arquivo_pdf'),
                        st.session_state.get('arquivo_excel')
                    )
                    
                    # Mostrar botões de download APENAS após geração
                    self.mostrar_botoes_download_atuais()
                    
                    # Botão para novo laudo
                    if st.button("🔄 Gerar Novo Laudo", type="secondary"):
                        # Limpar session state
                        for key in list(st.session_state.keys()):
                            if key.startswith('dados_') or key.startswith('etapa_') or key.startswith('arquivo_') or key.startswith('texto_'):
                                del st.session_state[key]
                        st.rerun()

def main():
    """Função principal da aplicação"""
    app = AppLaudoCompleto()
    app.configurar_pagina()
    app.executar_fluxo_completo()

if __name__ == "__main__":
    main()
