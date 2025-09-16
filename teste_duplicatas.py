#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a funcionalidade de detecção de duplicatas
"""

import pandas as pd
from zap_scraper import ZapScraper

def testar_deteccao_duplicatas():
    """Testa a detecção de duplicatas com dados simulados"""
    
    print("🧪 TESTE DE DETECÇÃO DE DUPLICATAS")
    print("=" * 50)
    
    # Criar scraper
    scraper = ZapScraper()
    
    # Dados simulados (alguns duplicados)
    dados_teste = [
        {
            'Descrição': 'Apartamento para comprar com 43 m², 3 quartos, 2 banheiros, 1 vaga em Vila Regente Feijó, São Paulo',
            'Endereco': 'Rua Emília Marengo',
            'M2': 43.0,
            'Preco': 159600.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'R$/M2': 3711.63
        },
        {
            'Descrição': 'Apartamento para comprar com 69 m², 3 quartos, 2 banheiros, 1 vaga em Itaquera, São Paulo',
            'Endereco': 'Rua Subragi',
            'M2': 69.0,
            'Preco': 200000.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'R$/M2': 2898.55
        },
        # DUPLICATA do primeiro imóvel
        {
            'Descrição': 'Apartamento para comprar com 43 m², 3 quartos, 2 banheiros, 1 vaga em Vila Regente Feijó, São Paulo',
            'Endereco': 'Rua Emília Marengo',
            'M2': 43.0,
            'Preco': 159600.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'R$/M2': 3711.63
        },
        # DUPLICATA do segundo imóvel
        {
            'Descrição': 'Apartamento para comprar com 69 m², 3 quartos, 2 banheiros, 1 vaga em Itaquera, São Paulo',
            'Endereco': 'Rua Subragi',
            'M2': 69.0,
            'Preco': 200000.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'R$/M2': 2898.55
        },
        {
            'Descrição': 'Apartamento para comprar com 55 m², 3 quartos, 2 banheiros, 1 vaga em Jardim Capelinha, São Paulo',
            'Endereco': 'Rua Guilherme Jerônimo Klosternecht',
            'M2': 55.0,
            'Preco': 185000.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'R$/M2': 3363.64
        }
    ]
    
    print(f"📊 Testando com {len(dados_teste)} imóveis (incluindo duplicatas)")
    print("\n🔄 Processando dados...")
    
    # Resetar contadores
    scraper.resetar_contadores_duplicatas()
    
    # Simular processamento
    dados_unicos = []
    for i, dados in enumerate(dados_teste, 1):
        print(f"\nProcessando imóvel {i}/{len(dados_teste)}: {dados['Descrição'][:50]}...")
        
        if not scraper.verificar_duplicata(dados):
            dados_unicos.append(dados)
            print("✅ Imóvel único - adicionado")
        else:
            print("🔄 Duplicata detectada - ignorada")
    
    # Mostrar resultados
    print(f"\n📈 RESULTADOS DO TESTE:")
    print(f"🏠 Imóveis únicos coletados: {len(dados_unicos)}")
    print(f"🔄 Duplicatas detectadas: {scraper.duplicatas_detectadas}")
    print(f"📋 Total processado: {len(dados_teste)}")
    
    stats = scraper.obter_estatisticas_duplicatas()
    print(f"📊 Taxa de duplicatas: {stats['taxa_duplicatas']:.1f}%")
    
    # Verificar se funcionou corretamente
    if len(dados_unicos) == 3 and scraper.duplicatas_detectadas == 2:
        print("\n✅ TESTE PASSOU! Detecção de duplicatas funcionando corretamente.")
    else:
        print(f"\n❌ TESTE FALHOU! Esperado: 3 únicos, 2 duplicatas. Obtido: {len(dados_unicos)} únicos, {scraper.duplicatas_detectadas} duplicatas.")
    
    return len(dados_unicos), scraper.duplicatas_detectadas

def testar_com_csv_existente():
    """Testa com um arquivo CSV existente que tem duplicatas"""
    
    print("\n🧪 TESTE COM CSV EXISTENTE")
    print("=" * 50)
    
    try:
        # Ler arquivo CSV existente
        df = pd.read_csv('dados_parciais_20250916-104548.csv')
        print(f"📁 Arquivo carregado: {len(df)} registros")
        
        # Criar scraper
        scraper = ZapScraper()
        scraper.resetar_contadores_duplicatas()
        
        # Simular processamento
        dados_unicos = []
        duplicatas = 0
        
        for i, row in df.iterrows():
            dados = row.to_dict()
            
            if not scraper.verificar_duplicata(dados):
                dados_unicos.append(dados)
            else:
                duplicatas += 1
        
        print(f"\n📈 RESULTADOS:")
        print(f"🏠 Imóveis únicos: {len(dados_unicos)}")
        print(f"🔄 Duplicatas detectadas: {duplicatas}")
        print(f"📋 Total original: {len(df)}")
        
        taxa_reducao = ((len(df) - len(dados_unicos)) / len(df)) * 100
        print(f"📊 Taxa de redução: {taxa_reducao:.1f}%")
        
        if duplicatas > 0:
            print("\n✅ Duplicatas detectadas com sucesso!")
        else:
            print("\nℹ️ Nenhuma duplicata detectada neste arquivo.")
            
    except FileNotFoundError:
        print("❌ Arquivo CSV não encontrado. Execute primeiro o scraper.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    # Executar testes
    testar_deteccao_duplicatas()
    testar_com_csv_existente()
    
    print("\n🎉 Testes concluídos!")
