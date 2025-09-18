#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a correção do alinhamento das colunas no Excel
"""

import pandas as pd
from excel_formatter import ExcelFormatter

def criar_dados_teste():
    """Cria dados de teste para verificar o alinhamento"""
    dados_teste = [
        {
            'Descrição': 'Apartamento para comprar com 43 m², 3 quartos, 2 banheiros, 1 vaga em Vila Regente Feijó, São Paulo',
            'Endereco': 'Rua Emília Marengo',
            'M2': 43.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'Preco': 159600.0,
            'Condominio': 200.0,
            'IPTU': 150.0,
            'R$/M2': 3711.63
        },
        {
            'Descrição': 'Apartamento para comprar com 69 m², 3 quartos, 2 banheiros, 1 vaga em Itaquera, São Paulo',
            'Endereco': 'Rua Subragi',
            'M2': 69.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'Preco': 200000.0,
            'Condominio': 300.0,
            'IPTU': 200.0,
            'R$/M2': 2898.55
        },
        {
            'Descrição': 'Apartamento para comprar com 55 m², 3 quartos, 2 banheiros, 1 vaga em Jardim Capelinha, São Paulo',
            'Endereco': 'Rua Guilherme Jerônimo Klosternecht',
            'M2': 55.0,
            'Quartos': 3,
            'Banheiros': 2,
            'Vagas': 1,
            'Preco': 185000.0,
            'Condominio': 250.0,
            'IPTU': 180.0,
            'R$/M2': 3363.64
        }
    ]
    
    return pd.DataFrame(dados_teste)

def testar_excel_corrigido():
    """Testa se o Excel está sendo gerado com colunas alinhadas corretamente"""
    
    print("🧪 TESTE DE CORREÇÃO DO EXCEL")
    print("=" * 50)
    
    # Criar dados de teste
    df_teste = criar_dados_teste()
    print(f"📊 Dados de teste criados: {len(df_teste)} registros")
    print(f"📋 Colunas: {list(df_teste.columns)}")
    
    # Criar Excel formatado
    print("\n🔄 Gerando Excel formatado...")
    excel_formatter = ExcelFormatter()
    # Criar pasta arquivos se não existir
    pasta_arquivos = "arquivos"
    if not os.path.exists(pasta_arquivos):
        os.makedirs(pasta_arquivos)
    
    caminho_excel = os.path.join(pasta_arquivos, 'teste_correcao_excel.xlsx')
    excel_file = excel_formatter.gerar_excel_formatado(df_teste, caminho_excel)
    
    if excel_file:
        print(f"✅ Excel criado: {excel_file}")
        print("\n📋 Verifique se as colunas estão alinhadas corretamente:")
        print("   - Descrição: Descrição completa do imóvel")
        print("   - Endereco: Nome da rua")
        print("   - M2: Área em metros quadrados")
        print("   - Quartos: Número de quartos")
        print("   - Banheiros: Número de banheiros")
        print("   - Vagas: Número de vagas")
        print("   - Preco: Preço total do imóvel")
        print("   - Condominio: Valor do condomínio")
        print("   - IPTU: Valor do IPTU")
        print("   - R$/M2: Preço por metro quadrado")
        
        # Mostrar preview dos dados
        print(f"\n📊 Preview dos dados:")
        print(df_teste.head())
        
    else:
        print("❌ Erro ao criar Excel")

if __name__ == "__main__":
    testar_excel_corrigido()
