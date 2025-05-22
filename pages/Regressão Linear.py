import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

st.set_page_config(page_title="Análise de Regressão Linear", layout="wide")
st.title("📈 Análise de Regressão Linear do Índice de Preços de Moradias")

if "data" not in st.session_state:
    st.error("Os dados não estão carregados!")
    st.stop()

df = st.session_state["data"].copy()

df = df.rename(columns={
    "Inflation Rate (%)": "Taxa de Inflação (%)",
    "GDP Growth (%)": "Crescimento do PIB (%)",
    "Mortgage Rate (%)": "Taxa de Hipoteca (%)"
})

df = df.dropna(subset=["House Price Index", "Taxa de Inflação (%)", "Crescimento do PIB (%)", "Taxa de Hipoteca (%)"])

numeric_cols = df.select_dtypes(include=[np.number])

st.subheader("📊 Estatísticas Descritivas")
desc_stats = numeric_cols.describe()
desc_stats.loc["Assimetria"] = numeric_cols.skew()
desc_stats.loc["Curtose"] = numeric_cols.kurtosis()
desc_stats = desc_stats.rename(index={
    "count": "Quantidade",
    "mean": "Média",
    "std": "Desvio Padrão",
    "min": "Mínimo",
    "25%": "1º Quartil",
    "50%": "Mediana",
    "75%": "3º Quartil",
    "max": "Máximo"
})
st.dataframe(desc_stats)

st.info("""
🔍 **Interpretação:**  
As estatísticas descritivas oferecem um panorama da distribuição dos dados. Podemos observar que a **Taxa de Hipoteca (%)** apresenta uma variabilidade maior, podendo impactar a acessibilidade ao financiamento imobiliário.  
A **Taxa de Inflação (%)** pode ter um impacto indireto nos preços das casas, pois influencia o poder de compra dos consumidores.  
O **Crescimento do PIB (%)** pode indicar períodos de valorização ou desaquecimento do mercado imobiliário, dependendo das tendências econômicas.  
Valores elevados de **Curtose** sugerem a presença de extremos nos dados, enquanto a **Assimetria** indica desvios na distribuição.
""")

st.subheader("🔍 Multicolinearidade - Fator de Inflação da Variância (VIF)")
X_vif = df[["Taxa de Inflação (%)", "Crescimento do PIB (%)", "Taxa de Hipoteca (%)"]]
X_vif = sm.add_constant(X_vif)
vif_data = pd.DataFrame()
vif_data["Variável"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
st.dataframe(vif_data)

st.info("""
🔍 **Interpretação:**  
O fator VIF nos ajuda a verificar se existe multicolinearidade entre as variáveis.  
Valores de **VIF acima de 5** indicam forte correlação entre variáveis, o que pode distorcer os resultados da regressão linear.  
Caso alguma variável apresente alto VIF, pode ser necessário removê-la ou transformar os dados.
""")

X = df[["Taxa de Inflação (%)", "Crescimento do PIB (%)", "Taxa de Hipoteca (%)"]]
X = sm.add_constant(X)
y = df["House Price Index"]
modelo = sm.OLS(y, X).fit()

st.subheader("📈 Resultados da Regressão Linear")
st.table(pd.DataFrame({
    "Variável": ["Constante", "Taxa de Inflação (%)", "Crescimento do PIB (%)", "Taxa de Hipoteca (%)"],
    "Coeficiente": modelo.params.values,
    "Erro Padrão": modelo.bse.values,
    "Estatística t": modelo.tvalues.values,
    "Valor-p": modelo.pvalues.values
}))

st.info("""
🔍 **Interpretação:**  
Os coeficientes indicam o impacto das variáveis sobre os preços das casas.  
📌 Uma **Taxa de Inflação (%)** mais alta pode influenciar o aumento dos preços imobiliários.  
📌 O **Crescimento do PIB (%)** pode afetar o mercado de forma variada, dependendo do contexto econômico.  
📌 A **Taxa de Hipoteca (%)** tem impacto direto na acessibilidade ao financiamento de moradia.  
Se os valores de **Valor-p forem acima de 0.05**, significa que a variável não tem um efeito estatisticamente significativo sobre os preços das casas.
""")

st.subheader("📊 Diagnóstico dos Resíduos")
residuos = modelo.resid
fig_res = plt.figure(figsize=(8, 6))
sns.histplot(residuos, bins=30, kde=True)
plt.xlabel("Resíduos")
plt.ylabel("Frequência")
plt.title("Distribuição dos Resíduos da Regressão")
st.pyplot(fig_res)

st.info("""
🔍 **Interpretação:**  
A análise dos resíduos ajuda a verificar se a regressão linear é adequada.  
Se os resíduos forem **muito assimétricos** ou houver picos exagerados (alta curtose), pode ser necessário testar **transformações não lineares** ou outro tipo de modelo estatístico.
""")

st.subheader("📊 Relações entre variáveis e Índice de Preço das Casas")
for var in X.columns[1:]:  
    fig = px.scatter(df, x=var, y="House Price Index", trendline="ols",
                     title=f"Relação entre {var} e Índice de Preço das Casas",
                     labels={var: var, "House Price Index": "Índice de Preço"})
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"""
    🔍 **Interpretação:**  
    Este gráfico mostra como **{var}** está relacionado aos preços das casas ao longo dos anos.  
    A linha de regressão indica se há uma **tendência positiva ou negativa** entre essa variável e o mercado imobiliário.  
    Se a dispersão dos pontos for muito alta, pode significar que há outros fatores que influenciam o Índice de Preço das Casas.
    """)


st.info("""
### 💡 **Resumo da análise**
  A análise de regressão linear revelou que variáveis macroeconômicas, como Taxa de Inflação (%), Crescimento do PIB (%) e Taxa de Hipoteca (%), 
possuem impacto limitado sobre o Índice de Preço das Casas, uma vez que nenhum dos fatores apresentou significância estatística relevante.
        
A avaliação das estatísticas descritivas indicou grande variabilidade nas taxas de hipoteca e inflação, enquanto o fator VIF confirmou a ausência de
multicolinearidade preocupante. A análise dos resíduos revelou que o modelo pode não capturar plenamente as complexidades do mercado imobiliário,

Embora os gráficos tenham mostrado algumas tendências, a alta dispersão dos dados sugere que outros fatores, como oferta e demanda imobiliária, políticas econômicas e crescimento populacional, 
podem exercer influência significativa sobre os preços das casas.""")