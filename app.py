import pandas as pd

import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", #Aqui eu configuro o setpage ou seja, informo as infos da página quando eu criar
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") #Aqui eu abro o nosso dataset


# SIDEBAR
st.sidebar.header("Filtre aqui por ano:") #Cada SIDEBAR é composto pelo cabeçalho seguido da nossa variavel que vai armazenar o filtro e eu posso colocar as opções de acordo com o meu dataset e um padrão para começar o filtro, nesse caso eu coloquei para pegar todos as opções que tem nas colunas
ano = st.sidebar.multiselect(
    "Selecione o ano: ",
    options=df["Ano"].unique(),
    default=df["Ano"].unique()
)

st.sidebar.header("Filtre aqui por natureza do acidente:")
nat_acidente = st.sidebar.multiselect(
    "Selecione a natureza do acidente: ",
    options=df["natureza_acidente"].unique(),
    default=df["natureza_acidente"].unique()
)

st.sidebar.header("Filtre aqui por bairro :")
bairro = st.sidebar.multiselect(
    "Selecione o bairro: ",
    options=df["bairro"].unique(),
    default=df["bairro"].unique()
)

st.sidebar.header("Filtre aqui por tempo_clima:")
tempo_clima = st.sidebar.multiselect(
    "Selecione o tempo clima: ",
    options=df["tempo_clima"].unique(),
    default=df["tempo_clima"].unique()
)

df_selection = df.query( #Aqui eu vou atribuir a varivavel que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & natureza_acidente == @nat_acidente & bairro == @bairro & tempo_clima == @tempo_clima" #O @ significa que estou chamando a varivel que criei lá no sidebar
)
st.dataframe(df_selection) #Aqui eu chamo nosso dataset para ele aparecer



##### Gráficos #####

#Vítimas fatais por ano  (Interativo)
df_selection.rename(columns={'vitimasfatais':'Vítimas Fatais'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'acidente_verificado':'Localização na via'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'condicao_via':'Condição da via'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'vitimas':'Número de vítimas'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True) # altera o nome da coluna



vitimasFatais = df_selection.groupby(['Ano']).sum(numeric_only=True)['Vítimas Fatais'] # soma o total de vítimas fatais em cada ano
st.bar_chart(vitimasFatais)


# Acidentes de acordo com o clima




# Vítimas x Acidentes Verificados (Interativo)
VitimasLocalizaçãoVia = df_selection[['Localização na via', 'Número de vítimas']]

bar_chart = alt.Chart(VitimasLocalizaçãoVia).mark_bar().encode(
    y= 'Localização na via',
    x= 'Número de vítimas'
)
st.altair_chart(bar_chart, use_container_width=True)


# Vítimas x Condição da Via (Interativo)
VitimasCondicaoVia = df_selection[['Condição da via', 'Número de vítimas']]
bar_chart = alt.Chart(VitimasCondicaoVia).mark_bar().encode(
    y= 'Condição da via',
    x= 'Número de vítimas'
)
st.altair_chart(bar_chart, use_container_width=True)

# Vítimas x Bairro (Interativo)
VitimasBairro = df_selection[['Bairro', 'Número de vítimas']]
bar_chart = alt.Chart(VitimasBairro).mark_bar().encode(
    y= 'Bairro',    
    x= 'Número de vítimas'
).properties(height=700)
st.altair_chart(bar_chart, use_container_width=True)






hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
