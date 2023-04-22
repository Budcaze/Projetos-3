import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np

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

st.write("Gráfico de barras que mostra a quantidade de acidentes por bairro")
chart = alt.Chart(chart_data).mark_bar().encode(x='counts', y=alt.Y('bairro', sort='-x'), text='counts')
st.altair_chart(chart, use_container_width=True)


#tendência de acidentes ao longo do tempo
st.write("Aqui está um gráfico de linhas que mostra a tendência dos acidentes ao longo do tempo:")
chart_data = df.groupby(['Ano']).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_line().encode(x=alt.X('Ano', axis=alt.AxisConfig(labelAngle=0)), y=alt.Y('counts', title='Número de acidentes'))
st.altair_chart(chart, use_container_width=True)



#hora do dia x numero de acidentes
st.write("Aqui está um gráfico de barras que mostra a quantidade de acidentes por hora no dia:")
chart_data = df.groupby(df['hora'].dt.hour).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_bar().encode(x=alt.X('hora:O', title='Hora do dia', axis=alt.AxisConfig(labelAngle=0)), y=alt.Y('counts', title='Número de acidentes'))
st.altair_chart(chart, use_container_width=True)



st.write("Aqui está um gráfico de regressão para prever o número de acidentes baseado na hora do dia:")
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


st.write("Aqui está um gráfico de barras que mostra a correlação das vítimas fatais com a condição da via:")
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
).properties(title="Correlação entre o número de vítimas fatais e as condições da via").transform_filter(
    alt.FieldOneOfPredicate(field='condicao_via', oneOf=df_corr['condicao_via'].unique()[1:])
)
st.altair_chart(correlation_chart, use_container_width=True)


st.write("Aqui está um gráfico de barras mostrando a frequência dos tipos de acidentes por condição da via")
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
st.altair_chart(bars, use_container_width=True)


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
st.text('Foi calculado com o modelo de árvore de decisão a acurácia de previsões de número de vítimas em relação a \nvelocidade máxima da via, e a seguir está o resultado:')
# Avaliando o desempenho do modelo
st.text(f"Acurácia: {metrics.accuracy_score(y_test, y_pred)}")

st.text("Uma acurácia de 0,773 significa que o modelo de árvore de decisão está correto em\n 77,3%' das previsões feitas em novos dados.")

st.write("Aqui está um gráfico de dispersão para mostrar a relação entre o tipo do acidente e a presença de vitima no acidente")
# Plota um gráfico de dispersão com os pontos agrupados por ano e tipo de acidente
chart = alt.Chart(df).mark_circle(size=60).encode(
    x=alt.X('Ano', axis=alt.AxisConfig(labelAngle=0)),
    y=alt.Y('vitimas', title='Número de vítimas', aggregate='sum'),
    color='situacao_semaforo',
    tooltip=['Ano', alt.Tooltip('vitimas', aggregate='sum'), 'situacao_semaforo']
).interactive()

# Exibe o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)




# Converta a coluna data para o tipo datetime
df_data = pd.to_datetime(df['data'], format='%Y-%m-%d').dt.to_period('M')
# Adicione uma nova coluna chamada mes que contém apenas o mês da data
df['mes'] = df_data.dt.month


st.write("Aqui está um gráfico de radar que contem a comparação entre o número de acidentes em diferentes meses do ano")
df_vm = df.groupby('mes')['vitimas'].sum().reset_index(name='vitimas')
fig, ax = plt.subplots(figsize=(3, 5), subplot_kw=dict(polar=True))

# Define os limites do gráfico de radar
ax.set_ylim([0, df_vm['vitimas'].max()+2])

# Define os ângulos e rótulos dos eixos
angles = [n / float(len(df_vm['mes'])) * 2 * 3.14159 for n in range(len(df_vm['mes']))]
labels = [str(mes) for mes in df_vm['mes']]
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




st.write("Aqui está um gráfico de linhas mostrando a evolução temporal da frequência de acidentes por bairro")
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
