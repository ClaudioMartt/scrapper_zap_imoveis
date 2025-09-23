import streamlit as st
import pandas as pd
from datetime import datetime
import os

class LaudoFormulario:
    def __init__(self):
        self.dados_imovel = {}
        self.dados_avaliador = {}
        
    def mostrar_formulario_imovel(self):
        """Mostra o formulário para coleta de dados do imóvel"""
        st.header("📋 Dados do Imóvel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.dados_imovel['numero_matricula'] = st.text_input(
                "Número da Matrícula",
                placeholder="Ex: 11.072",
                help="Número da matrícula do imóvel no cartório"
            )
            
            self.dados_imovel['cartorio'] = st.text_input(
                "Cartório de Registro de Imóveis",
                placeholder="Ex: Comarca de Taquarituba/SP, Livro nº 2 – Registro Geral",
                help="Informações completas do cartório"
            )
            
            self.dados_imovel['area_terreno'] = st.number_input(
                "Área do Terreno (m²)",
                min_value=0.0,
                value=201.0,
                step=0.1,
                help="Área total do terreno em metros quadrados"
            )
            
            self.dados_imovel['area_construida'] = st.number_input(
                "Área Construída (m²)",
                min_value=0.0,
                value=134.59,
                step=0.1,
                help="Área construída da edificação em metros quadrados"
            )
        
        with col2:
            self.dados_imovel['loteamento'] = st.text_input(
                "Bairro",
                placeholder="Ex: Jardim Santa Virgínia",
                help="Nome Bairro"
            )
            
            self.dados_imovel['cidade'] = st.text_input(
                "Cidade",
                placeholder="Ex: Taquarituba",
                help="Cidade onde está localizado o imóvel"
            )
            
            self.dados_imovel['estado'] = st.selectbox(
                "Estado",
                ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "PE", "CE", "PA", "MA", "AL", "PB", "RN", "SE", "TO", "MT", "MS", "RO", "AC", "AM", "RR", "AP", "DF"],
                index=0
            )
            
            self.dados_imovel['tipo_construcao'] = st.selectbox(
                "Tipo de Construção",
                ["Alvenaria", "Concreto", "Madeira", "Mista"],
                index=0
            )
            
            self.dados_imovel['cobertura'] = st.text_input(
                "Tipo de Cobertura",
                placeholder="Ex: Telhas",
                value="Telhas"
            )
    
    def mostrar_formulario_avaliador(self):
        """Mostra o formulário para dados do avaliador"""
        st.header("👤 Dados do Avaliador")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.dados_avaliador['nome'] = st.text_input(
                "Nome Completo",
                placeholder="Ex: Jhonni Balbino da Silva",
                value="Jhonni Balbino da Silva"
            )
            
            self.dados_avaliador['creci'] = st.text_input(
                "CRECI",
                placeholder="Ex: 296769-F",
                value="296769-F"
            )
            
            self.dados_avaliador['cnai'] = st.text_input(
                "CNAI",
                placeholder="Ex: 051453",
                value="051453"
            )
        
        with col2:
            self.dados_avaliador['telefone'] = st.text_input(
                "Telefone",
                placeholder="Ex: (11) 98796 8206",
                value="(11) 98796 8206"
            )
            
            self.dados_avaliador['email'] = st.text_input(
                "E-mail",
                placeholder="Ex: contato@avaliarapido.com.br",
                value="contato@avaliarapido.com.br"
            )
            
            self.dados_avaliador['website'] = st.text_input(
                "Website",
                placeholder="Ex: www.avaliarapido.com.br",
                value="www.avaliarapido.com.br"
            )
    
    def mostrar_formulario_data(self):
        """Mostra o formulário para data do laudo"""
        st.header("📅 Data do Laudo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.dados_avaliador['data_laudo'] = st.date_input(
                "Data do Laudo",
                value=datetime.now().date(),
                help="Data de referência do laudo"
            )
        
        with col2:
            self.dados_avaliador['cidade_assinatura'] = st.text_input(
                "Cidade da Assinatura",
                placeholder="Ex: Sorocaba",
                value="Sorocaba"
            )
            
            self.dados_avaliador['estado_assinatura'] = st.selectbox(
                "Estado da Assinatura",
                ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "PE", "CE", "PA", "MA", "AL", "PB", "RN", "SE", "TO", "MT", "MS", "RO", "AC", "AM", "RR", "AP", "DF"],
                index=0
            )
    
    def validar_dados(self):
        """Valida se todos os dados obrigatórios foram preenchidos"""
        campos_obrigatorios_imovel = [
            'numero_matricula', 'cartorio', 'area_terreno', 'area_construida',
            'loteamento', 'cidade', 'estado'
        ]
        
        campos_obrigatorios_avaliador = [
            'nome', 'creci', 'cnai', 'telefone', 'email'
        ]
        
        erros = []
        
        # Validar dados do imóvel
        for campo in campos_obrigatorios_imovel:
            if not self.dados_imovel.get(campo):
                erros.append(f"Campo obrigatório do imóvel não preenchido: {campo}")
        
        # Validar dados do avaliador
        for campo in campos_obrigatorios_avaliador:
            if not self.dados_avaliador.get(campo):
                erros.append(f"Campo obrigatório do avaliador não preenchido: {campo}")
        
        return erros
    
    def obter_dados_completos(self):
        """Retorna todos os dados coletados"""
        return {
            'imovel': self.dados_imovel,
            'avaliador': self.dados_avaliador
        }
    
    def mostrar_resumo(self):
        """Mostra um resumo dos dados coletados"""
        st.header("📋 Resumo dos Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏠 Dados do Imóvel")
            for key, value in self.dados_imovel.items():
                if value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        with col2:
            st.subheader("👤 Dados do Avaliador")
            for key, value in self.dados_avaliador.items():
                if value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def main():
    """Função principal para testar o formulário"""
    st.set_page_config(
        page_title="Formulário Laudo Imobiliário",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("📋 Formulário para Laudo de Avaliação Imobiliária")
    
    formulario = LaudoFormulario()
    
    # Mostrar formulários
    formulario.mostrar_formulario_imovel()
    st.divider()
    formulario.mostrar_formulario_avaliador()
    st.divider()
    formulario.mostrar_formulario_data()
    
    # Botão para validar e mostrar resumo
    if st.button("✅ Validar e Mostrar Resumo", type="primary"):
        erros = formulario.validar_dados()
        
        if erros:
            st.error("❌ Erros encontrados:")
            for erro in erros:
                st.write(f"- {erro}")
        else:
            st.success("✅ Todos os dados foram preenchidos corretamente!")
            formulario.mostrar_resumo()
            
            # Salvar dados em arquivo JSON
            dados_completos = formulario.obter_dados_completos()
            st.json(dados_completos)

if __name__ == "__main__":
    main()
