import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.

st.title("Vítimas")

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



df_selection = df.query( #Aqui eu vou atribuir a varivavel que eu criei nos sidebars as colunas do dataset
    "Ano == @ano & bairro == @bairro" #O @ significa que estou chamando a varivel que criei lá no sidebar
)
st.dataframe(df_selection) #Aqui eu chamo nosso dataset para ele aparecer



##### Gráficos #####

#Vítimas fatais por ano  (Interativo)
df_selection.rename(columns={'vitimasfatais':'Vítimas Fatais'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'acidente_verificado':'Localização na via'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'condicao_via':'Condição da via'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'vitimas':'Número de vítimas'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'bairro':'Bairro'}, inplace=True) # altera o nome da coluna
df_selection.rename(columns={'tempo_clima':'Clima'}, inplace=True) # altera o nome da coluna

VitimasTotais = df_selection.groupby(['Ano'])['Número de vítimas'].sum()
VitimasTotais = VitimasTotais.reset_index()


bar_chart = alt.Chart(VitimasTotais).mark_bar(color='#00BFFF').encode(      # color= '', define a cor do gráfico
    x= 'Ano',
    y= 'Número de vítimas'
).configure_axisX(      # propriedades do eixo x
    labelAngle=0    # rotaciona os labels do eixo x
).properties(   # propriedades do gráfico
    title='Total de Vítimas' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(bar_chart, use_container_width=True)

# Acidentes x Clima x Ano
data = df_selection['data']
df_selection['data'] = pd.to_datetime(data)     # converte a coluna para o tipo date
df_selection['data'] = df_selection['data'].dt.strftime('%y-%m') # seleciona apenas o mês e ano, ex: feb/21
VitimasTempoAno = df_selection.groupby(['data','Clima'], as_index=False)['Número de vítimas'].sum()     # agrupa a quantidade vitimas por data e clima, as_index=False transforma a soma de vitimas em uma coluna

bar_chart = alt.Chart(VitimasTempoAno).mark_circle(size=100).encode(
    x= alt.X('data:O', title='Data'),     # alt.X permite alterar propriedades do eixo X
    y= 'Número de vítimas',
    color= 'Clima',         # passando uma coluna em color podemos ter uma cor para cada valor único
    tooltip=['Clima', 'Número de vítimas']  # informações que aparecem quando passamos o mouse
).configure_axisX(      # propriedades do eixo x
    labelAngle=0    # rotaciona os labels do eixo x
).properties(   # propriedades do gráfico
    title='Quantidade de Vitimas x Clima' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(bar_chart, use_container_width=True)



# Vítimas x Condição da Via (Interativo)
VitimasCondicaoVia = df_selection.groupby('Condição da via')['Número de vítimas'].sum()
VitimasCondicaoVia = VitimasCondicaoVia.reset_index()
bar_chart = alt.Chart(VitimasCondicaoVia).mark_bar().encode(
    y= alt.Y('Condição da via', sort='-x'), # sort='-x' ordena Y em ordem decrescente de acordo com os valores do eixo X
    x= 'Número de vítimas',
    color='Condição da via'  # passando uma coluna em color podemos ter uma cor para cada valor único
).properties(   # propriedades do gráfico
    title='Vítimas x Condição da Via' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,  # tamanho da fonte
    anchor= 'middle',   # centraliza o titulo
    color= 'black'  # cor do titulo
)  
st.altair_chart(bar_chart, use_container_width=True)

# Vítimas x Bairro (Interativo)
VitimasBairro = df_selection.groupby('Bairro')['Número de vítimas'].sum()
VitimasBairro = VitimasBairro.reset_index()
bar_chart = alt.Chart(VitimasBairro).mark_bar(color='#7FFFD4').encode(
    y= alt.Y('Bairro', sort='-x'), # sort='-x' ordena Y em ordem decrescente de acordo com os valores do eixo X
    x= 'Número de vítimas',
    
).properties(   # propriedades do gráfico
    title='Vítimas por Bairro' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,  # tamanho da fonte
    anchor= 'middle',   # centraliza o titulo
    color= 'black'  # cor do titulo
)  
st.altair_chart(bar_chart, use_container_width=True)

# VitimasBairro = df_selection[['bairro', 'vitimas']]
# bar_chart = alt.Chart(VitimasBairro).mark_bar().encode(
#     y= 'bairro',  
#     x= 'vitimas'
# ).properties(height=700)
# st.altair_chart(bar_chart, use_container_width=True)

# VitimasBairro = df_selection.groupby('Bairro')['Número de vítimas'].sum() #agrupa a quantidade de vitimas por bairro
# VitimasBairro = VitimasBairro.reset_index()     # transforma o index (que era o nome do bairro quando agrupou) em coluna
# VitimasBairro.sort_values('Número de vítimas',ascending=False, inplace=True)    # Classifica em ordem decrescente


# bar_chart = alt.Chart(VitimasBairro[0:10]).mark_bar(color='#03bb85').encode(       # exibe apenas o top 10
#     y= alt.Y('Bairro', sort='-x'),  # Classifica os bairros em ordem decrescente no gráfico
#     x= 'Número de vítimas'
# ).properties(   # propriedades do gráfico
#     height=400,  # altura do gráfio
#     title='Vítimas Por Bairro' # adiciona o titulo no gráfico
# ).configure_title(  # formata o titulo
#     fontSize = 20,  # tamanho da fonte
#     anchor= 'middle',   # centraliza o titulo
#     color= 'black'  # cor do titulo
# )  
# st.altair_chart(bar_chart, use_container_width=True)





hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)