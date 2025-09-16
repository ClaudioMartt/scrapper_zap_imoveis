#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Automático do Zap Imóveis com Geração Automática de Excel
Executa o scraping e gera automaticamente um arquivo Excel formatado
"""

import sys
from zap_scraper import ZapScraper

def executar_scraper_automatico(url, max_paginas=5):
    """
    Executa o scraper automaticamente com geração de Excel
    
    Args:
        url (str): URL do Zap Imóveis para análise
        max_paginas (int): Número de páginas para processar
    
    Returns:
        pandas.DataFrame: DataFrame com os dados coletados ou None se houver erro
    """
    print("🏠 SCRAPER AUTOMÁTICO ZAP IMÓVEIS")
    print("=" * 40)
    print(f"🔗 URL: {url}")
    print(f"📄 Páginas: {max_paginas}")
    print("⏳ Iniciando processo automático...")
    
    try:
        # Criar instância do scraper
        scraper = ZapScraper()
        
        # Executar análise completa (inclui geração automática de Excel)
        df_resultado = scraper.analisar_site(url, max_paginas)
        
        if df_resultado is not None and not df_resultado.empty:
            print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
            print(f"📊 Total de imóveis coletados: {len(df_resultado)}")
            print(f"📁 Arquivos gerados automaticamente:")
            
            # Listar arquivos gerados
            import os
            arquivos_gerados = [f for f in os.listdir('.') if f.startswith('dados_final_') or f.startswith('dados_zap_formatado_')]
            for arquivo in sorted(arquivos_gerados)[-2:]:  # Últimos 2 arquivos
                tamanho = os.path.getsize(arquivo) / 1024
                tipo = "Excel" if arquivo.endswith('.xlsx') else "CSV"
                print(f"  📄 {arquivo} ({tipo}, {tamanho:.1f} KB)")
            
            print(f"\n✅ O arquivo Excel contém análises completas dos dados!")
            return df_resultado
        else:
            print("\n❌ ERRO: Nenhum dado foi coletado")
            return None
            
    except Exception as e:
        print(f"\n❌ ERRO durante a execução: {e}")
        return None

def main():
    """Função principal para execução via linha de comando"""
    if len(sys.argv) < 2:
        print("❌ Uso: python scraper_automatico.py <URL> [max_paginas]")
        print("📝 Exemplo: python scraper_automatico.py 'https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/' 3")
        return
    
    url = sys.argv[1]
    max_paginas = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # Executar scraper automático
    resultado = executar_scraper_automatico(url, max_paginas)
    
    if resultado is not None:
        print(f"\n🎯 Processo finalizado com sucesso!")
        print(f"📈 {len(resultado)} imóveis processados")
    else:
        print(f"\n💥 Processo falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()
