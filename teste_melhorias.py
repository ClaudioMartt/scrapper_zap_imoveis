#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das melhorias implementadas no zap_scraper.py
"""

from zap_scraper import ZapScraper

def testar_scraper():
    """Testa o scraper com uma URL de exemplo"""
    print("🧪 Testando as melhorias do ZapScraper...")
    
    # URL de exemplo do Zap Imóveis
    url_teste = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/"
    
    # Criar instância do scraper
    scraper = ZapScraper()
    
    try:
        print(f"🔍 Testando com URL: {url_teste}")
        print("📊 Limitando a 2 páginas para teste rápido...")
        
        # Testar com apenas 2 páginas para verificar se funciona
        df_resultado = scraper.analisar_site(url_teste, max_paginas=2)
        
        if df_resultado is not None and not df_resultado.empty:
            print(f"✅ Sucesso! Coletados {len(df_resultado)} imóveis")
            print("\n📋 Primeiras 5 linhas dos dados:")
            print(df_resultado.head())
            
            print("\n📈 Estatísticas básicas:")
            stats = scraper.calcular_estatisticas(df_resultado)
            scraper.imprimir_estatisticas(stats)
            
            return True
        else:
            print("❌ Nenhum dado foi coletado")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    sucesso = testar_scraper()
    if sucesso:
        print("\n🎉 Teste concluído com sucesso!")
        print("💡 O scraper agora deve trazer mais resultados como o notebook.")
    else:
        print("\n⚠️ Teste falhou. Verifique os logs acima.")
