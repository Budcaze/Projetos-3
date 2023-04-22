import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_parquet("data/DataSetAcidentesRecife.parquet")
df_tratado = pd.read_parquet("data/DataSetAcidentesRecifeTratado.parquet") # Abertura do DataSet.

st.title("Análise de Acidentes de Trânsito em Recife")

# Converte o tipo das colunas para inteiro
df['vitimas'] = df['vitimas'].fillna(0) # substitui o vazio por 0
df['vitimas'] = df['vitimas'].astype('int64') # Converte para inteiro

df['vitimasfatais'] = df['vitimasfatais'].fillna(0) # substitui o vazio por 0
df['vitimasfatais'] = df['vitimasfatais'].astype('int64') # Converte para inteiro

# Converte o ano para string
df['Ano'] = df['Ano'].astype('str') #Converte para string

#converte para datatime
df = df.dropna(subset=['hora'])
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S')

df['tipo'].replace({'MMMMMMMMMMMMNNNNNNNNNNNNNNC' :0},regex=True,inplace=True)
df['tipo'].replace({'SANTO AMARO' :0},regex=True,inplace=True)
df['tipo'] = df['tipo'].fillna(0)
df['tipo'].replace({0 :'SEM INFORMACOES'},regex=True,inplace=True)
df['tipo'].replace({'0' :'SEM INFORMACOES'},regex=True,inplace=True)

#Remover o Km/h da coluna velocidade_max_via
df['velocidade_max_via'].replace({' km/h':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'KM/H':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'km':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'KM':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'N/I':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'n/i':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'/h':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'30 e 40':'35'},regex=True,inplace=True)
df['velocidade_max_via'].replace({'':'0'},regex=True,inplace=True)

#Alterando tipo da coluna para inteiro
df['velocidade_max_via'] = df['velocidade_max_via'].fillna(0) # substitui o vazio por 0
df['velocidade_max_via'] = df['velocidade_max_via'].astype('int64') # Converte para inteiro

# SIDEBAR
st.sidebar.header("Filtre aqui por ano:") #Cada SIDEBAR é composto pelo cabeçalho seguido da nossa variavel que vai armazenar o filtro e eu posso colocar as opções de acordo com o meu dataset e um padrão para começar o filtro, nesse caso eu coloquei para pegar todos as opções que tem nas colunas
ano = st.sidebar.multiselect(
    "Selecione o ano: ",
    options=df["Ano"].unique(),
    default=df["Ano"].unique()
)



st.sidebar.header("Filtre aqui por bairro :")
bairro = st.sidebar.multiselect(
    "Selecione o bairro: ",
    options=df["bairro"].unique(),
    default=df["bairro"].unique()
)



df_selection = df.query( #Aqui eu vou atribuir a varivavel que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro" #O @ significa que estou chamando a varivel que criei lá no sidebar
)
# st.dataframe(df_selection) #Aqui eu chamo nosso dataset para ele aparecer

#bairro x numero de acidentes
bairro_counts = df['bairro'].value_counts().reset_index()
bairro_counts.columns = ['bairro', 'counts']
top_bairros = bairro_counts.head(15)['bairro'].tolist()

chart_data = df.groupby(['bairro']).size().reset_index(name='counts')
chart_data = chart_data[chart_data['bairro'].isin(top_bairros)]

st.write("Aqui está um gráfico de barras que mostra a quantidade de acidentes por bairro:")
chart = alt.Chart(chart_data).mark_bar().encode(x='counts', y=alt.Y('bairro', sort='-x'), text='counts')
st.altair_chart(chart, use_container_width=True)


#tendência de acidentes ao longo do tempo
st.write("Aqui está um gráfico de linhas que mostra a tendência dos acidentes ao longo do tempo:")
chart_data = df.groupby(['data']).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_line().encode(x='data', y='counts')
st.altair_chart(chart, use_container_width=True)



#hora do dia x numero de acidentes
st.write("Aqui está um gráfico de barras que mostra a quantidade de acidentes por hora no dia:")
chart_data = df.groupby(df['hora'].dt.hour).size().reset_index(name='counts')
chart = alt.Chart(chart_data).mark_bar().encode(x=alt.X('hora:O', title='Hora do dia', axis=alt.AxisConfig(labelAngle=0)), y=alt.Y('counts', title='Número de acidentes'))
st.altair_chart(chart, use_container_width=True)


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



st.write("Aqui está um gráfico de regressão para prever o número de acidentes baseado na hora do dia:")
# Cria coluna com a hora como números
df['hora_numerica'] = df['hora'].apply(lambda x: x.hour)

# Agrupa por hora e calcula a média do número de acidentes em cada hora
hora_counts = df.groupby('hora_numerica')['Unnamed: 0'].agg(['count']).reset_index()
hora_counts = hora_counts.groupby('hora_numerica')['count'].agg(['mean']).reset_index()
hora_counts.columns = ['hora', 'mean']
# Plota o gráfico de dispersão com a regressão linear
fig, ax = plt.subplots()
sns.regplot(x='hora', y='mean', data=hora_counts, scatter_kws={'s': 20}, ax = ax)
st.pyplot(fig)


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