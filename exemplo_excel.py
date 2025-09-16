#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do ExcelFormatter para criar arquivos Excel formatados
"""

import pandas as pd
from excel_formatter import ExcelFormatter, processar_csv_para_excel
from zap_scraper import ZapScraper
import os

def main():
    """Função principal para demonstrar o uso do ExcelFormatter"""
    
    print("🏠 FORMATADOR DE DADOS ZAP IMÓVEIS PARA EXCEL")
    print("=" * 50)
    
    print("Escolha uma opção:")
    print("1. Processar arquivo CSV existente")
    print("2. Executar scraper completo com Excel automático")
    print("3. Executar scraper automático (sem interação)")
    print("4. Sair")
    
    while True:
        try:
            opcao = input("\nDigite sua escolha (1-4): ").strip()
            
            if opcao == "1":
                processar_csv_existente()
                break
            elif opcao == "2":
                executar_scraper_completo()
                break
            elif opcao == "3":
                executar_scraper_automatico()
                break
            elif opcao == "4":
                print("👋 Até logo!")
                return
            else:
                print("❌ Opção inválida! Digite 1, 2, 3 ou 4")
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada pelo usuário")
            return

def processar_csv_existente():
    """Processa um arquivo CSV existente"""
    print("\n📁 PROCESSANDO ARQUIVO CSV EXISTENTE")
    print("-" * 40)
    
    # Verificar arquivos CSV disponíveis
    arquivos_csv = [f for f in os.listdir('.') if f.startswith('dados_zap_') and f.endswith('.csv')]
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo CSV encontrado!")
        print("💡 Execute primeiro o scraper para gerar dados CSV")
        return
    
    print(f"📋 Encontrados {len(arquivos_csv)} arquivo(s) CSV:")
    for i, arquivo in enumerate(arquivos_csv, 1):
        tamanho = os.path.getsize(arquivo) / 1024  # KB
        print(f"  {i}. {arquivo} ({tamanho:.1f} KB)")
    
    # Selecionar arquivo
    while True:
        try:
            escolha = input(f"\nEscolha um arquivo (1-{len(arquivos_csv)}) ou Enter para o mais recente: ").strip()
            
            if not escolha:
                arquivo_selecionado = arquivos_csv[-1]
                break
            elif escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(arquivos_csv):
                    arquivo_selecionado = arquivos_csv[idx]
                    break
                else:
                    print("❌ Número inválido!")
            else:
                print("❌ Digite um número válido!")
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada pelo usuário")
            return
    
    print(f"\n🔄 Processando arquivo: {arquivo_selecionado}")
    print("⏳ Aguarde enquanto criamos o Excel formatado...")
    
    # Processar arquivo
    excel_gerado = processar_csv_para_excel(arquivo_selecionado)
    
    if excel_gerado:
        mostrar_resultado_excel(excel_gerado)
    else:
        print("\n❌ ERRO ao criar arquivo Excel")
        print("💡 Verifique se o arquivo CSV está correto e tente novamente")

def executar_scraper_completo():
    """Executa o scraper completo com geração de Excel"""
    print("\n🕷️ EXECUTANDO SCRAPER COMPLETO COM EXCEL")
    print("-" * 40)
    
    url = input("Digite a URL do Zap Imóveis para análise: ").strip()
    
    if not url:
        print("❌ URL não fornecida!")
        return
    
    try:
        max_paginas = int(input("Quantas páginas processar? (padrão: 5): ") or "5")
    except ValueError:
        max_paginas = 5
    
    print(f"\n🔄 Iniciando extração de dados...")
    print(f"📄 Páginas a processar: {max_paginas}")
    print("⏳ Aguarde enquanto coletamos os dados...")
    
    # Executar scraper (agora gera Excel automaticamente)
    scraper = ZapScraper()
    df_resultado = scraper.analisar_site(url, max_paginas)
    
    if df_resultado is not None and not df_resultado.empty:
        print(f"\n🎉 SCRAPER CONCLUÍDO COM SUCESSO!")
        print(f"📊 Total de imóveis coletados: {len(df_resultado)}")
        print(f"📁 Arquivos gerados:")
        
        # Listar arquivos CSV e Excel gerados
        arquivos_gerados = [f for f in os.listdir('.') if f.startswith('dados_final_') or f.startswith('dados_zap_formatado_')]
        for arquivo in sorted(arquivos_gerados)[-2:]:  # Últimos 2 arquivos
            tamanho = os.path.getsize(arquivo) / 1024
            tipo = "Excel" if arquivo.endswith('.xlsx') else "CSV"
            print(f"  📄 {arquivo} ({tipo}, {tamanho:.1f} KB)")
    else:
        print("\n❌ ERRO na execução do scraper")
        print("💡 Verifique a URL e tente novamente")

def executar_scraper_automatico():
    """Executa o scraper automático sem interação do usuário"""
    print("\n🤖 EXECUTANDO SCRAPER AUTOMÁTICO")
    print("-" * 40)
    
    # URL de exemplo - você pode alterar esta URL
    url_exemplo = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/"
    
    print(f"🔗 URL: {url_exemplo}")
    print("📄 Páginas: 3 (padrão)")
    print("⏳ Iniciando processo automático...")
    print("💡 Para parar: feche o navegador")
    
    try:
        # Criar scraper e executar
        scraper = ZapScraper()
        df_resultado = scraper.analisar_site(url_exemplo, max_paginas=3)
        
        if df_resultado is not None and not df_resultado.empty:
            print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
            print(f"📊 Total de imóveis coletados: {len(df_resultado)}")
            print(f"📁 Arquivos gerados:")
            
            # Listar arquivos gerados
            arquivos_gerados = [f for f in os.listdir('.') if f.startswith('dados_final_') or f.startswith('dados_zap_formatado_')]
            for arquivo in sorted(arquivos_gerados)[-2:]:  # Últimos 2 arquivos
                tamanho = os.path.getsize(arquivo) / 1024
                tipo = "Excel" if arquivo.endswith('.xlsx') else "CSV"
                print(f"  📄 {arquivo} ({tipo}, {tamanho:.1f} KB)")
            
            print(f"\n✅ O arquivo Excel contém análises completas dos dados!")
            
        else:
            print("\n❌ ERRO: Nenhum dado foi coletado")
            
    except Exception as e:
        print(f"\n❌ ERRO durante a execução: {e}")

def mostrar_resultado_excel(excel_gerado):
    """Mostra informações sobre o arquivo Excel gerado"""
    print(f"\n🎉 SUCESSO!")
    print(f"📊 Arquivo Excel criado: {excel_gerado}")
    print(f"📁 Localização: {os.path.abspath(excel_gerado)}")
    
    # Mostrar informações do arquivo
    tamanho_excel = os.path.getsize(excel_gerado) / 1024  # KB
    print(f"💾 Tamanho do arquivo: {tamanho_excel:.1f} KB")
    
    print(f"\n📋 O arquivo Excel contém as seguintes abas:")
    print(f"  📊 Dados Completos - Todos os imóveis coletados")
    print(f"  📈 Resumo Estatístico - Métricas gerais")
    print(f"  💰 Análise de Preços - Distribuição por faixas de preço")
    print(f"  🏠 Análise de Áreas - Distribuição por faixas de área")
    print(f"  🏆 Top Imóveis - Melhores preços por m²")
    print(f"  🔍 Filtros Especiais - Imóveis com características específicas")

if __name__ == "__main__":
    main()
