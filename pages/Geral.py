import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn import svm
from sklearn.svm import SVR
import datetime

df_bruto = pd.read_parquet("data/DataSetAcidentesRecife.parquet")
df_tratado = pd.read_parquet("data/DataSetAcidentesRecifeTratado.parquet")

st.set_page_config(page_title="Análise de Acidentes de Trânsito em Recife", 
                   page_icon=":car:", 
                   layout="wide")

st.title("Análise de Acidentes de Trânsito em Recife")

plt.style.use('ggplot')
sns.set_style("whitegrid")
sns.set_palette("pastel")

# Tratando dados
df_bruto['vitimas'] = df_bruto['vitimas'].fillna(0).astype(int)
df_bruto['vitimasfatais'] = df_bruto['vitimasfatais'].fillna(0).astype(int)
df_bruto['situacao_semaforo'] = df_bruto['situacao_semaforo'].fillna(0)
df_bruto['situacao_semaforo'].replace({'': 'sem informações', 0: 'sem informações'},regex=True,inplace=True)
df_bruto['Ano'] = df_bruto['Ano'].astype(str)
df_bruto = df_bruto.dropna(subset=['hora'])
df_bruto['hora'] = pd.to_datetime(df_bruto['hora'], format='%H:%M:%S')

df_bruto['tipo'].replace({'MMMMMMMMMMMMNNNNNNNNNNNNNNC' :0},regex=True,inplace=True)
df_bruto['tipo'].replace({'SANTO AMARO' :0},regex=True,inplace=True)
df_bruto['tipo'] = df_bruto['tipo'].fillna(0)
df_bruto['tipo'].replace({0 :'SEM INFORMACOES'},regex=True,inplace=True)
df_bruto['tipo'].replace({'0' :'SEM INFORMACOES'},regex=True,inplace=True)

#Remover o Km/h da coluna velocidade_max_via
df_bruto['velocidade_max_via'].replace({' km/h':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'KM/H':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'km':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'KM':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'N/I':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'n/i':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'/h':''},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'30 e 40':'35'},regex=True,inplace=True)
df_bruto['velocidade_max_via'].replace({'':'0'},regex=True,inplace=True)

#Tratar bairro
#Define 0 para None e outros valores errados
df_bruto['bairro'] = df_bruto['bairro'].fillna(0)
df_bruto['bairro'] = df_bruto['bairro'].replace('BAIRRO DO RECIFE', 'RECIFE')
df_bruto['bairro'] = df_bruto['bairro'].replace('BOA  VIAGEM', 'BOA VIAGEM')
df_bruto['bairro'] = df_bruto['bairro'].replace('BOMBA DO HEMETERIO', 'BOMBA DO HEMETÉRIO')
df_bruto['bairro'] = df_bruto['bairro'].replace('FABIO', 0)
df_bruto['bairro'] = df_bruto['bairro'].replace('IPESEP', 'IPSEP')
df_bruto['bairro'] = df_bruto['bairro'].replace('JOANA BEZERRA', 'ILHA JOANA BEZERRA')
df_bruto['bairro'] = df_bruto['bairro'].replace('MARCELO', 0)
df_bruto['bairro'] = df_bruto['bairro'].astype(str)

#Alterando tipo da coluna para inteiro
df_bruto['velocidade_max_via'] = df_bruto['velocidade_max_via'].fillna(0) # substitui o vazio por 0
df_bruto['velocidade_max_via'] = df_bruto['velocidade_max_via'].astype('int64') # Converte para inteiro

# SIDEBAR
with st.sidebar:
    st.sidebar.title("Filtros")
    # Filtro por ano
    st.header("Filtre por ano")
    ano = st.multiselect("Selecione o ano", options=df_bruto["Ano"].unique(), default=df_bruto["Ano"].unique())

    # Filtro por bairro
    st.header("Filtre por bairro")
    bairro = st.multiselect("Selecione o bairro", options=df_bruto["bairro"].unique(), default=df_bruto["bairro"].unique())



df = df_bruto.query("Ano == @ano & bairro == @bairro")

