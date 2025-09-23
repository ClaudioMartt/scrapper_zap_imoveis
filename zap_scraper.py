import pandas as pd
import re
import numpy as np
import time
import random
import os
from scipy.stats import zscore
import warnings
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from excel_formatter import ExcelFormatter
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore")

class ZapScraper:
    def __init__(self):
        self.driver = None
        self.data_list = []
        self.debug = True  # Ativar debug para análise
        self.excel_formatter = ExcelFormatter()
        self.imoveis_unicos = set()  # Set para armazenar identificadores únicos
        self.duplicatas_detectadas = 0  # Contador de duplicatas
    
    def criar_identificador_imovel(self, dados):
        """Cria um identificador único para o imóvel baseado em suas características"""
        try:
            # Usar características principais para criar identificador único
            identificador_parts = []
            
            # Descrição (sem "Apartamento para comprar com" para normalizar)
            if 'Descrição' in dados:
                descricao = dados['Descrição'].replace("Apartamento para comprar com", "").strip()
                identificador_parts.append(descricao)
            
            # Endereço
            if 'Endereco' in dados and dados['Endereco']:
                identificador_parts.append(dados['Endereco'].strip())
            
            # Área (m²)
            if 'M2' in dados:
                identificador_parts.append(f"{dados['M2']:.1f}")
            
            # Preço
            if 'Preco' in dados:
                identificador_parts.append(f"{dados['Preco']:.0f}")
            
            # Quartos, banheiros, vagas
            if 'Quartos' in dados:
                identificador_parts.append(f"Q{dados['Quartos']}")
            if 'Banheiros' in dados:
                identificador_parts.append(f"B{dados['Banheiros']}")
            if 'Vagas' in dados:
                identificador_parts.append(f"V{dados['Vagas']}")
            
            # Criar hash do identificador
            identificador = "|".join(identificador_parts)
            return hash(identificador)
            
        except Exception as e:
            print(f"Erro ao criar identificador: {e}")
            return None
    
    def verificar_duplicata(self, dados):
        """Verifica se o imóvel já foi coletado anteriormente"""
        try:
            identificador = self.criar_identificador_imovel(dados)
            if identificador is None:
                return True  # Se não conseguir criar identificador, considera duplicata
            
            if identificador in self.imoveis_unicos:
                self.duplicatas_detectadas += 1
                print(f"\n🔄 Duplicata detectada! Total de duplicatas: {self.duplicatas_detectadas}")
                return True
            else:
                self.imoveis_unicos.add(identificador)
                return False
                
        except Exception as e:
            print(f"Erro ao verificar duplicata: {e}")
            return True  # Em caso de erro, considera duplicata para segurança
    
    def resetar_contadores_duplicatas(self):
        """Reseta os contadores de duplicatas para uma nova execução"""
        self.imoveis_unicos.clear()
        self.duplicatas_detectadas = 0
        print("🔄 Contadores de duplicatas resetados")
    
    def obter_estatisticas_duplicatas(self):
        """Retorna estatísticas sobre duplicatas detectadas"""
        total_processados = len(self.imoveis_unicos) + self.duplicatas_detectadas
        taxa_duplicatas = (self.duplicatas_detectadas / total_processados * 100) if total_processados > 0 else 0
        
        return {
            'imoveis_unicos': len(self.imoveis_unicos),
            'duplicatas_detectadas': self.duplicatas_detectadas,
            'total_processados': total_processados,
            'taxa_duplicatas': taxa_duplicatas
        }
    
    def verificar_chrome_instalado(self):
        """Verifica se o Chrome está instalado no sistema"""
        try:
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', ''))
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    print(f"Chrome encontrado em: {path}")
                    return True
            
            print("Chrome não encontrado. Por favor, instale o Google Chrome.")
            return False
        except Exception as e:
            print(f"Erro ao verificar Chrome: {e}")
            return False
    
    def _criar_driver_com_opcoes(self, version_main=None):
        """Cria um novo driver com opções frescas para evitar reutilização"""
        options = uc.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configurações adicionais para evitar crashes
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-ipc-flooding-protection')
        
        if version_main is not None:
            return uc.Chrome(options=options, version_main=version_main)
        else:
            return uc.Chrome(options=options)

    def configure_driver(self):
        """Configura o driver do Chrome com opções para evitar detecção"""
        try:
            # Verificar se o Chrome está instalado
            if not self.verificar_chrome_instalado():
                return False
            
            # Configuração simples e robusta
            options = uc.ChromeOptions()
            ua = UserAgent()
            user_agent = ua.random
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Tentar criar o driver
            try:
                print("Tentando criar driver...")
                self.driver = uc.Chrome(options=options)
                print("Driver criado com sucesso!")
                
                # Configurar timeout e outras propriedades
                self.driver.set_page_load_timeout(30)
                self.driver.implicitly_wait(10)
                
                width = random.randint(1050, 1200)
                height = random.randint(800, 960)
                self.driver.set_window_size(width, height)
                
                # Executar script para ocultar automação
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                return True
                
            except Exception as e:
                print(f"Erro ao criar driver: {e}")
                return False
                
        except Exception as e:
            print(f"Erro ao configurar o driver: {e}")
            return False
    
    def add_random_actions(self):
        """Adiciona ações aleatórias para simular comportamento humano"""
        try:
            self.driver.execute_script("""
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': arguments[0],
                    'clientY': arguments[1]
                });
                document.dispatchEvent(event);
            """, random.randint(0, 800), random.randint(0, 600))
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"Erro nas ações aleatórias: {e}")
    
    def verificar_carregamento_completo(self, timeout=15):
        """Verifica se a página carregou completamente"""
        print("\nVerificando carregamento completo...")
        last_count = 0
        stable_count = 0
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            elementos = self.driver.find_elements(By.CLASS_NAME, "flex.flex-col.grow.min-w-0")
            current_count = len(elementos)
            print(f"\rElementos encontrados: {current_count}", end="")
            
            if current_count == last_count:
                stable_count += 1
                if stable_count >= 3:
                    print(f"\nCarregamento estabilizou com {current_count} elementos")
                    return current_count
            else:
                stable_count = 0
                last_count = current_count
                start_time = time.time()
            
            time.sleep(1)
        
        print(f"\nTimeout atingido. Último número de elementos: {last_count}")
        return last_count
    
    def scroll_page(self):
        """Faz scroll na página para carregar todos os elementos"""
        try:
            print("Iniciando scroll da página...")
            
            # Scroll simples e eficaz
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Verificar quantos elementos temos agora
            elementos = self.driver.find_elements(By.CLASS_NAME, "flex.flex-col.grow.min-w-0")
            print(f"Elementos encontrados após scroll: {len(elementos)}")
            
            return len(elementos)
            
        except Exception as e:
            print(f"Erro durante a rolagem: {e}")
            return 0
    
    def extrair_dados_anuncio(self, anuncio_soup):
        """Extrai dados de um anúncio específico"""
        dados = {}
        
        try:
            # Extrai localização - voltar ao seletor original
            localizacao_element = anuncio_soup.find("h2", {"data-cy": "rp-cardProperty-location-txt"})
            if localizacao_element:
                dados['Descrição'] = localizacao_element.text.strip().replace("Apartamento para comprar em", "").strip()
                
            # Extrai endereço - voltar ao seletor original
            endereco_element = anuncio_soup.find("p", {"data-cy": "rp-cardProperty-street-txt"})
            if endereco_element:
                dados['Endereco'] = endereco_element.text.strip()
                
            # Extrai área (m²)
            area_element = anuncio_soup.find("li", attrs={"data-cy": "rp-cardProperty-propertyArea-txt"})
            if area_element:
                area_text = area_element.text.strip()
                match = re.search(r'(\d+(?:\.|,)?\d*)\s*m²', area_text)
                if match:
                    area_str = match.group(1).replace('.', '').replace(',', '.')
                    dados['M2'] = float(area_str)
            
            # Método alternativo para encontrar área
            if 'M2' not in dados:
                for elemento in anuncio_soup.find_all(['li', 'span', 'h3']):
                    if elemento.text and 'm²' in elemento.text:
                        match = re.search(r'(\d+(?:\.|,)?\d*)\s*m²', elemento.text)
                        if match:
                            area_str = match.group(1).replace('.', '').replace(',', '.')
                            dados['M2'] = float(area_str)
                            break

            # Extrai características (quartos, banheiros, vagas)
            caracteristicas = anuncio_soup.find_all("li", class_="flex row items-center gap-0-5")
            for item in caracteristicas:
                texto = item.text.strip()
                if item.get('data-cy') == 'rp-cardProperty-bedroomQuantity-txt':
                    dados['Quartos'] = int(re.search(r'(\d+)', texto).group(1))
                elif item.get('data-cy') == 'rp-cardProperty-bathroomQuantity-txt':
                    dados['Banheiros'] = int(re.search(r'(\d+)', texto).group(1))
                elif item.get('data-cy') == 'rp-cardProperty-parkingSpacesQuantity-txt':
                    dados['Vagas'] = int(re.search(r'(\d+)', texto).group(1))
                    
            # Extrai preço
            preco = None
            
            # Primeira tentativa: classe específica
            preco_element = anuncio_soup.find("p", class_="text-2-25 text-feedback-success-110 font-semibold")
            if not preco_element:
                preco_element = anuncio_soup.find("p", class_="text-2-25 text-neutral-120 font-semibold")
            
            if preco_element:
                preco_texto = preco_element.text.strip()
                preco_match = re.search(r'R\$\s*([\d.,]+)', preco_texto)
                if preco_match:
                    preco = float(preco_match.group(1).replace('.', '').replace(',', '.'))
            
            # Segunda tentativa: procura por qualquer elemento com padrão de preço
            if not preco:
                for elemento in anuncio_soup.find_all(['p', 'span', 'div']):
                    texto = elemento.text.strip()
                    if 'R$' in texto and len(texto) < 50:
                        preco_match = re.search(r'R\$\s*([\d.,]+)', texto)
                        if preco_match:
                            preco = float(preco_match.group(1).replace('.', '').replace(',', '.'))
                            break
            
            if preco:
                dados['Preco'] = preco
            else:
                print("\nNão foi possível encontrar o preço do imóvel")
                return None
                
            # Extrai taxas (condomínio e IPTU)
            taxas_element = anuncio_soup.find("p", class_="text-1-75 text-neutral-110")
            if taxas_element:
                taxas_texto = taxas_element.text.strip()
                cond_match = re.search(r'Cond\.\s*R\$\s*([\d.,]+)', taxas_texto)
                iptu_match = re.search(r'IPTU\s*R\$\s*([\d.,]+)', taxas_texto)
                
                if cond_match:
                    dados['Condominio'] = float(cond_match.group(1).replace('.', '').replace(',', '.'))
                if iptu_match:
                    dados['IPTU'] = float(iptu_match.group(1).replace('.', '').replace(',', '.'))
            
            # Calcula preço por m²
            if 'Preco' in dados and 'M2' in dados and dados['M2'] > 0:
                dados['R$/M2'] = dados['Preco'] / dados['M2']
            
            # Extrai URL do anúncio - abordagem simplificada
            url_encontrada = None
            
            # Tentar encontrar o link do anúncio usando seletores específicos do Zap Imóveis
            # O Zap Imóveis geralmente tem a URL no elemento <a> que envolve o card do imóvel
            
            # Tentativa 1: Procurar por link que contenha '/imovel/'
            for link in anuncio_soup.find_all("a", href=True):
                href = link.get('href')
                if href and '/imovel/' in href:
                    if href.startswith('/'):
                        url_encontrada = f"https://www.zapimoveis.com.br{href}"
                    else:
                        url_encontrada = href
                    break
            
            # Tentativa 2: Procurar por qualquer link que pareça ser de imóvel
            if not url_encontrada:
                for link in anuncio_soup.find_all("a", href=True):
                    href = link.get('href')
                    if href and len(href) > 20:  # URLs de imóveis são geralmente longas
                        # Verificar se contém padrões típicos de URLs de imóveis
                        if any(palavra in href.lower() for palavra in ['imovel', 'casa', 'apartamento', 'venda', 'aluguel', 'sp+', 'rj+', 'mg+']):
                            if href.startswith('/'):
                                url_encontrada = f"https://www.zapimoveis.com.br{href}"
                            else:
                                url_encontrada = href
                            break
            
            # Tentativa 3: Se ainda não encontrou, usar o primeiro link que não seja de navegação
            if not url_encontrada:
                for link in anuncio_soup.find_all("a", href=True):
                    href = link.get('href')
                    # Ignorar links de navegação, redes sociais, etc.
                    if href and not any(palavra in href.lower() for palavra in ['facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp', 'mailto:', 'tel:', '#', 'javascript:']):
                        if href.startswith('/') and len(href) > 10:
                            url_encontrada = f"https://www.zapimoveis.com.br{href}"
                            break
                        elif 'zap' in href and len(href) > 20:
                            url_encontrada = href
                            break
            
            if url_encontrada:
                dados['URL'] = url_encontrada
            else:
                # Se não conseguir extrair URL real, criar uma URL genérica baseada nos dados
                endereco_limpo = dados.get('Endereco', '').replace(' ', '-').lower()
                cidade_limpa = dados.get('Descrição', '').split(',')[0].replace(' ', '-').lower() if dados.get('Descrição') else 'local'
                dados['URL'] = f"https://www.zapimoveis.com.br/venda/imovel/{cidade_limpa}/{endereco_limpo}/"
                
        except Exception as e:
            print(f"\nErro ao extrair dados do anúncio: {e}")
            return None
            
        return dados
    
    def extrair_dados_pagina(self, url, max_paginas=10):
        """Extrai dados de múltiplas páginas do Zap Imóveis"""
        self.data_list = []
        self.resetar_contadores_duplicatas()  # Resetar contadores de duplicatas
        pagina_atual = 1
        
        try:
            if not self.configure_driver():
                return None
                
            print("Driver configurado com sucesso!")
            self.driver.get(url)
            time.sleep(5)  # Aumentar tempo de espera inicial
            
            while pagina_atual <= max_paginas:
                try:
                    # Verificar se o driver ainda está ativo
                    self.driver.current_url
                except Exception as e:
                    print(f"\nNavegador foi fechado ou perdeu conexão: {e}")
                    print("Salvando dados coletados até agora...")
                    return self.salvar_dados()
                    
                print(f"\nProcessando página {pagina_atual}")
                print("Para parar: feche o navegador")
                
                try:
                    # Aguardar carregamento da página com timeout maior
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "flex.flex-col.grow.min-w-0"))
                    )
                    
                    num_elementos = self.scroll_page()
                    if num_elementos == 0:
                        print("Nenhum elemento encontrado após scroll")
                        # Salvar HTML para debug
                        self.debug_salvar_html(f"debug_page_{pagina_atual}.html")
                        break
                        
                    print(f"\nIniciando extração de {num_elementos} elementos...")
                    
                    elementos = self.driver.find_elements(By.CLASS_NAME, "flex.flex-col.grow.min-w-0")
                    for idx, elemento in enumerate(elementos, 1):
                        try:
                            print(f"\rProcessando elemento {idx}/{num_elementos}", end="")
                            html_content = elemento.get_attribute('outerHTML')
                            soup = BeautifulSoup(html_content, 'html.parser')
                            dados = self.extrair_dados_anuncio(soup)
                            
                            if dados:
                                # Verificar se é duplicata antes de adicionar
                                if not self.verificar_duplicata(dados):
                                    self.data_list.append(dados)
                                else:
                                    print(f"\rDuplicata ignorada - elemento {idx}/{num_elementos}", end="")
                        except Exception as e:
                            print(f"\nErro ao processar elemento {idx}: {e}")
                            continue
                    
                    print(f"\nTotal de dados coletados até agora: {len(self.data_list)}")
                    
                    # Tentar encontrar botão de próxima página com múltiplos seletores
                    next_button = None
                    try:
                        # Primeira tentativa: seletor original
                        next_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="next-page"]')
                    except:
                        try:
                            # Segunda tentativa: seletor alternativo
                            next_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="próxima"]')
                        except:
                            try:
                                # Terceira tentativa: procurar por texto
                                next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Próxima') or contains(text(), 'Next')]")
                            except:
                                pass
                    
                    if next_button:
                        if not (next_button.is_enabled() and "disabled" not in next_button.get_attribute("class")):
                            print("\nNão há mais páginas para processar")
                            break
                            
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
                        time.sleep(random.uniform(1, 2))
                        next_button.click()
                        time.sleep(random.uniform(4, 6))
                        pagina_atual += 1
                    else:
                        print("\nBotão de próxima página não encontrado. Finalizando extração.")
                        break
                        
                except Exception as e:
                    print(f"\nErro ao processar página {pagina_atual}: {e}")
                    # Tentar continuar com a próxima página se possível
                    if pagina_atual < max_paginas:
                        print("Tentando continuar com a próxima página...")
                        pagina_atual += 1
                        time.sleep(5)
                        continue
                    else:
                        break
        
        except Exception as e:
            print(f"\nErro durante a extração: {e}")
        
        finally:
            try:
                if self.driver:
                    print("\nFechando navegador...")
                    self.driver.quit()
            except Exception as e:
                print(f"Erro ao fechar navegador: {e}")
        
        return self.salvar_dados()
    
    def debug_salvar_html(self, filename="debug_page.html"):
        """Salva o HTML da página atual para debug"""
        if self.debug and self.driver:
            try:
                # Verificar se a janela ainda está ativa
                self.driver.current_url
                html_content = self.driver.page_source
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"HTML salvo em {filename} para debug")
            except Exception as e:
                print(f"Erro ao salvar HTML (janela pode ter sido fechada): {e}")
    
    def salvar_dados(self):
        """Salva os dados coletados em CSV"""
        if self.data_list:
            # Criar pasta arquivos se não existir
            pasta_arquivos = "arquivos"
            if not os.path.exists(pasta_arquivos):
                os.makedirs(pasta_arquivos)
            
            df = pd.DataFrame(self.data_list)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f'dados_parciais_{timestamp}.csv'
            caminho_csv = os.path.join(pasta_arquivos, filename)
            df.to_csv(caminho_csv, index=False)
            print(f"\nDados salvos em: {caminho_csv}")
            return df
        return None
    
    def calcular_estatisticas(self, df):
        """Calcula estatísticas dos dados"""
        if 'R$/M2' in df.columns:
            media_aritmetica = df['R$/M2'].mean()
            media_ponderada = np.average(df['R$/M2'], weights=df['M2'])
            mediana = df['R$/M2'].median()
            moda = df['R$/M2'].mode()[0] if not df['R$/M2'].mode().empty else np.nan
            coef_var = df['R$/M2'].std() / df['R$/M2'].mean()
            total_linhas = len(df)

            return {
                'media_aritmetica': media_aritmetica,
                'media_ponderada': media_ponderada,
                'mediana': mediana,
                'moda': moda,
                'coef_variacao': coef_var,
                'total_linhas': total_linhas,
                'preco_medio': df['Preco'].mean() if 'Preco' in df.columns else 0,
                'area_media': df['M2'].mean() if 'M2' in df.columns else 0
            }
        return {}
    
    def remover_outliers_iqr(self, df, fator=1.5):
        """Remove outliers usando o método IQR"""
        if 'R$/M2' in df.columns:
            Q1 = df['R$/M2'].quantile(0.25)
            Q3 = df['R$/M2'].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - fator * IQR
            limite_superior = Q3 + fator * IQR
            return df[(df['R$/M2'] >= limite_inferior) & (df['R$/M2'] <= limite_superior)]
        return df
    
    def remover_outliers_zscore(self, df, threshold=3):
        """Remove outliers usando o método Z-Score"""
        if 'R$/M2' in df.columns:
            z_scores = np.abs(zscore(df['R$/M2']))
            return df[z_scores < threshold]
        return df
    
    def remover_outliers_iterativo(self, df, threshold=3, fator=1.5, max_iter=10):
        """Remove outliers usando método iterativo"""
        for _ in range(max_iter):
            df_old = df.copy()
            df = self.remover_outliers_iqr(df, fator)
            df = self.remover_outliers_zscore(df, threshold)
            if len(df) == len(df_old):
                break
        return df
    
    def analisar_site(self, url_inicial, max_paginas=10):
        """Método principal para análise completa do site"""
        try:
            print("Iniciando extração de dados...")
            print("Para parar a extração, feche o navegador")
            
            df = self.extrair_dados_pagina(url_inicial, max_paginas)
            if df is not None and not df.empty:
                # Mostrar estatísticas de duplicatas
                stats_duplicatas = self.obter_estatisticas_duplicatas()
                print(f"\n📊 ESTATÍSTICAS DE DUPLICATAS:")
                print(f"🏠 Imóveis únicos coletados: {stats_duplicatas['imoveis_unicos']}")
                print(f"🔄 Duplicatas detectadas: {stats_duplicatas['duplicatas_detectadas']}")
                print(f"📈 Taxa de duplicatas: {stats_duplicatas['taxa_duplicatas']:.1f}%")
                print(f"📋 Total processado: {stats_duplicatas['total_processados']}")
                
                print("\nEstatísticas antes da remoção de outliers:")
                stats = self.calcular_estatisticas(df)
                self.imprimir_estatisticas(stats)
                
                df_cleaned = self.remover_outliers_iterativo(df)
                
                print("\nEstatísticas após a remoção de outliers:")
                stats_cleaned = self.calcular_estatisticas(df_cleaned)
                self.imprimir_estatisticas(stats_cleaned)
                
                # Criar pasta arquivos se não existir
                pasta_arquivos = "arquivos"
                if not os.path.exists(pasta_arquivos):
                    os.makedirs(pasta_arquivos)
                
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f'dados_final_{timestamp}.csv'
                caminho_csv = os.path.join(pasta_arquivos, filename)
                df_cleaned.to_csv(caminho_csv, index=False)
                print(f"\nDados finais salvos em: {caminho_csv}")
                
                # Gerar Excel formatado automaticamente
                print("\n🔄 Gerando arquivo Excel formatado automaticamente...")
                excel_file = self.gerar_excel_formatado(df_cleaned)
                if excel_file:
                    print(f"📊 Arquivo Excel formatado criado: {excel_file}")
                    print(f"📁 Localização: {os.path.abspath(excel_file)}")
                    
                    # Mostrar informações sobre o Excel gerado
                    tamanho_excel = os.path.getsize(excel_file) / 1024  # KB
                    print(f"💾 Tamanho do arquivo Excel: {tamanho_excel:.1f} KB")
                    print(f"📋 O arquivo Excel contém 6 abas com análises detalhadas dos dados")
                else:
                    print("❌ Erro ao criar arquivo Excel")
                
                return df_cleaned
        except Exception as e:
            print(f"Erro na análise: {e}")
        
        return None
    
    def imprimir_estatisticas(self, stats):
        """Imprime as estatísticas de forma formatada"""
        if stats:
            print(f"Média Aritmética: {stats['media_aritmetica']:.2f}".replace('.', ','))
            print(f"Média Ponderada: {stats['media_ponderada']:.2f}".replace('.', ','))
            print(f"Mediana: {stats['mediana']:.2f}".replace('.', ','))
            print(f"Moda: {stats['moda']:.2f}".replace('.', ','))
            print(f"Coeficiente de Variação: {stats['coef_variacao']:.4f}".replace('.', ','))
            print(f"Total de Linhas: {stats['total_linhas']}")
            print(f"Preço Médio: R$ {stats['preco_medio']:.2f}".replace('.', ','))
            print(f"Área Média: {stats['area_media']:.2f} m²".replace('.', ','))
    
    def gerar_excel_formatado(self, df, nome_arquivo=None):
        """Gera arquivo Excel formatado com todas as abas"""
        try:
            if df is None or df.empty:
                print("❌ Nenhum dado disponível para gerar Excel")
                return None
            
            print("\n🔄 Gerando arquivo Excel formatado...")
            excel_file = self.excel_formatter.gerar_excel_formatado(df, nome_arquivo)
            
            if excel_file:
                print(f"✅ Excel formatado criado com sucesso: {excel_file}")
                return excel_file
            else:
                print("❌ Erro ao criar arquivo Excel")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao gerar Excel: {e}")
            return None

