"""
Exemplo de uso do ZapScraper
Este arquivo demonstra como usar a classe ZapScraper diretamente
"""

from zap_scraper import ZapScraper
import pandas as pd

def exemplo_basico():
    """Exemplo básico de uso do scraper"""
    
    # URL de exemplo (substitua pela URL real)
    url_exemplo = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/?pagina=1"
    
    # Criar instância do scraper
    scraper = ZapScraper()
    
    print("Iniciando scraping...")
    
    # Extrair dados (máximo 3 páginas para teste)
    df = scraper.extrair_dados_pagina(url_exemplo, max_paginas=3)
    
    if df is not None and not df.empty:
        print(f"\n✅ Coletados {len(df)} imóveis!")
        
        # Mostrar primeiras linhas
        print("\n📋 Primeiras linhas dos dados:")
        print(df.head())
        
        # Calcular estatísticas
        print("\n📊 Estatísticas:")
        stats = scraper.calcular_estatisticas(df)
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Remover outliers
        print("\n🧹 Removendo outliers...")
        df_limpo = scraper.remover_outliers_iterativo(df)
        print(f"Dados após limpeza: {len(df_limpo)} imóveis")
        
        # Salvar dados
        # Criar pasta arquivos se não existir
        pasta_arquivos = "arquivos"
        if not os.path.exists(pasta_arquivos):
            os.makedirs(pasta_arquivos)
        
        caminho_csv = os.path.join(pasta_arquivos, 'exemplo_dados_limpos.csv')
        df_limpo.to_csv(caminho_csv, index=False)
        print("✅ Dados salvos em 'exemplo_dados_limpos.csv'")
        
    else:
        print("❌ Nenhum dado foi coletado")

def exemplo_com_filtros():
    """Exemplo com filtros personalizados"""
    
    # URL de exemplo
    url_exemplo = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/?pagina=1"
    
    # Criar instância do scraper
    scraper = ZapScraper()
    
    print("Iniciando scraping com filtros...")
    
    # Extrair dados
    df = scraper.extrair_dados_pagina(url_exemplo, max_paginas=2)
    
    if df is not None and not df.empty:
        print(f"\n✅ Coletados {len(df)} imóveis!")
        
        # Filtros personalizados
        if 'Quartos' in df.columns:
            df_2_quartos = df[df['Quartos'] == 2]
            print(f"Imóveis com 2 quartos: {len(df_2_quartos)}")
        
        if 'R$/M2' in df.columns:
            df_preco_medio = df[df['R$/M2'] <= df['R$/M2'].mean()]
            print(f"Imóveis com preço abaixo da média: {len(df_preco_medio)}")
        
        # Salvar dados filtrados
        caminho_csv = os.path.join(pasta_arquivos, 'exemplo_dados_filtrados.csv')
        df.to_csv(caminho_csv, index=False)
        print("✅ Dados filtrados salvos em 'exemplo_dados_filtrados.csv'")

if __name__ == "__main__":
    print("🏠 Exemplo de uso do ZapScraper")
    print("=" * 50)
    
    try:
        # Executar exemplo básico
        exemplo_basico()
        
        print("\n" + "=" * 50)
        
        # Executar exemplo com filtros
        exemplo_com_filtros()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("Certifique-se de ter o Chrome instalado e uma conexão com internet")
