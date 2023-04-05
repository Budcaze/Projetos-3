import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn import svm
from sklearn.svm import SVR


# Carregando os dados
df = pd.read_parquet("data/DataSetAcidentesRecifeTratado.parquet")
df_categorico = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.

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


############### TESTE ###########################
st.title("Teste")
df_teste = df

# remover colunas desnecessárias
df_teste = df_teste.drop(['data', 'hora', 'bairro', 'endereco', 'numero', 'detalhe_endereco_acidente', 
              'complemento', 'bairro_cruzamento', 'num_semaforo', 'acidente_verificado', 'ponto_controle', 'sentido_via',
              'situacao_placa','situacao_semaforo', 'divisao_via1', 'divisao_via2', 'divisao_via3'], axis=1)

# dividir o dataset em treino e teste
X = df_teste.drop(['vitimas', 'vitimasfatais'], axis=1)
y = df_teste['vitimasfatais']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# modelo de regressão linear
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

# modelo de árvore de decisão
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)

# modelo de Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Modelo de SVM
svm_model = SVR()
svm_model.fit(X_train, y_train)

# avaliar o desempenho dos modelos
st.text(f"Regressão Linear - R2 Score: {r2_score(y_test, lr_pred)}")
st.text(f"Regressão Linear - RMSE: {np.sqrt(mean_squared_error(y_test, lr_pred))}")

# Avaliar o desempenho do modelo de árvore de decisão
r2_dt = r2_score(y_test, dt_pred)
rmse_dt = np.sqrt(mean_squared_error(y_test, dt_pred))
st.text(f"R² do modelo de Árvore de Decisão:{r2_dt}")
st.text(f"RMSE do modelo de Árvore de Decisão:{rmse_dt}")

# Calcular o erro médio quadrado do modelo Random Forest no conjunto de teste
y_pred_rf = rf.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
st.text(f"Erro quadrado médio do modelo Random Forest: {mse_rf}")

# Avaliar o desempenho do modelo de SVM
y_pred_svm = svm_model.predict(X_test)
r2_svm = r2_score(y_test, y_pred_svm)
mse_svm = mean_squared_error(y_test, y_pred_svm)
st.text(f"R² do modelo de SVM: {r2_svm}")
st.text(f"Erro quadrado médio do modelo de SVM: {mse_svm}")