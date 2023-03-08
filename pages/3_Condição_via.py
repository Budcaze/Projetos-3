import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.


st.title("Acidentes por Condição da via")



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
st.sidebar.header("Filtre aqui por condição da via:")
cond_via = st.sidebar.multiselect(
    "Selecione a condição da via: ",
    options=df["condicao_via"].unique(),
    default=df["condicao_via"].unique()
)



df_selection = df.query( # Aqui eu vou atribuir a variável que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro & condicao_via == @cond_via" #O @ significa que estou chamando a variável que criei lá no sidebar
)
#st.dataframe(df_selection) # Abertura do Dataset

# Alteração dos nomes das colunas
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True)
df_selection.rename(columns={'tempo_clima':'Clima'}, inplace=True)


#Gráfico Ano x Clima x Registros

condicao_via_Ano = df_selection.groupby(['Ano','condicao_via'], as_index=False)['condicao_via'].size()

bars = alt.Chart(condicao_via_Ano).mark_bar().encode(
    x=alt.X('sum(size):Q', stack='zero', title='Quantidade de Ocorrências'),
    y=alt.Y('Ano'),
    color=alt.Color('condicao_via', title='Condição da via')
).properties(   # propriedades do gráfico
    title='Condição via x Ocorrências', # adiciona o titulo no gráfico
    width= 1000,
    height=400
)

chart1 = alt.layer(bars).configure_title(    # edita o titulo
    fontSize = 20,
    anchor= 'middle',
    color= 'black'
)

text = alt.Chart(condicao_via_Ano).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(size):Q', title='Quantidade de Ocorrências', stack='zero'),
    y=alt.Y('Ano:N'),
    detail='condicao_via:N',
    text=alt.Text('sum(size):Q', title='Quantidade de Ocorrências')
)

st.altair_chart(chart1 + text, use_container_width=True)
# Fim do gráfico de barras estacadas





CasosCondicaoVia = df_selection.groupby('condicao_via').size()
CasosCondicaoVia= CasosCondicaoVia.reset_index() # transforma o index em uma coluna

donut_chart = alt.Chart(CasosCondicaoVia).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="condicao_via", type="quantitative"),
    color=alt.Color(field="condicao_via", type="nominal"),
).properties(   # propriedades do gráfico
    title='Quantidade de Condição da via x Clima' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(donut_chart, use_container_width=True)