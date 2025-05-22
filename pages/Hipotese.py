import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Testes de Hipótese", layout="wide")
st.title("🧪 Testes de Hipóteses com Dados de Moradia")

if "data" not in st.session_state:
    st.error("Os dados não estão carregados!")
    st.stop()

# Copiar o DataFrame da sessão
df = st.session_state["data"].copy()
df = df[df["House Price Index"].notna()]

# ------------------------------------------
# Hipótese 1: Comparar o índice médio entre 2015 e 2024
# ------------------------------------------
st.header("📊 Hipótese 1: Diferença no Índice Médio entre 2015 e 2024")

precos_2015 = df[df["Year"] == 2015]["House Price Index"]
precos_2024 = df[df["Year"] == 2024]["House Price Index"]

# Teste t independente
t_stat, p_valor_t = stats.ttest_ind(precos_2015, precos_2024, equal_var=False)

st.write(f"**Estatística t:** {t_stat:.2f}")
st.write(f"**p-valor:** {p_valor_t:.4f}")
st.info("""
🔍 **Interpretação:** 
 A análise mostrou que não houve diferença estatisticamente significativa entre os índices médios de preços das casas entre 2015 e 2024. 
Apesar de possíveis variações visuais no gráfico de boxplot, os dados indicam que as médias podem ser consideradas estatisticamente semelhantes, 
ou seja, a evolução ao longo dos anos pode ter se mantido estável em termos globais.
""")

if p_valor_t < 0.05:
    st.success("Rejeitamos H0: Há diferença significativa entre os índices médios de 2015 e 2024.")
else:
    st.info("Não rejeitamos H0: Não há diferença significativa entre os índices médios.")

# Visualização
fig_box_1 = px.box(df[df["Year"].isin([2015, 2024])], x="Year", y="House Price Index",
                  title="Distribuição do Índice de Preço - 2015 vs 2024",
                  color="Year")
st.plotly_chart(fig_box_1, use_container_width=True)

# ------------------------------------------
# Hipótese 2: Proporção de países acima da média global por ano
# ------------------------------------------
st.header("📊 Hipótese 2: Proporção de Países Acima da Média Global")

media_global = df.groupby("Year")["House Price Index"].mean()
df["Acima da Média"] = df.apply(lambda row: row["House Price Index"] > media_global[row["Year"]], axis=1)

# Tabela de contingência
contingencia = pd.crosstab(df["Year"], df["Acima da Média"])
qui2, p_valor_q, _, _ = stats.chi2_contingency(contingencia)

st.write(f"**Estatística Qui-quadrado:** {qui2:.2f}")
st.write(f"**p-valor:** {p_valor_q:.4f}")
st.info("""
🔍 **Interpretação:** 
 O teste de qui-quadrado indica que a proporção de países com índice acima da média global não varia significativamente ao longo dos anos. 
A distribuição parece relativamente estável entre os períodos analisados, sugerindo que não há uma tendência clara de aumento 
ou queda na quantidade de países com desempenho superior à média mundial.
""")

if p_valor_q < 0.05:
    st.success("Rejeitamos H0: A proporção de países com índice acima da média varia com o ano.")
else:
    st.info("Não rejeitamos H0: A proporção de países com índice acima da média é independente do ano.")

# Visualização
proporcoes = df.groupby("Year")["Acima da Média"].mean().reset_index()
proporcoes["Proporção (%)"] = proporcoes["Acima da Média"] * 100

fig_bar = px.bar(proporcoes, x="Year", y="Proporção (%)",
                 title="Proporção de Países com Índice Acima da Média por Ano",
                 labels={"Proporção (%)": "Proporção (%)"})

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------
st.info("""
📌 Nesta página, realizamos dois testes de hipótese:
1. Comparação de médias entre 2015 e 2024 usando teste t.
2. Teste qui-quadrado para verificar se a proporção de países acima da média varia por ano.

As análises ajudam a entender variações temporais e padrões relevantes no mercado global de moradia.
""")