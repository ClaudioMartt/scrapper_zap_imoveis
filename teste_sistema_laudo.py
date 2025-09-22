#!/usr/bin/env python3
"""
Script de teste para o Sistema de Laudo de Avaliação Imobiliária
"""

import os
import sys
from datetime import datetime

def testar_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔍 Testando imports...")
    
    try:
        from laudo_formulario import LaudoFormulario
        print("✅ laudo_formulario.py - OK")
    except Exception as e:
        print(f"❌ laudo_formulario.py - ERRO: {e}")
        return False
    
    try:
        from pesquisa_localidade import PesquisaLocalidade
        print("✅ pesquisa_localidade.py - OK")
    except Exception as e:
        print(f"❌ pesquisa_localidade.py - ERRO: {e}")
        return False
    
    try:
        from gerador_laudo_docx import GeradorLaudoDocx
        print("✅ gerador_laudo_docx.py - OK")
    except Exception as e:
        print(f"❌ gerador_laudo_docx.py - ERRO: {e}")
        return False
    
    try:
        from gerador_laudo_pdf import GeradorLaudoPdf
        print("✅ gerador_laudo_pdf.py - OK")
    except Exception as e:
        print(f"❌ gerador_laudo_pdf.py - ERRO: {e}")
        return False
    
    try:
        from app_laudo_completo import AppLaudoCompleto
        print("✅ app_laudo_completo.py - OK")
    except Exception as e:
        print(f"❌ app_laudo_completo.py - ERRO: {e}")
        return False
    
    return True

def testar_dependencias():
    """Testa se as dependências estão instaladas"""
    print("\n🔍 Testando dependências...")
    
    dependencias = [
        'streamlit',
        'pandas',
        'docx',
        'agno',
        'dotenv'
    ]
    
    todas_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            todas_ok = False
    
    return todas_ok

def testar_formulario():
    """Testa o formulário de laudo"""
    print("\n🔍 Testando formulário...")
    
    try:
        from laudo_formulario import LaudoFormulario
        
        formulario = LaudoFormulario()
        
        # Simular dados
        formulario.dados_imovel = {
            'numero_matricula': '11.072',
            'cartorio': 'Comarca de Taquarituba/SP',
            'area_terreno': 201.0,
            'area_construida': 134.59,
            'loteamento': 'Jardim Santa Virgínia',
            'cidade': 'Taquarituba',
            'estado': 'SP'
        }
        
        formulario.dados_avaliador = {
            'nome': 'Jhonni Balbino da Silva',
            'creci': '296769-F',
            'cnai': '051453',
            'telefone': '(11) 98796 8206',
            'email': 'contato@avaliarapido.com.br'
        }
        
        # Testar validação
        erros = formulario.validar_dados()
        
        if not erros:
            print("✅ Validação do formulário - OK")
            return True
        else:
            print(f"❌ Validação do formulário - ERRO: {erros}")
            return False
            
    except Exception as e:
        print(f"❌ Teste do formulário - ERRO: {e}")
        return False

def testar_gerador_docx():
    """Testa o gerador de DOCX"""
    print("\n🔍 Testando gerador DOCX...")
    
    try:
        from gerador_laudo_docx import GeradorLaudoDocx
        
        gerador = GeradorLaudoDocx()
        
        # Dados de teste
        dados_imovel = {
            'numero_matricula': '11.072',
            'cartorio': 'Comarca de Taquarituba/SP, Livro nº 2 – Registro Geral',
            'area_terreno': 201.0,
            'area_construida': 134.59,
            'loteamento': 'Jardim Santa Virgínia',
            'cidade': 'Taquarituba',
            'estado': 'SP',
            'tipo_construcao': 'Alvenaria',
            'cobertura': 'Telhas'
        }
        
        dados_avaliador = {
            'nome': 'Jhonni Balbino da Silva',
            'creci': '296769-F',
            'cnai': '051453',
            'telefone': '(11) 98796 8206',
            'email': 'contato@avaliarapido.com.br',
            'website': 'www.avaliarapido.com.br',
            'data_laudo': datetime.now().date(),
            'cidade_assinatura': 'Sorocaba',
            'estado_assinatura': 'SP'
        }
        
        # Criar pasta arquivos se não existir
        if not os.path.exists('arquivos'):
            os.makedirs('arquivos')
        
        # Gerar laudo de teste
        arquivo_gerado = gerador.gerar_laudo_completo(dados_imovel, dados_avaliador)
        
        if arquivo_gerado and os.path.exists(arquivo_gerado):
            tamanho = os.path.getsize(arquivo_gerado) / 1024  # KB
            print(f"✅ Gerador DOCX - OK (arquivo: {os.path.basename(arquivo_gerado)}, {tamanho:.1f} KB)")
            return True
        else:
            print("❌ Gerador DOCX - ERRO: Arquivo não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Teste do gerador DOCX - ERRO: {e}")
        return False

