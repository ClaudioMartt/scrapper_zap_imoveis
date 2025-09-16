#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples da funcionalidade de detecção de duplicatas
"""

from zap_scraper import ZapScraper

def teste_basico():
    """Teste básico da detecção de duplicatas"""
    
    print("🧪 TESTE BÁSICO - DETECÇÃO DE DUPLICATAS")
    print("=" * 50)
    
    # Criar scraper
    scraper = ZapScraper()
    
    # Dados de teste
    dados1 = {
        'Descrição': 'Apartamento para comprar com 43 m², 3 quartos, 2 banheiros, 1 vaga em Vila Regente Feijó, São Paulo',
        'Endereco': 'Rua Emília Marengo',
        'M2': 43.0,
        'Preco': 159600.0,
        'Quartos': 3,
        'Banheiros': 2,
        'Vagas': 1,
        'R$/M2': 3711.63
    }
    
    dados2 = {
        'Descrição': 'Apartamento para comprar com 69 m², 3 quartos, 2 banheiros, 1 vaga em Itaquera, São Paulo',
        'Endereco': 'Rua Subragi',
        'M2': 69.0,
        'Preco': 200000.0,
        'Quartos': 3,
        'Banheiros': 2,
        'Vagas': 1,
        'R$/M2': 2898.55
    }
    
    print("🔄 Testando primeiro imóvel...")
    resultado1 = scraper.verificar_duplicata(dados1)
    print(f"Resultado: {'Duplicata' if resultado1 else 'Único'}")
    
    print("\n🔄 Testando segundo imóvel (diferente)...")
    resultado2 = scraper.verificar_duplicata(dados2)
    print(f"Resultado: {'Duplicata' if resultado2 else 'Único'}")
    
    print("\n🔄 Testando primeiro imóvel novamente (deve ser duplicata)...")
    resultado3 = scraper.verificar_duplicata(dados1)
    print(f"Resultado: {'Duplicata' if resultado3 else 'Único'}")
    
    # Mostrar estatísticas
    stats = scraper.obter_estatisticas_duplicatas()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"Imóveis únicos: {stats['imoveis_unicos']}")
    print(f"Duplicatas detectadas: {stats['duplicatas_detectadas']}")
    print(f"Total processado: {stats['total_processados']}")
    print(f"Taxa de duplicatas: {stats['taxa_duplicatas']:.1f}%")
    
    # Verificar se funcionou
    if stats['imoveis_unicos'] == 2 and stats['duplicatas_detectadas'] == 1:
        print("\n✅ TESTE PASSOU! Detecção funcionando corretamente.")
    else:
        print(f"\n❌ TESTE FALHOU! Esperado: 2 únicos, 1 duplicata.")
    
    return stats

if __name__ == "__main__":
    teste_basico()
