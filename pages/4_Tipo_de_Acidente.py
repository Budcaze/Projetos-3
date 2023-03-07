import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.


st.title("Acidentes por Tipo de Acidente")



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
st.sidebar.header("Filtre aqui por tipo de acidente:")
tipoAc = st.sidebar.multiselect(
    "Selecione o bairro: ",
    options=df["tipo"].unique(),
    default=df["tipo"].unique()
)



df_selection = df.query( # Aqui eu vou atribuir a variável que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro & tipo == @tipoAc" #O @ significa que estou chamando a variável que criei lá no sidebar
)
#st.dataframe(df_selection) # Abertura do Dataset

# Alteração dos nomes das colunas
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True)
df_selection.rename(columns={'tipo':'Tipo do Acidente'}, inplace=True)


#Gráfico Ano x Tipo do Acidente x Registros

tipoAcAno = df_selection.groupby(['Ano','Tipo do Acidente'], as_index=False)['Tipo do Acidente'].size()

bars = alt.Chart(tipoAcAno).mark_bar().encode(
    x=alt.X('sum(size):Q', stack='zero', title='Quantidade de Ocorrências'),
    y=alt.Y('Ano'),
    color=alt.Color('Tipo do Acidente')
).properties(   # propriedades do gráfico
    title='Tipo do Acidente x Ocorrências', # adiciona o titulo no gráfico
    width= 1000,
    height=400
)
text = alt.Chart(tipoAcAno).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(size):Q', title='Quantidade de Ocorrências', stack='zero'),
    y=alt.Y('Ano:N'),
    detail='Tipo do Acidente:N',
    text=alt.Text('sum(size):Q', title='Quantidade de Ocorrências')
)

st.altair_chart(bars + text, use_container_width=True)
# Fim do gráfico de barras estacadas


# Gráfico Tipo do Acidente x Bairro

#

tipoAcBairro = df_selection.groupby(['Bairro','Tipo do Acidente'], as_index=False)['Tipo do Acidente'].size()
#st.dataframe(tipoAcBairro)

bars = alt.Chart(tipoAcBairro).mark_circle().encode(
   x='size:Q',
    y='bairro:N',
    color='Tipo do Acidente',
).interactive()
#Termina o Gráfico de bolinhas
#st.altair_chart(bars, use_container_width=True)

# Acidentes x Tipo do Acidente
QuantCasosTipoAc =  df_selection.groupby(['Tipo do Acidente'], as_index=False)['Tipo do Acidente'].size()
#st.dataframe(QuantCasosTipoAc)
QuantCasosTipoAc = QuantCasosTipoAc.reset_index() # transforma o index em uma coluna

pie_chart = alt.Chart(QuantCasosTipoAc).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="size", type="quantitative", title="Quantidade de Casos"),
    color=alt.Color(field="Tipo do Acidente", type="nominal"),
).properties(   # propriedades do gráfico
    title='Quantidade Casos x Tipo do Acidente' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(pie_chart, use_container_width=True)

CasosCondicaoVia = df_selection.groupby('condicao_via')['Tipo do Acidente'].size()
CasosCondicaoVia= CasosCondicaoVia.reset_index() # transforma o index em uma coluna

donut_chart = alt.Chart(CasosCondicaoVia).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Tipo do Acidente", type="quantitative"),
    color=alt.Color(field="condicao_via", type="nominal"),
).properties(   # propriedades do gráfico
    title='Quantidade de Condição da via x Tipo do Acidente' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(donut_chart, use_container_width=True)