def testar_gerador_excel():
    """Testa o gerador de Excel"""
    print("\n🔍 Testando gerador Excel...")
    
    try:
        from excel_formatter import ExcelFormatter
        import pandas as pd
        
        # Criar dados de teste
        dados_teste = pd.DataFrame({
            'Descrição': ['Casa teste 1', 'Casa teste 2'],
            'Endereco': ['Rua A', 'Rua B'],
            'M2': [100.0, 120.0],
            'Preco': [300000.0, 360000.0],
            'R$/M2': [3000.0, 3000.0]
        })
        
        excel_formatter = ExcelFormatter()
        
        # Criar pasta arquivos se não existir
        if not os.path.exists('arquivos'):
            os.makedirs('arquivos')
        
        # Gerar Excel de teste
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_excel = f'teste_excel_{timestamp}.xlsx'
        caminho_excel = os.path.join('arquivos', filename_excel)
        
        excel_file = excel_formatter.gerar_excel_formatado(dados_teste, caminho_excel)
        
        if excel_file and os.path.exists(excel_file):
            tamanho = os.path.getsize(excel_file) / 1024  # KB
            print(f"✅ Gerador Excel - OK (arquivo: {os.path.basename(excel_file)}, {tamanho:.1f} KB)")
            return True
        else:
            print("❌ Gerador Excel - ERRO: Arquivo não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Teste do gerador Excel - ERRO: {e}")
        return False

def testar_gerador_pdf():
    """Testa o gerador de PDF"""
    print("🔍 Testando gerador PDF...")
    
    try:
        from gerador_laudo_pdf import GeradorLaudoPdf
        
        gerador = GeradorLaudoPdf()
        
        # Dados de teste
        dados_imovel = {
            'numero_matricula': '11.072',
            'cartorio': 'Comarca de Taquarituba/SP, Livro nº 2 – Registro Geral',
            'area_terreno': 201.0,
            'area_construida': 134.59,
            'loteamento': 'Jardim Santa Virgínia',
            'cidade': 'Taquarituba',
            'estado': 'SP',
            'tipo_construcao': 'Alvenaria',
            'cobertura': 'Telhas'
        }
        
        dados_avaliador = {
            'nome': 'Jhonni Balbino da Silva',
            'creci': '296769-F',
            'cnai': '051453',
            'telefone': '(11) 98796 8206',
            'email': 'contato@avaliarapido.com.br',
            'website': 'www.avaliarapido.com.br',
            'data_laudo': datetime.now().date(),
            'cidade_assinatura': 'Sorocaba',
            'estado_assinatura': 'SP'
        }
        
        # Gerar laudo
        arquivo_gerado = gerador.gerar_laudo_completo(dados_imovel, dados_avaliador)
        
        if arquivo_gerado and os.path.exists(arquivo_gerado):
            tamanho = os.path.getsize(arquivo_gerado) / 1024  # KB
            print(f"✅ Arquivo PDF gerado: {arquivo_gerado} ({tamanho:.1f} KB)")
            return True
        else:
            print("❌ Erro ao gerar arquivo PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste do gerador PDF: {e}")
        return False

def testar_pesquisa_localidade():
    """Testa a pesquisa de localidade"""
    print("\n🔍 Testando pesquisa de localidade...")
    
    try:
        from pesquisa_localidade import PesquisaLocalidade
        
        pesquisa = PesquisaLocalidade()
        
        # Testar com dados padrão
        texto = pesquisa._gerar_texto_padrao()
        
        if texto and len(texto) > 100:
            print("✅ Pesquisa de localidade - OK (modo padrão)")
            return True
        else:
            print("❌ Pesquisa de localidade - ERRO: Texto muito curto")
            return False
            
    except Exception as e:
        print(f"❌ Teste da pesquisa de localidade - ERRO: {e}")
        return False

def testar_estrutura_arquivos():
    """Testa se a estrutura de arquivos está correta"""
    print("\n🔍 Testando estrutura de arquivos...")
    
    arquivos_necessarios = [
        'laudo_formulario.py',
        'pesquisa_localidade.py',
        'gerador_laudo_docx.py',
        'app_laudo_completo.py',
        'requirements.txt',
        'INSTRUCOES_LAUDO.md'
    ]
    
    todos_presentes = True
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_presentes = False
    
    return todos_presentes

def main():
    """Função principal de teste"""
    print("🏠 TESTE DO SISTEMA DE LAUDO DE AVALIAÇÃO IMOBILIÁRIA")
    print("=" * 60)
    
    testes = [
            ("Estrutura de Arquivos", testar_estrutura_arquivos),
            ("Dependências", testar_dependencias),
            ("Imports", testar_imports),
            ("Formulário", testar_formulario),
            ("Pesquisa Localidade", testar_pesquisa_localidade),
            ("Gerador DOCX", testar_gerador_docx),
            ("Gerador PDF", testar_gerador_pdf),
            ("Gerador Excel", testar_gerador_excel)
        ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print(f"\n{'='*20} {nome_teste.upper()} {'='*20}")
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado no teste {nome_teste}: {e}")
            resultados.append((nome_teste, False))
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    testes_ok = 0
    total_testes = len(resultados)
    
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste:.<30} {status}")
        if resultado:
            testes_ok += 1
    
    print(f"\n🎯 RESULTADO FINAL: {testes_ok}/{total_testes} testes passaram")
    
    if testes_ok == total_testes:
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("\nPara executar o sistema:")
        print("streamlit run app_laudo_completo.py")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM - VERIFIQUE OS ERROS ACIMA")
        print("\nPara resolver os problemas:")
        print("1. Instale as dependências: pip install -r requirements.txt")
        print("2. Verifique se todos os arquivos estão presentes")
        print("3. Configure as chaves de API no arquivo .env")

if __name__ == "__main__":
    main()
