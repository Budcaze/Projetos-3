import pandas as pd

import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", #Aqui eu configuro o setpage ou seja, informo as infos da página quando eu criar
    page_icon=":kissing_smiling_eyes:",
    layout="wide")
df = pd.read_excel("data/DataSetAcidentesRecife.xlsx") #Aqui eu abro o nosso dataset


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





bar_chart = alt.Chart(df).mark_bar().encode(
    y= 'vitimas',
    x= 'acidente_verificado'
)
st.altair_chart(bar_chart, use_container_width=True)


bar_chart = alt.Chart(df).mark_bar().encode(
    y= 'vitimas',
    x= 'condicao_via'
)
st.altair_chart(bar_chart, use_container_width=True)

bar_chart = alt.Chart(df).mark_bar().encode(
    y= 'vitimas',
    x= 'bairro'
)
st.altair_chart(bar_chart, use_container_width=True)






hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
