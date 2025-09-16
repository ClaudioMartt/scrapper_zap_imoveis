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

# Configuração da página
st.set_page_config(
    page_title="🏠 Zap Imóveis Scraper",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .url-input {
        font-size: 16px;
        padding: 10px;
    }
    .search-container {
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
    }
    .search-box {
        width: 100%;
        padding: 12px 20px;
        font-size: 16px;
        border: 2px solid #ddd;
        border-radius: 25px;
        outline: none;
        transition: border-color 0.3s;
    }
    .search-box:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    .progress-container {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Zap Imóveis Scraper</h1>
        <p>Extraia dados de imóveis do Zap Imóveis de forma rápida e eficiente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Configurações do scraper
        max_paginas = st.slider("Número máximo de páginas", 1, 20, 5)
        timeout = st.slider("Timeout (segundos)", 10, 60, 30)
        
        st.markdown("---")
        st.markdown("### 📊 Opções de Análise")
        remover_outliers = st.checkbox("Remover outliers", value=True)
        gerar_graficos = st.checkbox("Gerar gráficos", value=True)
        gerar_excel = st.checkbox("Gerar Excel formatado", value=True)
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.info("""
        Esta ferramenta extrai dados de imóveis do Zap Imóveis incluindo:
        - Preço e localização
        - Área e características
        - Análise estatística
        - Gráficos e visualizações
        - Excel formatado com 6 abas
        """)
    
    # Área principal centralizada
    st.markdown("---")
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Container centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown("### 🔗 URL do Zap Imóveis")
        
        # Input para URL centralizado
        url_input = st.text_input(
            "",
            placeholder="https://www.zapimoveis.com.br/venda/apartamentos/...",
            help="Cole a URL completa da página de busca do Zap Imóveis",
            key="url_input",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Validação da URL
        if url_input and "zapimoveis.com.br" not in url_input:
            st.error("⚠️ Por favor, insira uma URL válida do Zap Imóveis")
            url_input = None
        
        # Espaçamento
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão centralizado
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("🚀 Iniciar Scraping", type="primary", disabled=not url_input, use_container_width=True):
                if url_input:
                    executar_scraping(url_input, max_paginas, timeout, remover_outliers, gerar_graficos, gerar_excel)
        
        # Espaçamento após o botão
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Área de status e resultados
    if 'scraping_status' in st.session_state:
        mostrar_resultados()

def executar_scraping(url, max_paginas, timeout, remover_outliers, gerar_graficos, gerar_excel):
    """Executa o scraping e mostra o progresso"""
    
    # Inicializar variáveis de sessão
    st.session_state.scraping_status = "iniciando"
    st.session_state.dados_coletados = []
    st.session_state.arquivos_gerados = []
    st.session_state.estatisticas = {}
    
    # Container para progresso
    progress_container = st.container()
    status_container = st.container()
    results_container = st.container()
    
    with progress_container:
        # Container centralizado para progresso
        col_prog1, col_prog2, col_prog3 = st.columns([1, 2, 1])
        
        with col_prog2:
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Progresso do Scraping")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Placeholder para logs
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
            
            # Salvar arquivos CSV
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename_csv = f'dados_zap_{timestamp}.csv'
            df.to_csv(filename_csv, index=False)
            st.session_state.arquivos_gerados.append(filename_csv)
            
            # Gerar Excel se solicitado
            if gerar_excel:
                status_text.text("📊 Gerando Excel formatado...")
                progress_bar.progress(95)
                log_container.text("Criando arquivo Excel com 6 abas de análise...")
                
                try:
                    excel_formatter = ExcelFormatter()
                    filename_excel = f'dados_zap_formatado_{timestamp}.xlsx'
                    excel_file = excel_formatter.gerar_excel_formatado(df, filename_excel)
                    
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
        # Centralizar mensagem de sucesso
        col_msg1, col_msg2, col_msg3 = st.columns([1, 2, 1])
        with col_msg2:
            st.success("✅ Scraping concluído com sucesso!")
        
        # Mostrar estatísticas principais
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
        
        # Mostrar dados em tabela
        st.header("📋 Dados Coletados")
        
        df = st.session_state.dados_coletados
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Localidade' in df.columns:
                localidades = ['Todas'] + list(df['Localidade'].unique())
                localidade_selecionada = st.selectbox("Filtrar por localidade:", localidades)
                if localidade_selecionada != 'Todas':
                    df = df[df['Localidade'] == localidade_selecionada]
        
        with col2:
            if 'Quartos' in df.columns:
                quartos = ['Todos'] + sorted(df['Quartos'].dropna().unique().astype(int))
                quartos_selecionados = st.selectbox("Filtrar por quartos:", quartos)
                if quartos_selecionados != 'Todos':
                    df = df[df['Quartos'] == quartos_selecionados]
        
        with col3:
            if 'Preco' in df.columns:
                preco_min = float(df['Preco'].min())
                preco_max = float(df['Preco'].max())
                preco_range = st.slider(
                    "Faixa de preço:",
                    preco_min, preco_max, (preco_min, preco_max),
                    format="R$ %.0f"
                )
                df = df[(df['Preco'] >= preco_range[0]) & (df['Preco'] <= preco_range[1])]
        
        # Mostrar tabela
        st.dataframe(df, use_container_width=True)
        
        # Gráficos
        if len(df) > 0:
            st.header("📈 Visualizações")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Histograma de preço por m²
                if 'R$/M2' in df.columns:
                    fig_hist = px.histogram(
                        df, x='R$/M2', 
                        title='Distribuição de Preços por m²',
                        labels={'R$/M2': 'Preço por m² (R$)', 'count': 'Quantidade'},
                        color_discrete_sequence=['#667eea']
                    )
                    fig_hist.update_layout(showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Boxplot de preço por m²
                if 'R$/M2' in df.columns:
                    fig_box = go.Figure()
                    fig_box.add_trace(go.Box(
                        y=df['R$/M2'],
                        name='Preço por m²',
                        marker_color='#764ba2'
                    ))
                    fig_box.update_layout(
                        title='Boxplot de Preços por m²',
                        yaxis_title='Preço por m² (R$)'
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
            
            # Scatter plot: Área vs Preço
            if 'M2' in df.columns and 'Preco' in df.columns:
                fig_scatter = px.scatter(
                    df, x='M2', y='Preco',
                    title='Área vs Preço dos Imóveis',
                    labels={'M2': 'Área (m²)', 'Preco': 'Preço (R$)'},
                    color='R$/M2' if 'R$/M2' in df.columns else None,
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Informações sobre Excel
        excel_files = [f for f in st.session_state.arquivos_gerados if f.endswith('.xlsx')]
        if excel_files:
            st.info("""
            📊 **Arquivo Excel Gerado!** 
            
            O arquivo Excel contém **6 abas** com análises detalhadas:
            - 📋 **Dados Completos**: Todos os imóveis coletados
            - 📈 **Resumo Estatístico**: Métricas gerais
            - 💰 **Análise de Preços**: Distribuição por faixas
            - 🏠 **Análise de Áreas**: Distribuição por faixas
            - 🏆 **Top Imóveis**: Melhores preços por m²
            - 🔍 **Filtros Especiais**: Imóveis com características específicas
            """)
        
        # Download de arquivos
        st.header("💾 Download dos Arquivos")
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            st.subheader("📄 Arquivo CSV")
            csv_files = [f for f in st.session_state.arquivos_gerados if f.endswith('.csv')]
            for arquivo in csv_files:
                if os.path.exists(arquivo):
                    with open(arquivo, 'rb') as f:
                        st.download_button(
                            label=f"📥 Baixar CSV: {arquivo}",
                            data=f.read(),
                            file_name=arquivo,
                            mime="text/csv",
                            use_container_width=True
                        )
        
        with col_download2:
            st.subheader("📊 Arquivo Excel")
            excel_files = [f for f in st.session_state.arquivos_gerados if f.endswith('.xlsx')]
            for arquivo in excel_files:
                if os.path.exists(arquivo):
                    with open(arquivo, 'rb') as f:
                        st.download_button(
                            label=f"📥 Baixar Excel: {arquivo}",
                            data=f.read(),
                            file_name=arquivo,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
            
            if not excel_files:
                st.info("💡 Ative a opção 'Gerar Excel formatado' na sidebar para criar arquivos Excel")
        
        # Estatísticas detalhadas
        st.header("📊 Estatísticas Detalhadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Preço por m²")
            stats_data = {
                'Métrica': ['Média Aritmética', 'Média Ponderada', 'Mediana', 'Moda', 'Coef. Variação'],
                'Valor': [
                    f"R$ {st.session_state.estatisticas.get('media_aritmetica', 0):,.2f}",
                    f"R$ {st.session_state.estatisticas.get('media_ponderada', 0):,.2f}",
                    f"R$ {st.session_state.estatisticas.get('mediana', 0):,.2f}",
                    f"R$ {st.session_state.estatisticas.get('moda', 0):,.2f}",
                    f"{st.session_state.estatisticas.get('coef_variacao', 0):.2%}"
                ]
            }
            st.table(pd.DataFrame(stats_data))
        
        with col2:
            st.subheader("🏠 Resumo Geral")
            resumo_data = {
                'Item': ['Total de Imóveis', 'Preço Médio Total', 'Área Média'],
                'Valor': [
                    f"{st.session_state.estatisticas.get('total_linhas', 0)}",
                    f"R$ {st.session_state.estatisticas.get('preco_medio', 0):,.2f}",
                    f"{st.session_state.estatisticas.get('area_media', 0):,.0f} m²"
                ]
            }
            st.table(pd.DataFrame(resumo_data))

if __name__ == "__main__":
    main()
