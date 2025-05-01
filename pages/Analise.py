import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Análise de Moradia", layout="wide")
st.title("📊 Análise Exploratória + Intervalo de Confiança")

if "data" not in st.session_state:
    st.error("Os dados não estão carregados!")
    st.stop()

df = st.session_state["data"].copy()

# Apenas dados com Índice de Preço de Casa válido
df = df[df["House Price Index"].notna()]

st.subheader("🌍 Evolução Global do Índice de Preço das Casas com Intervalo de Confiança")

# Cálculo da média e intervalo de confiança ano a ano
global_grouped = df.groupby("Year")["House Price Index"]
media_anual = global_grouped.mean()
desvio_anual = global_grouped.std()
n_anual = global_grouped.count()

conf = 0.95
z = stats.norm.ppf(1 - (1 - conf) / 2)

margin_anual = z * (desvio_anual / np.sqrt(n_anual))

df_ic = pd.DataFrame({
    "Year": media_anual.index,
    "Média": media_anual.values,
    "IC Inferior": media_anual.values - margin_anual,
    "IC Superior": media_anual.values + margin_anual
})

# Gráfico com faixa de confiança
fig_global = go.Figure()
fig_global.add_trace(go.Scatter(
    x=df_ic["Year"], y=df_ic["IC Superior"],
    mode="lines", line=dict(width=0),
    name="IC Superior",
    showlegend=False
))
fig_global.add_trace(go.Scatter(
    x=df_ic["Year"], y=df_ic["IC Inferior"],
    fill='tonexty',
    mode="lines", line=dict(width=0),
    fillcolor='rgba(0,100,255,0.2)',
    name="Intervalo de Confiança 95%"
))
fig_global.add_trace(go.Scatter(
    x=df_ic["Year"], y=df_ic["Média"],
    mode="lines+markers",
    line=dict(color="blue"),
    name="Média Global"
))
fig_global.update_layout(
    title="Evolução do Índice Global de Preços com Intervalo de Confiança",
    xaxis_title="Ano",
    yaxis_title="Índice de Preço",
    showlegend=True
)

st.plotly_chart(fig_global, use_container_width=True)

st.info("""
Este gráfico mostra a média global do índice de preços das casas para cada ano entre 2015 e 2024, acompanhada de sua faixa de confiança de 95%.
Essa representação permite observar a tendência mundial e a variabilidade dos dados em torno da média.
        
A linha azul representa a média global do índice de preços por ano, permitindo visualizar o comportamento geral do mercado imobiliário global.

A faixa de confiança de 95% (área sombreada azul-clara) ilustra o intervalo no qual a verdadeira média populacional do índice de preços provavelmente se encontra.

📌 Se observar, há quedas e flutuações bruscas em determinados anos (2020 há 2022), isso pode estar relacionado
 a eventos econômicos globais, como recessões, pandemias, crises financeiras ou políticas governamentais 
 que afetaram os preços das moradias.

Um crescimento constante da média sugere valorização do mercado imobiliário. 

🔍 Este gráfico é fundamental para entender se há uma tendência de valorização ou desaceleração do mercado global de moradia. 
   A inclusão do intervalo de confiança torna a análise estatística mais robusta, permitindo visualizar a incerteza associada à média global dos preços de casas.
""")
# ===========================================================
# NOVO: Gráfico Boxplot por Ano para representar dispersão
# ===========================================================
st.subheader("🌐 Dispersão do Índice de Preços por Ano e País")

fig_box = px.box(
    df,
    x="Year",
    y="House Price Index",
    points="outliers",
    title="Distribuição do Índice de Preço das Casas por Ano (Todos os Países)",
    labels={"House Price Index": "Índice de Preço", "Year": "Ano"},
    color_discrete_sequence=["#636EFA"]
)
fig_box.update_traces(marker=dict(opacity=0.6))

st.plotly_chart(fig_box, use_container_width=True)

st.info(""" O boxplot de dispersão do Índice de Preços por Ano e País fornece uma visão clara sobre a variação 
dos preços das casas em diferentes países ao longo dos anos.
        
Cada boxplot representa um ano, no qual exibe como os preços das casas se distribuem entre os países em 
cada ano. A dispersão dos valores permite identificar quais anos tiveram maior desigualdade nos preços das moradias.
        
📌A linha central dentro da caixa, respresenta a mediana, no qual aponta o valor central do Índice de Preço das Casas.
Se ela se desloca para cima ao longo dos anos, indica um aumento geral nos preços das moradias.
        
Os Quartis (limites da caixa, parte inferior e superior da caixa) mostram onde se encontram 50% dos valores centrais do índice de preços.
Se a caixa for larga, significa que há grande variação nos preços entre os países, Se for estreita, indica que os preços estão mais 
homogêneos.
        
Extremos e Outliers (pontos fora da caixa) representam países onde os preços das casas são significativamente mais altos ou mais baixos que a média global.
muitos outliers podem indicar desigualdade extrema entre países, onde alguns enfrentam supervalorização imobiliária e outros têm preços bem abaixo da média.
        
🔍Este gráfico complementa a análise anterior, mostrando não apenas a média, mas também como os preços se espalham entre os países. Se houver anos com alta 
dispersão e muitos outliers, isso pode indicar instabilidade no mercado imobiliário global. Já uma distribuição mais uniforme sugere que os preços evoluíram 
de forma equilibrada entre diferentes regiões.
""")