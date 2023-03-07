import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.


st.title("Acidentes por Clima")



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
    options=df["bairro"].unique()
    
)
st.sidebar.header("Filtre aqui por clima:")
clima = st.sidebar.multiselect(
    "Selecione o bairro: ",
    options=df["tempo_clima"].unique(),
    default=df["tempo_clima"].unique()
)



df_selection = df.query( # Aqui eu vou atribuir a variável que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro & tempo_clima == @clima" #O @ significa que estou chamando a variável que criei lá no sidebar
)
# st.dataframe(df_selection) # Abertura do Dataset

# Alteração dos nomes das colunas
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True)
df_selection.rename(columns={'tempo_clima':'Clima'}, inplace=True)
df_selection.rename(columns={'condicao_via':'Condição da via'}, inplace=True)


#Gráfico Ano x Clima x Registros

climaAno = df_selection.groupby(['Ano','Clima'], as_index=False)['Clima'].size()

bars = alt.Chart(climaAno).mark_bar().encode(
    x=alt.X('sum(size):Q', stack='zero', title='Quantidade de Ocorrências'),
    y=alt.Y('Ano'),
    color=alt.Color('Clima')
).properties(   # propriedades do gráfico
    title='Clima x Ocorrências', # adiciona o titulo no gráfico
    width= 1000,
    height=400
)
text = alt.Chart(climaAno).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(size):Q', title='Quantidade de Ocorrências', stack='zero'),
    y=alt.Y('Ano:N'),
    detail='Clima:N',
    text=alt.Text('sum(size):Q', title='Quantidade de Ocorrências')
)

st.altair_chart(bars + text, use_container_width=True)
# Fim do gráfico de barras estacadas


# Gráfico Clima x Bairro

#

climaBairro = df_selection.groupby(['Bairro','Clima'], as_index=False)['Clima'].size()
# st.dataframe(climaBairro)

bars = alt.Chart(climaBairro).mark_circle().encode(
   x='size:Q',
    y='bairro:N',
    color='Clima',
).interactive()
#Termina o Gráfico de bolinhas
# st.altair_chart(bars, use_container_width=True)

# Acidentes x Clima
QuantCasosClima =  df_selection.groupby(['Clima'], as_index=False)['Clima'].size()
# st.dataframe(QuantCasosClima)
QuantCasosClima = QuantCasosClima.reset_index() # transforma o index em uma coluna

pie_chart = alt.Chart(QuantCasosClima).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="size", type="quantitative", title="Quantidade de Casos"),
    color=alt.Color(field="Clima", type="nominal"),
).properties(   # propriedades do gráfico
    title='Quantidade Casos x Clima' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(pie_chart, use_container_width=True)

CasosCondicaoVia = df_selection.groupby('Condição da via')['Clima'].size()
CasosCondicaoVia= CasosCondicaoVia.reset_index() # transforma o index em uma coluna

donut_chart = alt.Chart(CasosCondicaoVia).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Clima", type="quantitative"),
    color=alt.Color(field="Condição da via", type="nominal"),
).properties(   # propriedades do gráfico
    title='Quantidade de Condição da via x Clima' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(donut_chart, use_container_width=True)