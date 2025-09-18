"""
Script de teste para a URL específica que está faltando 1 imóvel
"""

from zap_scraper import ZapScraper
import time

def testar_url_especifica():
    """Testa a URL específica que está com problema"""
    
    # URL que está faltando 1 imóvel (deveria ter 3, mas só encontra 2)
    url_problema = "https://www.zapimoveis.com.br/lancamentos/apartamentos/sp+sao-paulo/pronto-para-morar/?transacao=lancamentos&onde=%2CS%C3%A3o+Paulo%2CS%C3%A3o+Paulo%2C%2C%2C%2C%2Ccity%2CBR%3ESao_Paulo%3ENULL%3ESao_Paulo%2C-23.555771%2C-46.639557%2C&tipos=apartamento_residencial&quartos=2%2C3%2C4&precoMaximo=300000&tipo=Pronto+para+morar"
    
    print("🔍 Testando URL específica com problema...")
    print(f"URL: {url_problema}")
    print("=" * 80)
    
    # Criar instância do scraper
    scraper = ZapScraper()
    
    try:
        print("🚀 Iniciando teste...")
        
        # Configurar driver
        if not scraper.configure_driver():
            print("❌ Erro ao configurar driver")
            return
        
        print("✅ Driver configurado com sucesso")
        
        # Acessar página
        scraper.driver.get(url_problema)
        time.sleep(5)  # Aguardar carregamento inicial
        
        print("✅ Página acessada")
        
        # Salvar HTML inicial para debug
        scraper.debug_salvar_html("debug_inicial.html")
        
        # Aguardar elementos carregarem
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            WebDriverWait(scraper.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy*='property']"))
            )
            print("✅ Elementos de propriedade detectados")
        except:
            print("⚠️ Timeout aguardando elementos de propriedade")
        
        # Fazer scroll
        print("\n📜 Fazendo scroll...")
        num_elementos = scraper.scroll_page()
        print(f"✅ Scroll concluído. Elementos encontrados: {num_elementos}")
        
        # Salvar HTML após scroll
        scraper.debug_salvar_html("debug_apos_scroll.html")
        
        # Testar diferentes seletores
        print("\n🔍 Testando diferentes seletores...")
        seletores_teste = [
            "flex.flex-col.grow.min-w-0",
            "[data-cy*='property-card']",
            "[data-testid*='property']",
            "[class*='property-card']",
            ".card-property",
            "[data-cy*='lancamento']",
            "[data-testid*='lancamento']",
            ".lancamento-card",
            "[class*='lancamento']"
        ]
        
        for seletor in seletores_teste:
            try:
                elementos = scraper.driver.find_elements(By.CSS_SELECTOR, seletor)
                print(f"Seletor '{seletor}': {len(elementos)} elementos")
                
                if elementos:
                    # Mostrar informações dos primeiros elementos
                    for i, elemento in enumerate(elementos[:3]):
                        try:
                            texto = elemento.text.strip()[:100]
                            print(f"  Elemento {i+1}: {texto}...")
                        except:
                            print(f"  Elemento {i+1}: [Erro ao obter texto]")
            except Exception as e:
                print(f"Seletor '{seletor}': Erro - {e}")
        
        # Tentar extrair dados
        print("\n📊 Tentando extrair dados...")
        dados = scraper.extrair_dados_pagina(url_problema, max_paginas=1)
        
        if dados is not None and not dados.empty:
            print(f"✅ Dados extraídos: {len(dados)} imóveis")
            print("\n📋 Resumo dos dados:")
            print(dados.to_string())
            
            # Salvar dados
            # Criar pasta arquivos se não existir
            pasta_arquivos = "arquivos"
            if not os.path.exists(pasta_arquivos):
                os.makedirs(pasta_arquivos)
            
            caminho_csv = os.path.join(pasta_arquivos, "teste_url_especifica.csv")
            dados.to_csv(caminho_csv, index=False)
            print("\n💾 Dados salvos em 'teste_url_especifica.csv'")
        else:
            print("❌ Nenhum dado foi extraído")
        
        # Salvar HTML final
        scraper.debug_salvar_html("debug_final.html")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        
    finally:
        try:
            if scraper.driver:
                scraper.driver.quit()
        except:
            pass

if __name__ == "__main__":
    testar_url_especifica()
