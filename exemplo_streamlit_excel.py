#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Streamlit com funcionalidade de Excel
"""

import streamlit as st
import pandas as pd
from excel_formatter import ExcelFormatter
import os

def main():
    """Demonstração da funcionalidade de Excel no Streamlit"""
    
    st.set_page_config(
        page_title="📊 Exemplo Excel no Streamlit",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Demonstração: Excel Formatado no Streamlit")
    
    st.markdown("""
    Este exemplo demonstra como integrar a funcionalidade de Excel formatado 
    no Streamlit para o projeto Zap Imóveis.
    """)
    
    # Verificar se há arquivos CSV existentes
    arquivos_csv = [f for f in os.listdir('.') if f.startswith('dados_zap_') and f.endswith('.csv')]
    
    if arquivos_csv:
        st.success(f"✅ Encontrados {len(arquivos_csv)} arquivo(s) CSV para processar")
        
        # Selecionar arquivo
        arquivo_selecionado = st.selectbox(
            "Selecione um arquivo CSV para converter para Excel:",
            arquivos_csv
        )
        
        if st.button("🔄 Converter para Excel Formatado"):
            with st.spinner("Processando arquivo..."):
                try:
                    # Ler CSV
                    df = pd.read_csv(arquivo_selecionado)
                    st.info(f"📊 Arquivo carregado: {len(df)} registros")
                    
                    # Criar Excel formatado
                    excel_formatter = ExcelFormatter()
                    excel_file = excel_formatter.gerar_excel_formatado(df)
                    
                    if excel_file:
                        st.success(f"✅ Excel criado: {excel_file}")
                        
                        # Mostrar informações do arquivo
                        tamanho = os.path.getsize(excel_file) / 1024
                        st.metric("Tamanho do arquivo", f"{tamanho:.1f} KB")
                        
                        # Botão de download
                        with open(excel_file, 'rb') as f:
                            st.download_button(
                                label="📥 Baixar Excel Formatado",
                                data=f.read(),
                                file_name=excel_file,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        
                        # Mostrar preview dos dados
                        st.subheader("📋 Preview dos Dados")
                        st.dataframe(df.head(10))
                        
                    else:
                        st.error("❌ Erro ao criar arquivo Excel")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    else:
        st.warning("⚠️ Nenhum arquivo CSV encontrado")
        st.info("💡 Execute primeiro o scraper para gerar dados CSV")
    
    # Informações sobre o Excel
    st.markdown("---")
    st.subheader("📊 Sobre o Excel Formatado")
    
    st.markdown("""
    O arquivo Excel gerado contém **6 abas** com análises detalhadas:
    
    ### 📋 Dados Completos
    - Todos os imóveis coletados
    - Formatação profissional com cores alternadas
    - Colunas: Descrição, Endereço, M², Quartos, Banheiros, Vagas, Preço, Condomínio, IPTU, R$/M²
    
    ### 📈 Resumo Estatístico
    - Métricas gerais dos dados
    - Preços médios, mínimos e máximos
    - Áreas médias e coeficientes de variação
    - Estatísticas de quartos, banheiros e vagas
    
    ### 💰 Análise de Preços
    - Distribuição por faixas de preço
    - Quantidade de imóveis por faixa
    - Preços médios por faixa
    - Área média por faixa de preço
    
    ### 🏠 Análise de Áreas
    - Distribuição por faixas de área
    - Quantidade de imóveis por faixa
    - Preços médios por faixa de área
    - Análise de preço por m² por faixa
    
    ### 🏆 Top Imóveis
    - Top 10 melhores preços por m²
    - Imóveis com melhor custo-benefício
    - Ordenados por menor R$/M²
    
    ### 🔍 Filtros Especiais
    - Imóveis 3 quartos + 2 banheiros
    - Imóveis com vaga de garagem
    - Imóveis até R$ 200.000
    - Imóveis 50-80m²
    """)
    
    # Como usar no Streamlit
    st.markdown("---")
    st.subheader("🚀 Como Usar no Streamlit")
    
    st.code("""
# No seu app.py do Streamlit:

from excel_formatter import ExcelFormatter

# Durante o processamento dos dados:
if gerar_excel:
    excel_formatter = ExcelFormatter()
    excel_file = excel_formatter.gerar_excel_formatado(df)
    
    # Botão de download
    with open(excel_file, 'rb') as f:
        st.download_button(
            label="📥 Baixar Excel",
            data=f.read(),
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    """, language="python")

if __name__ == "__main__":
    main()