#GRAFICOS
#bairro x numero de acidentes
bairro_counts = df['bairro'].value_counts().reset_index().rename(columns={'index':'bairro', 'bairro':'counts'})
top_bairros = bairro_counts.head(15)['bairro'].tolist()
chart_data = df.groupby(['bairro']).size().reset_index(name='counts')
chart_data = chart_data[chart_data['bairro'].isin(top_bairros)]

st.write("Gráfico de barras, mostrando a distribuição de acidentes de trânsito por bairros no Recife. Sendo possível ver o destaque desigual de Boa Viagem; Uma média de 1.105 acidentes por ano, enquanto que os demais bairros apresentam médias menores. A distribuição desigual dos acidentes de trânsito pelos bairros podem indicar que existem outros fatores que favorecem expressivamente acidentes em Boa Viagem.")
chart = alt.Chart(chart_data).mark_bar().encode(x=alt.X('counts', title="Número de acidentes"), y=alt.Y('bairro', sort='-x'))
st.altair_chart(chart, use_container_width=True)

#tendência de acidentes ao longo do tempo
st.write("Gráfico de linhas, demonstrando a evolução do quantitativo de acidentes ao longo do tempo. Ao analisar esse gráfico, é possível notar que houve um aumento nos números de acidentes de trânsito entre 2015 e 2019, com um pico de 12.044 acidentes em 2019. Entretanto houve uma queda significativa nos números de acidentes de 2020 a 2021, com 4.092 e 2.380 acidentes, respectivamente, sendo possível observar o impacto gerado pela pandemia na relação dos acidentes.")
chart_data = df.groupby(['Ano']).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_line().encode(x=alt.X('Ano', axis=alt.AxisConfig(labelAngle=0)), y=alt.Y('counts', title='Número de acidentes'))
st.altair_chart(chart, use_container_width=True)

#hora do dia x numero de acidentes
st.write("Gráfico de barras, no qual é possível observar a distribuição do quantitativo de acidentes globais durante o horário do dia, ou seja, os horários mais comuns para o acontecimento dos acidentes. É possível notar que há uma tendência de aumento no número de acidentes durante o período matutino, com pico por volta das 8 horas da manhã, e no período vespertino, com pico por volta das 17 horas. Esses horários são próximos aos horários de pico de trânsito na cidade, que ocorrem quando as pessoas estão indo ou voltando do trabalho ou das escolas. Quando traçamos um paralelo com os horários de pico de trabalho e escola, podemos observar que os horários de maior número de acidentes, às 8 horas e às 17 horas, coincidem, que é quando muitas pessoas começam a se deslocar para os seus destinos.")
chart_data = df.groupby(df['hora'].dt.hour).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_bar().encode(x=alt.X('hora:O', title='Hora do dia', axis=alt.AxisConfig(labelAngle=0)), y=alt.Y('counts', title='Número de acidentes'))
st.altair_chart(chart, use_container_width=True)

st.write("O gráfico abaixo permite visualização do aumento gradual do número de acidentes ao longo do dia, bem como a previsão do número desses acidentes. A linha de regressão reforça a relação do horário de pico com aumento no número de acidentes, o horário das 8 horas tem uma média superior a 4.000 acidentes, mantendo-se acima de 3.000 acidentes até próximo das 18 horas.")
# Cria coluna com a hora como números
df['hora_numerica'] = df['hora'].apply(lambda x: x.hour)

# Agrupa por hora e calcula a média do número de acidentes em cada hora
hora_counts = df.groupby('hora_numerica')['Unnamed: 0'].agg(['count']).reset_index()
hora_counts = hora_counts.groupby('hora_numerica')['count'].agg(['mean']).reset_index()
hora_counts.columns = ['hora', 'mean']
# Plota o gráfico de dispersão com a regressão linear
fig, ax = plt.subplots(figsize=(4, 2.2))
sns.regplot(x='hora', y='mean', data=hora_counts, scatter_kws={'s': 20}, ax = ax)
ax.set_ylabel('Média')
st.pyplot(fig)

