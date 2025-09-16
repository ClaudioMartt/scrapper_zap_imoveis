"""
Script de teste simples para verificar se o scraper está funcionando
"""

from zap_scraper import ZapScraper
import time

def teste_simples():
    """Teste simples com URL básica"""
    
    # URL simples de teste
    url_teste = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/?pagina=1"
    
    print("🔍 Teste simples do scraper...")
    print(f"URL: {url_teste}")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ZapScraper()
    
    try:
        print("🚀 Iniciando teste...")
        
        # Configurar driver
        if not scraper.configure_driver():
            print("❌ Erro ao configurar driver")
            return
        
        print("✅ Driver configurado")
        
        # Acessar página
        scraper.driver.get(url_teste)
        time.sleep(5)
        
        print("✅ Página acessada")
        
        # Aguardar elementos
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            WebDriverWait(scraper.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flex.flex-col.grow.min-w-0"))
            )
            print("✅ Elementos detectados")
        except:
            print("⚠️ Timeout aguardando elementos")
        
        # Fazer scroll
        print("\n📜 Fazendo scroll...")
        num_elementos = scraper.scroll_page()
        print(f"✅ Scroll concluído. Elementos: {num_elementos}")
        
        # Encontrar elementos
        elementos = scraper.driver.find_elements(By.CLASS_NAME, "flex.flex-col.grow.min-w-0")
        print(f"✅ Elementos encontrados para processar: {len(elementos)}")
        
        # Processar alguns elementos
        if elementos:
            print(f"\n📊 Processando primeiros {min(3, len(elementos))} elementos...")
            
            for i, elemento in enumerate(elementos[:3]):
                try:
                    from bs4 import BeautifulSoup
                    html_content = elemento.get_attribute('outerHTML')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    dados = scraper.extrair_dados_anuncio(soup)
                    
                    if dados:
                        print(f"✅ Elemento {i+1}: {dados.get('Localidade', 'N/A')} - R$ {dados.get('Preco', 'N/A')}")
                        scraper.data_list.append(dados)
                    else:
                        print(f"⚠️ Elemento {i+1}: Não retornou dados")
                except Exception as e:
                    print(f"❌ Elemento {i+1}: Erro - {e}")
        
        print(f"\n📋 Total de dados coletados: {len(scraper.data_list)}")
        
        if scraper.data_list:
            # Salvar dados
            import pandas as pd
            df = pd.DataFrame(scraper.data_list)
            df.to_csv("teste_simples.csv", index=False)
            print("💾 Dados salvos em 'teste_simples.csv'")
            
            # Mostrar resumo
            print("\n📊 Resumo dos dados:")
            print(df.to_string())
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        
    finally:
        try:
            if scraper.driver:
                scraper.driver.quit()
        except:
            pass

if __name__ == "__main__":
    teste_simples()
