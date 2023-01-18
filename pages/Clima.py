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
    options=df["bairro"].unique(),
    default=df["bairro"].unique()
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
st.dataframe(df_selection) # Abertura do Dataset

# Alteração dos nomes das colunas
df_selection.rename(columns={'vitimasfatais':'Vítimas Fatais'}, inplace=True)
df_selection.rename(columns={'acidente_verificado':'Localização na via'}, inplace=True)
df_selection.rename(columns={'condicao_via':'Condição da via'}, inplace=True)
df_selection.rename(columns={'vitimas':'Número de vítimas'}, inplace=True)
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True)
df_selection.rename(columns={'tempo_clima':'Clima'}, inplace=True)

Total_acidentes = df_selection.groupby(['Ano']).sum()
Total_acidentes = Total_acidentes.reset_index()

st.write(df.groupby(['tempo_clima']).sum())

