#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples do alinhamento das colunas no Excel
"""

import pandas as pd
from excel_formatter import ExcelFormatter

# Dados simples para teste
dados = [
    {
        'Descrição': 'Apartamento 43m²',
        'Endereco': 'Rua A',
        'M2': 43.0,
        'Preco': 159600.0,
        'R$/M2': 3711.63
    },
    {
        'Descrição': 'Apartamento 69m²', 
        'Endereco': 'Rua B',
        'M2': 69.0,
        'Preco': 200000.0,
        'R$/M2': 2898.55
    }
]

df = pd.DataFrame(dados)
print("📊 Dados de teste:")
print(df)

# Criar Excel
formatter = ExcelFormatter()
excel_file = formatter.gerar_excel_formatado(df, 'teste_alinhamento.xlsx')

if excel_file:
    print(f"\n✅ Excel criado: {excel_file}")
    print("📋 Verifique se as colunas estão alinhadas corretamente!")
else:
    print("\n❌ Erro ao criar Excel")
