import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard de Moradia Global", layout="wide")

st.title("🏠 Análise da Acessibilidade de Moradia no Mundo")
st.markdown("""
### 🎯 Problema de Mercado:
**Como o índice de preço das casas evoluiu globalmente entre 2015 e 2024 e qual o intervalo de confiança da média global em cada ano?**

Este dashboard tem como objetivo analisar a evolução dos preços de moradia globalmente, com foco na tendência de variação ano a ano e a incerteza estatística associada.
""")

st.markdown("""
### 📦 Dataset Utilizado
**Fonte:** Kaggle – "Global Housing Market Analysis (2015–2024)"

O conjunto de dados contém as seguintes variáveis:

| Variável | Tipo | Subtipo | Natureza | Estrutura | Temporalidade |
|----------|------|---------|----------|-----------|----------------|
| Country | Qualitativa | Categórica nominal | Pública | Heterogênea | Estática |
| Year | Quantitativa | Discreta | Pública | Homogênea | Dinâmica |
| House Price Index | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Rent Index | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Affordability Ratio | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Mortgage Rate (%) | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Inflation Rate (%) | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| GDP Growth (%) | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Population Growth (%) | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Urbanization Rate (%) | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
| Construction Index | Quantitativa | Contínua | Pública | Homogênea | Dinâmica |
""")

st.markdown("""
### 🕵️ Hipóteses e Perguntas Investigativas

Hipótese principal:
- O índice de preços de moradia apresentou crescimento consistente ao longo dos anos, mas com variação significativa entre regiões.

Pergunta investigativa:
- Como o índice de preço das casas evoluiu globalmente entre 2015 e 2024 e qual o intervalo de confiança da média global em cada ano?
""")

st.markdown("""
### 🧱 Layout e Estrutura do Dashboard

O dashboard será construído com **Streamlit**, em formato multipágina:

- Home.py: Apresentação do problema, do dataset e classificação das variáveis
- 2_📈_Data Analysis.py: Análise exploratória dos dados com foco global e intervalo de confiança por ano
- Páginas adicionais poderão incluir distribuições, comparativos regionais e previsões

Serão utilizadas bibliotecas como pandas, numpy, scipy, plotly e streamlit, com um layout interativo e focado em visualizações intuitivas e interpretação estatística.
""")

# Função para carregar os dados
def carregar_dados():
    df = pd.read_csv("global_housing_market_extended.csv")
    return df

# Carregar e armazenar na sessão
if "data" not in st.session_state:
    st.session_state["data"] = carregar_dados()

st.success("Dados carregados com sucesso! Acesse a aba de Análise para continuar.")

# Adicionando os membros do grupo
st.markdown("---")
st.markdown("### 👥 MEMBROS DO GRUPO")
st.markdown("""
- Diana Letícia de Souza Inocencio - RM553562
- João Viktor Carvalho de Souza - RM552613
- Thiago Araújo Vieira - RM553477
- Victor Augusto Pereira dos Santos - RM553518
- Vitor de Moura Nascimento - RM553806
""")    