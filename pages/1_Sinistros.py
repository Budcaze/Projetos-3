import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.


st.title("Vitimas Fatais")

st.title("Sinistros")


# Converte o tipo das colunas para inteiro
df['vitimas'] = df['vitimas'].fillna(0) # substitui o vazio por 0
df['vitimas'] = df['vitimas'].astype('int64') # Converte para inteiro

df['vitimasfatais'] = df['vitimasfatais'].fillna(0) # substitui o vazio por 0
df['vitimasfatais'] = df['vitimasfatais'].astype('int64') # Converte para inteiro

# Converte o ano para string
df['Ano'] = df['Ano'].astype('str') #Converte para string

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

st.sidebar.header("Filtre aqui por Clima:")
mask_clima = ~df["tempo_clima"].isin([None])    # define como false os valores da coluna iguais a None
filtrar_clima = df["tempo_clima"].loc[mask_clima]   # seleciona apenas o valores com true
tempo_clima = st.sidebar.multiselect(
    "Selecione o tempo clima: ",
    options=filtrar_clima.unique(),
    default=filtrar_clima.unique()
)
df_selection = df.query( # Aqui eu vou atribuir a variável que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro & tempo_clima == @tempo_clima" #O @ significa que estou chamando a variável que criei lá no sidebar
)
st.dataframe(df_selection) # Abertura do Dataset

# Alteração dos nomes das colunas
df_selection.rename(columns={'vitimasfatais':'Vítimas Fatais'}, inplace=True)
df_selection.rename(columns={'acidente_verificado':'Localização na via'}, inplace=True)
df_selection.rename(columns={'condicao_via':'Condição da via'}, inplace=True)
df_selection.rename(columns={'vitimas':'Número de vítimas'}, inplace=True)
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True)
df_selection.rename(columns={'tempo_clima':'Clima'}, inplace=True)



VitimasFatais = df_selection.groupby(['Ano'])['Vítimas Fatais'].sum()
VitimasFatais = VitimasFatais.reset_index()

st.write(df.groupby(['Ano']).sum()[['vitimasfatais']].sort_values(by='Ano'))

bar_chart = alt.Chart(VitimasFatais).mark_bar(color='red').encode(      # color= '', define a cor do gráfico
    x= 'Ano',
    y= 'Vítimas Fatais'
).configure_axisX(      # propriedades do eixo x
    labelAngle=0    # rotaciona os labels do eixo x
).properties(   # propriedades do gráfico
    title='Vítimas Fatais por Ano' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(bar_chart, use_container_width=True)

VitimasBairro = df_selection.groupby('Bairro')['Vítimas Fatais'].sum()
VitimasBairro = VitimasBairro.reset_index()

bar_chart = alt.Chart(VitimasBairro).mark_bar(color='#D33210').encode(
    y= alt.Y('Bairro', sort='-x'), # sort='-x' ordena Y em ordem decrescente de acordo com os valores do eixo X
    x= 'Vítimas Fatais',
).properties(   # propriedades do gráfico
    title='Vítimas fatais por Bairro' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,  # tamanho da fonte
    anchor= 'middle',   # centraliza o titulo
    color= 'black'  # cor do titulo
)  
st.altair_chart(bar_chart, use_container_width=True)

VitimasClima = df_selection.groupby('Clima')['Vítimas Fatais'].sum()
VitimasClimaBom = VitimasClima
# VitimasClimaChuvoso =
# VitimasClimaNublado = 
VitimasClima = VitimasFatais.reset_index()

source = pd.DataFrame({"category": ["Bom", "Chuvoso", "Nublado"], "value": [VitimasClimaBom, 6, 10,]})

Donut = alt.Chart(source).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),
).properties(
    title = "Vítimas Fatais por Clima"
)
st.altair_chart(Donut, use_container_width=True)

