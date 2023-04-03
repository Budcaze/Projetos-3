import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder



# Carregando os dados
df = pd.read_parquet("data/DataSetAcidentesRecifeTratado.parquet")

scatter = alt.Chart(df).mark_point().encode(x='vitimas', y='velocidade_max_via')
st.altair_chart(scatter, use_container_width=True)


newDF2 = df[['Ano', 'vitimas', 'vitimasfatais', 'velocidade_max_via']]
A = newDF2.drop(['vitimas'], axis=1)
b = df['vitimas']
A_train, A_test, b_train, b_test = train_test_split(A, b, test_size=0.2, random_state=42)

# Criando um modelo de classificação com Random Forest
clf = RandomForestClassifier()
clf.fit(A_train, b_train)

# Avaliando o desempenho do modelo com métricas de classificação
b_pred = clf.predict(A_test)
report2 = classification_report(b_test, b_pred)
st.text(report2)

gravidade_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('gravidade', bin=True),
    y='count()',
    color=alt.Color('gravidade')
).properties(
    width=600,
    height=400
)

#ANALISE EXPLORATORIA DE DADOS
# Visualização da distribuição do número de vítimas
vitimas_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('vitimas', bin=True),
    y='count()',
    color=alt.Color('vitimas', scale=alt.Scale(scheme='viridis'))
).properties(
    width=600,
    height=400
)
st.altair_chart(vitimas_chart)


