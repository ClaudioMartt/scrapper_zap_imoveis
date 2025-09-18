import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import re
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import zscore
import warnings
warnings.filterwarnings("ignore")

# Importar as funções do scraper
from zap_scraper import ZapScraper
from excel_formatter import ExcelFormatter

def criar_pasta_arquivos():
    """Cria a pasta 'arquivos' se ela não existir"""
    pasta_arquivos = "arquivos"
    if not os.path.exists(pasta_arquivos):
        os.makedirs(pasta_arquivos)
        print(f"📁 Pasta '{pasta_arquivos}' criada com sucesso!")
    return pasta_arquivos

# Configuração da página
st.set_page_config(
    page_title="Zap Imóveis Scraper",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado estilo Google
st.markdown("""
<style>
    /* Esconder elementos do Streamlit */
    .stApp > header {
        visibility: hidden;
    }
    .stApp > div:first-child {
        padding-top: 0rem;
    }
    
    /* Container principal centralizado */
    .main-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem 1rem;
        text-align: center;
    }
    
    /* Logo estilo Google */
    .logo {
        font-size: 4rem;
        font-weight: 400;
        color: #4285f4;
        margin-bottom: 2rem;
        font-family: 'Product Sans', Arial, sans-serif;
    }
    
    /* Barra de busca estilo Google */
    .search-container {
        position: relative;
        margin-bottom: 2rem;
    }
    
    .search-box {
        width: 100%;
        max-width: 500px;
        padding: 12px 20px;
        font-size: 16px;
        border: 1px solid #dfe1e5;
        border-radius: 24px;
        outline: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px 1px rgba(64,60,67,.16);
    }
    
    .search-box:hover {
        box-shadow: 0 2px 8px 1px rgba(64,60,67,.24);
    }
    
    .search-box:focus {
        border-color: #4285f4;
        box-shadow: 0 2px 8px 1px rgba(64,60,67,.24);
    }
    
    /* Botão estilo Google */
    .google-button {
        background-color: #f8f9fa;
        border: 1px solid #f8f9fa;
        border-radius: 4px;
        color: #3c4043;
        font-size: 14px;
        padding: 10px 20px;
        margin: 11px 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .google-button:hover {
        box-shadow: 0 1px 1px rgba(0,0,0,.1);
        background-color: #f8f9fa;
        border: 1px solid #dadce0;
        color: #202124;
    }
    
    .google-button-primary {
        background-color: #4285f4;
        color: white;
        border: 1px solid #4285f4;
    }
    
    .google-button-primary:hover {
        background-color: #3367d6;
        border: 1px solid #3367d6;
    }
    
    /* Container de status */
    .status-container {
        max-width: 600px;
        margin: 2rem auto;
        text-align: center;
    }
    
    .status-message {
        font-size: 14px;
        color: #5f6368;
        margin: 1rem 0;
    }
    
    /* Barra de progresso personalizada */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4285f4 0%, #34a853 100%);
    }
    
    /* Resultados */
    .results-container {
        max-width: 800px;
        margin: 2rem auto;
        text-align: left;
    }
    
    /* Esconder elementos desnecessários */
    .stApp > div:first-child > div:first-child > div:first-child {
        display: none;
    }
    
    /* Espaçamento */
    .spacing {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Container principal estilo Google
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Logo estilo Google
    st.markdown("""
    <div class="logo">
        🏠 Zap Scraper
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de URL centralizada
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    url_input = st.text_input(
        "",
        placeholder="Cole aqui a URL do Zap Imóveis...",
        key="url_input",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Validação da URL
    if url_input and "zapimoveis.com.br" not in url_input:
        st.error("⚠️ Por favor, insira uma URL válida do Zap Imóveis")
        url_input = None
    
    # Botões estilo Google
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        pass  # Espaço vazio
    
    with col2:
        if st.button("🚀 Iniciar Scraping", disabled=not url_input, use_container_width=True):
            if url_input:
                executar_scraping(url_input)
    
    with col3:
        pass  # Espaço vazio
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Área de status e resultados
    if 'scraping_status' in st.session_state:
        mostrar_resultados()

def executar_scraping(url):
    """Executa o scraping e mostra o progresso"""
    
    # Configurações padrão
    max_paginas = 5
    timeout = 30
    remover_outliers = True
    gerar_graficos = True
    gerar_excel = True
    detectar_duplicatas = True
    
    # Inicializar variáveis de sessão
    st.session_state.scraping_status = "iniciando"
    st.session_state.dados_coletados = []
    st.session_state.arquivos_gerados = []
    st.session_state.estatisticas = {}
    
    # Container para progresso centralizado
    st.markdown('<div class="status-container">', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.empty()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    try:
        # Inicializar scraper
        scraper = ZapScraper()
        
        # Simular progresso (em uma implementação real, isso seria baseado no progresso real)
        status_text.text("🔄 Inicializando navegador...")
        progress_bar.progress(10)
        log_container.text("Configurando driver do Chrome...")
        
        # Executar scraping
        status_text.text("🔍 Coletando dados dos imóveis...")
        progress_bar.progress(30)
        if detectar_duplicatas:
            log_container.text("Acessando página e coletando dados (detecção de duplicatas ativa)...")
        else:
            log_container.text("Acessando página e coletando dados...")
        
        # Aqui você integraria com a função real do scraper
        dados = scraper.extrair_dados_pagina(url, max_paginas)
        
        if dados is not None and not dados.empty:
            status_text.text("✅ Dados coletados com sucesso!")
            progress_bar.progress(80)
            log_container.text(f"Coletados {len(dados)} imóveis com sucesso!")
            
            # Processar dados
            df = pd.DataFrame(dados)
            st.session_state.dados_coletados = df
            
            # Remover outliers se solicitado
            if remover_outliers:
                status_text.text("🧹 Removendo outliers...")
                log_container.text("Aplicando filtros para remoção de outliers...")
                df_limpo = scraper.remover_outliers_iterativo(df)
                st.session_state.dados_coletados = df_limpo
            
            # Calcular estatísticas
            status_text.text("📈 Calculando estatísticas...")
            progress_bar.progress(90)
            log_container.text("Calculando estatísticas dos dados coletados...")
            
            estatisticas = scraper.calcular_estatisticas(df)
            st.session_state.estatisticas = estatisticas
            
            # Obter estatísticas de duplicatas
            stats_duplicatas = scraper.obter_estatisticas_duplicatas()
            st.session_state.estatisticas_duplicatas = stats_duplicatas
            
            # Criar pasta arquivos e salvar CSV
            pasta_arquivos = criar_pasta_arquivos()
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename_csv = f'dados_zap_{timestamp}.csv'
            caminho_csv = os.path.join(pasta_arquivos, filename_csv)
            df.to_csv(caminho_csv, index=False)
            st.session_state.arquivos_gerados.append(caminho_csv)
            
            # Gerar Excel se solicitado
            if gerar_excel:
                status_text.text("📊 Gerando Excel formatado...")
                progress_bar.progress(95)
                log_container.text("Criando arquivo Excel com 6 abas de análise...")
                
                try:
                    excel_formatter = ExcelFormatter()
                    filename_excel = f'dados_zap_formatado_{timestamp}.xlsx'
                    caminho_excel = os.path.join(pasta_arquivos, filename_excel)
                    excel_file = excel_formatter.gerar_excel_formatado(df, caminho_excel)
                    
                    if excel_file:
                        st.session_state.arquivos_gerados.append(excel_file)
                        log_container.text("✅ Excel formatado criado com sucesso!")
                    else:
                        log_container.text("⚠️ Erro ao criar Excel formatado")
                        
                except Exception as e:
                    log_container.text(f"⚠️ Erro ao gerar Excel: {str(e)}")
            
            status_text.text("🎉 Scraping concluído!")
            progress_bar.progress(100)
            log_container.text("Processo finalizado com sucesso!")
            
            # Atualizar status
            st.session_state.scraping_status = "concluido"
            
        else:
            st.error("❌ Nenhum dado foi coletado. Verifique a URL e tente novamente.")
            st.session_state.scraping_status = "erro"
    
    except Exception as e:
        st.error(f"❌ Erro durante o scraping: {str(e)}")
        st.session_state.scraping_status = "erro"
        log_container.text(f"Erro: {str(e)}")

def mostrar_resultados():
    """Mostra os resultados do scraping"""
    
    if st.session_state.scraping_status == "concluido":
        # Container de resultados
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Mensagem de sucesso centralizada
        st.success("✅ Scraping concluído com sucesso!")
        
        # Resumo principal
        st.header("📊 Resumo dos Dados Coletados")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🏠 Total de Imóveis",
                st.session_state.estatisticas.get('total_linhas', 0)
            )
        
        with col2:
            preco_medio = st.session_state.estatisticas.get('media_aritmetica', 0)
            st.metric(
                "💰 Preço Médio (R$/m²)",
                f"R$ {preco_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            )
        
        with col3:
            area_media = st.session_state.estatisticas.get('area_media', 0)
            st.metric(
                "📐 Área Média",
                f"{area_media:,.0f} m²"
            )
        
        with col4:
            coef_var = st.session_state.estatisticas.get('coef_variacao', 0)
            st.metric(
                "📊 Coef. Variação",
                f"{coef_var:.2%}"
            )
        
        # # Estatísticas de duplicatas (se disponível)
        # if 'estatisticas_duplicatas' in st.session_state:
        #     st.subheader("🔄 Duplicatas Detectadas")
            
        #     col_dup1, col_dup2 = st.columns(2)
            
        #     with col_dup1:
        #         st.metric(
        #             "🔄 Duplicatas Removidas",
        #             st.session_state.estatisticas_duplicatas.get('duplicatas_detectadas', 0)
        #         )
            
        #     with col_dup2:
        #         taxa_dup = st.session_state.estatisticas_duplicatas.get('taxa_duplicatas', 0)
        #         st.metric(
        #             "📈 Taxa de Duplicatas",
        #             f"{taxa_dup:.1f}%"
        #         )
        
        # Mostrar Top 10 imóveis
        st.header("🏆 Top 10 Melhores Imóveis")
        st.markdown("*Os melhores imóveis por preço por m² (menor valor)*")
        
        df = st.session_state.dados_coletados
        
        # Criar Top 10 baseado no preço por m² (menor valor = melhor)
        if 'R$/M2' in df.columns:
            df_top10 = df.sort_values('R$/M2').head(10)
            
            # Selecionar apenas as colunas mais importantes para exibição
            colunas_importantes = []
            
            # Ordem de prioridade das colunas
            colunas_prioridade = [
                'Endereco', 'Localidade', 'Preco', 'M2', 'R$/M2', 
                'Quartos', 'Banheiros', 'Tipo', 'Condominio'
            ]
            
            for coluna in colunas_prioridade:
                if coluna in df_top10.columns:
                    colunas_importantes.append(coluna)
            
            # Mostrar apenas as colunas importantes
            df_exibicao = df_top10[colunas_importantes] if colunas_importantes else df_top10
            
            # Formatar valores monetários para melhor visualização
            if 'Preco' in df_exibicao.columns:
                df_exibicao = df_exibicao.copy()
                df_exibicao['Preco'] = df_exibicao['Preco'].apply(lambda x: f"R$ {x:,.0f}" if pd.notna(x) else x)
            
            if 'R$/M2' in df_exibicao.columns:
                df_exibicao = df_exibicao.copy()
                df_exibicao['R$/M2'] = df_exibicao['R$/M2'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else x)
            
            st.dataframe(df_exibicao, use_container_width=True)
            
            # Mostrar estatísticas do Top 10
            col1, col2, col3 = st.columns(3)
            
            with col1:
                preco_medio_top10 = df_top10['R$/M2'].mean()
                st.metric(
                    "💰 Preço Médio Top 10",
                    f"R$ {preco_medio_top10:,.2f}/m²"
                )
            
            with col2:
                area_media_top10 = df_top10['M2'].mean() if 'M2' in df_top10.columns else 0
                st.metric(
                    "📐 Área Média Top 10",
                    f"{area_media_top10:,.0f} m²"
                )
            
            with col3:
                preco_total_medio = df_top10['Preco'].mean() if 'Preco' in df_top10.columns else 0
                st.metric(
                    "🏠 Preço Total Médio",
                    f"R$ {preco_total_medio:,.0f}"
                )
        else:
            st.warning("⚠️ Não foi possível calcular o Top 10 - coluna 'R$/M2' não encontrada")
            st.dataframe(df.head(10), use_container_width=True)
        
        # Gráfico dos Top 10
        if len(df) > 0 and 'R$/M2' in df.columns:
            st.header("📈 Top 10 - Preços por m²")
            
            df_top10 = df.sort_values('R$/M2').head(10)
            
            # Criar gráfico de barras para os Top 10
            fig_bar = px.bar(
                df_top10, 
                x='R$/M2', 
                y='Endereco' if 'Endereco' in df_top10.columns else 'Localidade',
                title='Top 10 Melhores Preços por m²',
                labels={'R$/M2': 'Preço por m² (R$)', 'Endereco': 'Endereço', 'Localidade': 'Localidade'},
                color='R$/M2',
                color_continuous_scale='Blues_r',  # Escala invertida (azul mais escuro = menor preço)
                orientation='h'
            )
            fig_bar.update_layout(
                showlegend=False,
                height=400,
                yaxis={'categoryorder':'total ascending'}  # Ordenar por valor
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Download de arquivos
        st.header("💾 Download dos Arquivos")
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            csv_files = [f for f in st.session_state.arquivos_gerados if f.endswith('.csv')]
            for arquivo in csv_files:
                if os.path.exists(arquivo):
                    with open(arquivo, 'rb') as f:
                        st.download_button(
                            label=f"📥 Baixar CSV",
                            data=f.read(),
                            file_name=arquivo,
                            mime="text/csv",
                            use_container_width=True
                        )
        
        with col_download2:
            excel_files = [f for f in st.session_state.arquivos_gerados if f.endswith('.xlsx')]
            for arquivo in excel_files:
                if os.path.exists(arquivo):
                    with open(arquivo, 'rb') as f:
                        st.download_button(
                            label=f"📥 Baixar Excel",
                            data=f.read(),
                            file_name=arquivo,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