st.write("Gráfico de barras, o qual demostra a correlação da quantidade de vítimas fatais com a condição da via. Nele é possível observar um número muito maior de acidente em via seca, no que toca aos quatro valores no eixo x: molhada, oleosa, outros e seca, onde a condição oleosa e outros apresentaram valor zero no eixo Y, enquanto que as condições molhada e seca apresentaram valores de cerca de 10 e 60, respectivamente, ambas as colunas ficaram na cor verde. Isso sugere que, em geral, as condições da via molhada e seca estão positivamente correlacionadas com o número de vítimas fatais em acidentes de trânsito.")
# Criar novo DataFrame com as colunas relevantes
df_corr = df[["condicao_via", "vitimasfatais"]]

# Cálculo da correlação
correlations = df_corr.corr()["vitimasfatais"].drop("vitimasfatais")
correlations = correlations[correlations.abs() > 0.1]

# Gráfico de correlação
correlation_chart = alt.Chart(df_corr).mark_bar().encode(
    x=alt.X("condicao_via", title='Condição da Via', axis=alt.AxisConfig(labelAngle=0)),
    y=alt.Y("vitimasfatais", title="Correlação"),
    color=alt.condition(
        alt.datum.vitimasfatais > 0,
        alt.value("green"), alt.value("red")
    )
).properties(title="").transform_filter(
    alt.FieldOneOfPredicate(field='condicao_via', oneOf=df_corr['condicao_via'].unique()[1:])
)
st.altair_chart(correlation_chart, use_container_width=True)


# st.write("Gráfico de barras demostrando a frequência dos tipos de acidentes em determinadas condições de via")
# agrupamento dos dados por tipo de acidente e condição da via
df_grouped = df.groupby(['tipo', 'condicao_via']).size().reset_index(name='counts')

# ordenação dos tipos de acidente em ordem decrescente e seleção dos 10 maiores
df_grouped = df_grouped.sort_values(by='counts', ascending=False)

# criação do gráfico de barras
bars = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('counts:Q', axis=alt.Axis(title='Frequência')),
    y=alt.Y('tipo:N', sort='-x', axis=alt.Axis(title='Tipo de Acidente')),
    color=alt.Color('condicao_via:N', legend=alt.Legend(title='Condição da Via'))
)

# exibição do gráfico
# st.altair_chart(bars, use_container_width=True)


# Selecionando as colunas que serão utilizadas na análise
X = df[['velocidade_max_via']]

# Definindo a variável target
y = df['vitimas']

# Dividindo o dataset em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criando o modelo de árvore de decisão
tree = DecisionTreeClassifier(max_depth=3, random_state=42)

# Treinando o modelo
tree.fit(X_train, y_train)

# Fazendo as previsões com o conjunto de teste
y_pred = tree.predict(X_test)
# st.text('Foi calculado com o modelo de árvore de decisão a acurácia de previsões de número de vítimas em relação a \nvelocidade máxima da via, e a seguir está o resultado:')
# Avaliando o desempenho do modelo
#st.text(f"Acurácia: {metrics.accuracy_score(y_test, y_pred)}")

#st.text("Uma acurácia de 0,773 significa que o modelo de árvore de decisão está correto em\n 77,3%' das previsões feitas em novos dados.")

st.write("Gráfico de dispersão o qual demostra a relação entre o estado do semafórico da via e a presença de vitimas dos acidentes. Pode-se observar que a situação do semáforo 'Não existe' foi a que apresentou a maior quantidade de vítimas em todos os anos, exceto em 2018, quando a situação do semáforo 'Sem informações' teve a maior quantidade de vítimas. Por outro lado, a situação do semáforo 'Desligado' foi a que apresentou a menor quantidade de vítimas em todos os anos.")
# Plota um gráfico de dispersão com os pontos agrupados por ano e tipo de acidente
chart = alt.Chart(df).mark_circle(size=60).encode(
    x=alt.X('Ano', axis=alt.AxisConfig(labelAngle=0)),
    y=alt.Y('vitimas', title='Número de vítimas', aggregate='sum'),
    color=alt.Color('situacao_semaforo', title="Situação do Semáforo"),
    tooltip=['Ano', alt.Tooltip('vitimas', aggregate='sum'), 'situacao_semaforo']
).interactive()

