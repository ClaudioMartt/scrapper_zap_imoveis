#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Simples para Executar o Scraper do Zap Imóveis
Gera automaticamente um arquivo Excel formatado ao final
"""

from zap_scraper import ZapScraper

def main():
    """Executa o scraper com configurações padrão"""
    
    # URL de exemplo - você pode alterar esta URL
    url_exemplo = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/"
    
    print("🏠 SCRAPER ZAP IMÓVEIS - EXECUÇÃO AUTOMÁTICA")
    print("=" * 50)
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
            import os
            arquivos_gerados = [f for f in os.listdir('.') if f.startswith('dados_final_') or f.startswith('dados_zap_formatado_')]
            for arquivo in sorted(arquivos_gerados)[-2:]:  # Últimos 2 arquivos
                tamanho = os.path.getsize(arquivo) / 1024
                tipo = "Excel" if arquivo.endswith('.xlsx') else "CSV"
                print(f"  📄 {arquivo} ({tipo}, {tamanho:.1f} KB)")
            
            print(f"\n✅ O arquivo Excel contém:")
            print(f"  📊 Dados Completos - Todos os imóveis")
            print(f"  📈 Resumo Estatístico - Métricas gerais")
            print(f"  💰 Análise de Preços - Por faixas")
            print(f"  🏠 Análise de Áreas - Por faixas")
            print(f"  🏆 Top Imóveis - Melhores preços/m²")
            print(f"  🔍 Filtros Especiais - Imóveis específicos")
            
        else:
            print("\n❌ ERRO: Nenhum dado foi coletado")
            
    except Exception as e:
        print(f"\n❌ ERRO durante a execução: {e}")

if __name__ == "__main__":
    main()