def agno_tavily():
    agent = Agent(tools=[TavilyTools()])
    agent.print_response("Search tavily for 'Higienopolis'", markdown=True)


# Função principal para uso direto
def main():
    """Função principal para executar o scraper"""
    print("🏠 SCRAPER ZAP IMÓVEIS COM EXCEL AUTOMÁTICO")
    print("=" * 50)
    
    url_inicial = input("Digite a URL do Zap Imóveis para análise: ").strip()
    
    if not url_inicial:
        print("❌ URL não fornecida!")
        return None
    
    try:
        max_paginas = int(input("Quantas páginas processar? (padrão: 5): ") or "5")
    except ValueError:
        max_paginas = 5
    
    print(f"\n🔄 Iniciando extração de dados...")
    print(f"📄 Páginas a processar: {max_paginas}")
    print("⏳ Aguarde enquanto coletamos os dados e geramos o Excel...")
    
    scraper = ZapScraper()
    df_resultado = scraper.analisar_site(url_inicial, max_paginas)
    
    if df_resultado is not None and not df_resultado.empty:
        print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"📊 Total de imóveis coletados: {len(df_resultado)}")
        print(f"📁 Arquivos gerados automaticamente:")
        
        # Listar arquivos CSV e Excel gerados
        arquivos_gerados = [f for f in os.listdir('.') if f.startswith('dados_final_') or f.startswith('dados_zap_formatado_')]
        for arquivo in sorted(arquivos_gerados)[-2:]:  # Últimos 2 arquivos
            tamanho = os.path.getsize(arquivo) / 1024
            tipo = "Excel" if arquivo.endswith('.xlsx') else "CSV"
            print(f"  📄 {arquivo} ({tipo}, {tamanho:.1f} KB)")
        
        print(f"\n✅ O arquivo Excel contém análises completas dos dados!")
        return df_resultado
    else:
        print("\n❌ ERRO na execução do scraper")
        print("💡 Verifique a URL e tente novamente")
        return None


if __name__ == "__main__":
    main()
