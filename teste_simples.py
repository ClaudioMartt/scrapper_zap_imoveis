#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples do scraper para identificar problemas
"""

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

warnings.filterwarnings("ignore")

def teste_basico():
    """Teste básico do scraper"""
    print("🧪 Teste básico do scraper...")
    
    driver = None
    try:
        # Configuração simples do driver
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
        
        print("Criando driver...")
        driver = uc.Chrome(options=options)
        print("✅ Driver criado com sucesso!")
        
        # Configurar timeout
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        # Definir tamanho da janela
        driver.set_window_size(1200, 800)
        
        # URL de teste
        url = "https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo/"
        print(f"🌐 Acessando: {url}")
        
        driver.get(url)
        time.sleep(5)
        
        print("🔍 Procurando elementos...")
        
        # Aguardar carregamento
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flex.flex-col.grow.min-w-0"))
            )
            print("✅ Elementos carregados!")
        except Exception as e:
            print(f"❌ Erro ao aguardar elementos: {e}")
            return False
        
        # Fazer scroll simples
        print("📜 Fazendo scroll...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Procurar elementos
        elementos = driver.find_elements(By.CLASS_NAME, "flex.flex-col.grow.min-w-0")
        print(f"📊 Encontrados {len(elementos)} elementos")
        
        if len(elementos) > 0:
            print("✅ Sucesso! Elementos encontrados")
            
            # Testar extração de dados do primeiro elemento
            try:
                primeiro_elemento = elementos[0]
                html_content = primeiro_elemento.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Procurar preço
                preco_element = soup.find("p", class_="text-2-25 text-feedback-success-110 font-semibold")
                if not preco_element:
                    preco_element = soup.find("p", class_="text-2-25 text-neutral-120 font-semibold")
                
                if preco_element:
                    preco_texto = preco_element.text.strip()
                    print(f"💰 Preço encontrado: {preco_texto}")
                else:
                    print("❌ Preço não encontrado")
                
                # Procurar localização
                localizacao_element = soup.find("h2", {"data-cy": "rp-cardProperty-location-txt"})
                if localizacao_element:
                    localizacao = localizacao_element.text.strip()
                    print(f"📍 Localização: {localizacao}")
                else:
                    print("❌ Localização não encontrada")
                
                return True
                
            except Exception as e:
                print(f"❌ Erro ao extrair dados: {e}")
                return False
        else:
            print("❌ Nenhum elemento encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                print("🔒 Driver fechado")
            except:
                pass

if __name__ == "__main__":
    sucesso = teste_basico()
    if sucesso:
        print("\n🎉 Teste básico passou!")
        print("💡 O problema pode estar na lógica de scroll ou extração de dados")
    else:
        print("\n⚠️ Teste básico falhou")
        print("💡 Verifique se o Chrome está instalado e atualizado")