# Exibe o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)

# Converta a coluna data para o tipo datetime
df_data = pd.to_datetime(df['data'], format='%Y-%m-%d').dt.to_period('M')
# Adicione uma nova coluna chamada mes que contém apenas o mês da data
df['mes'] = df_data.dt.month
meses = [datetime.date(2000, m, 1).strftime('%b') for m in range(1, 13)]


st.write("Observando o gráfico de radar abaixo, podemos notar que os meses de setembro a dezembro possuem os maiores números de vítimas de trânsito, com valores acima da média anual. Por outro lado, os meses de fevereiro e abril possuem os menores números de vítimas, abaixo da média anual, esses valores nestes meses podem estar relacionados com fatores climáticos, os meses de setembro e outubro correspondem a época de transição entre o inverno e o verão, e podem ser caracterizados por temperaturas mais elevadas e clima mais seco, o que pode aumentar o fluxo de trânsito e, consequentemente, o risco de acidentes. Também podem estar relacionados a fatores sazonais, alguns meses do ano podem apresentar um maior número de eventos ou atividades que aumentem o fluxo de veículos e pedestres, como feriados, eventos esportivos, festivais e outras celebrações.")
df_vm = df.groupby('mes')['vitimas'].sum().reset_index(name='vitimas')
fig, ax = plt.subplots(figsize=(3, 5), subplot_kw=dict(polar=True))

# Define os limites do gráfico de radar
ax.set_ylim([0, df_vm['vitimas'].max()+2])

# Define os ângulos e rótulos dos eixos
angles = [n / float(len(df_vm['mes'])) * 2 * 3.14159 for n in range(len(df_vm['mes']))]
#labels = [str(mes) for mes in df_vm['mes']]
labels = meses
ax.set_xticks(angles)
ax.set_xticklabels(labels)

# Adiciona os dados ao gráfico
ax.plot(angles, df_vm['vitimas'], 'o-', linewidth=2)

# Adiciona um preenchimento ao gráfico
ax.fill(angles, df_vm['vitimas'], alpha=0.25)

# Define o título do gráfico
ax.set_title('Quantidade de vítimas por mês', size=20, y=1.05)

# Mostra o gráfico
st.pyplot(fig)




st.write("Gráfico de linhas demostrando a evolução temporal da frequência de acidentes por bairro. Sendo possível explorar de forma aprofundada a evolução dos acidentes de trânsito ao longo do tempo em cada bairro, além de notarmos o impacto da pandemia separadamente em todos eles.")
# Agrupa os dados por bairro e data e conta o número de acidentes em cada grupo
df_grouped = df.groupby(['bairro', 'Ano']).size().reset_index(name='count')

# Ordena o DataFrame em ordem decrescente de contagem e seleciona os 10 primeiros bairros
top10_bairros = df_grouped.groupby('bairro')['count'].sum().reset_index(name='count_total')\
    .sort_values(by='count_total', ascending=False).head(10)['bairro'].values

# Cria uma figura e um eixo
fig, ax = plt.subplots()

# Itera pelos bairros únicos no DataFrame e adiciona uma linha para cada um dos 10 bairros com maior número de vítimas
for bairro in top10_bairros:
    # Seleciona apenas as linhas correspondentes ao bairro atual
    Ano_bairro = df_grouped[df_grouped['bairro'] == bairro]
    
    # Plota a linha correspondente ao bairro atual
    ax.plot(Ano_bairro['Ano'], Ano_bairro['count'], label=bairro)

# Adiciona uma legenda
ax.legend(fontsize=6)

# Define os rótulos dos eixos
ax.set_xlabel('Ano')
ax.set_ylabel('Número de acidentes')

# Mostra o gráfico usando st.pyplot()
st.pyplot(fig)


######## Machine learning ############
# Carregando os dados
df = pd.read_parquet("data/DataSetAcidentesRecifeTratado.parquet")


st.title("Modelos de Machine Learning")

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