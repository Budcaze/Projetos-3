import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", # Configuração do setpage, ou seja, informações da página.
    page_icon=":warning:",
    layout="wide")
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet") # Abertura do DataSet.

st.title("Geral")

# Converte o tipo das colunas para inteiro
df['vitimas'] = df['vitimas'].fillna(0) # substitui o vazio por 0
df['vitimas'] = df['vitimas'].astype('int64') # Converte para inteiro

df['vitimasfatais'] = df['vitimasfatais'].fillna(0) # substitui o vazio por 0
df['vitimasfatais'] = df['vitimasfatais'].astype('int64') # Converte para inteiro

# Converte o ano para string
df['Ano'] = df['Ano'].astype('str') #Converte para string

#converte para datatime
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S')

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

vitimasOrg = VitimasTotais = df_selection.groupby(['Ano'])['Número de vítimas'].sum().sort_values(ascending=False)
vitimasOrg = vitimasOrg.reset_index()
ano_primeira_linha = vitimasOrg['Ano'].iloc[0]
media_vitimas = VitimasTotais.mean()
#st.dataframe(vitimasOrg)
left_column, middle_column, right_column = st.columns(3)
with middle_column:
    st.subheader(f"Ano com mais vítimas: {ano_primeira_linha}")
    st.subheader(f"Média anual de vítimas: {media_vitimas}")
st.markdown("---------")

anoVitimas = df_selection[['Ano', 'Número de vítimas']]

# Gráficos

### Tendência de acidentes e vítimas ao longo dos anos ###
linechart = alt.Chart(anoVitimas).mark_line().encode(
    x=alt.X("Ano", axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    y=alt.Y("sum(Número de vítimas)", title='Número de Vítimas'),
    #color=alt.datum(alt.repeat("layer")),
).properties(   # propriedades do gráfico
    title='Tendência de acidentes com vítimas ao longo dos anos' # adiciona o titulo no gráfico
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(linechart, use_container_width=True)


### Vítimas Fatais por Ano ###

VitimasFatais = df_selection.groupby(['Ano'])['Vítimas Fatais'].sum()
VitimasFatais = VitimasFatais.reset_index()

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

### Distribuição dos veículos envolvidos em acidentes ###

# define a lista de colunas de veículos
veiculos_data = []
veiculos = ['auto', 'moto', 'ciclom', 'ciclista', 'onibus', 'caminhao', 'viatura', 'outros']

# transforma os dados em um formato apropriado para o gráfico
for veiculo in veiculos:
    veiculos_data.append({'Tipo de veículo': veiculo, 'Quantidade': df_selection[veiculo].sum()})

veiculos_df = pd.DataFrame(veiculos_data)


chart = alt.Chart(veiculos_df).mark_bar().encode(
    x=alt.X('Tipo de veículo', sort=veiculos, axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    y='Quantidade',
    color=alt.Color('Tipo de veículo', sort=veiculos),
    tooltip=['Tipo de veículo', 'Quantidade']
).properties(
    title='Distribuição de veículos envolvidos em acidentes'
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(chart, use_container_width=True)


### Relação entre a hora do acidente e a quantidade de acidentes ###
horaAcidentes = df_selection[['hora', 'Número de vítimas']]
horaAcidentes['hora'] = horaAcidentes['hora'].dt.hour

scatter = alt.Chart(horaAcidentes).mark_circle(size=60).encode(
    x=alt.X('hora', axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    y=alt.Y('sum(Número de vítimas)', title="Quantidade de vítimas"),
    #tooltip=[]
).interactive().properties(
    title='Relação entre a hora do acidente e a quantidade de acidentes'
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(scatter, use_container_width=True)

#### fatais x hora #####

### Relação entre a hora do acidente e a quantidade de óbitos ###
horaAcidentes = df_selection[['hora', 'Vítimas Fatais']]
horaAcidentes['hora'] = horaAcidentes['hora'].dt.hour

scatter = alt.Chart(horaAcidentes).mark_circle(size=60).encode(
    x=alt.X('hora', axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    y=alt.Y('sum(Vítimas Fatais)', title= "Quantidade de óbitos"),
    #tooltip=[]
).interactive().properties(
    title='Relação entre a hora do acidente e a quantidade de óbitos'
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
) 
st.altair_chart(scatter, use_container_width=True)


###  ###

tipoAcAno = df_selection.groupby(['Ano','tipo'], as_index=False)['tipo'].size()

streamgraph = alt.Chart(tipoAcAno).mark_area().encode(
    alt.X('Ano', axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    alt.Y('sum(size):Q', axis=None, title='Quantidade de Ocorrências'),
    alt.Color('tipo',
        scale=alt.Scale(scheme='category20b')
    )
).interactive(

).properties(   # propriedades do gráfico
  title='Tipo do Acidente x Ocorrências', # adiciona o titulo no gráfico
    width= 900,
    height=400
).configure_legend(labelLimit=0)    #exibir o texto da legenda por completo

st.altair_chart(streamgraph, use_container_width=True)


### Vitimas x velocidade maxima x Condição da via###
vitimasVelVia = df_selection[['Número de vítimas', 'Condição da via', 'velocidade_max_via']]
vitimasVelVia = vitimasVelVia.dropna()    #remove os nulos
scatter1 = alt.Chart(vitimasVelVia).mark_circle(size=60).encode(
    x=alt.X('velocidade_max_via', title='Velocidade Máxima da Via',axis=alt.Axis(labelAngle=0, domain=False, tickSize=0)),
    y=alt.Y('Número de vítimas'),
    color='Condição da via',
    size='Número de vítimas'
).interactive().properties(
    title='Relação entre a Condição, Velocidade máxima da via e a quantidade de acidentes com vítimas'
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
).configure_legend(labelLimit=0)    #exibir o texto da legenda por completo
st.altair_chart(scatter1, use_container_width=True)

###  ###
velFatal = df_selection[['Vítimas Fatais', 'velocidade_max_via']]
heat = alt.Chart(velFatal).mark_rect().encode(
    alt.X('Vítimas Fatais:Q', title='Vítimas Fatais', bin=alt.Bin(maxbins=60)),
    alt.Y('velocidade_max_via:Q', title='Velocidade Máxima da Via', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
).interactive().properties(
    title='Vítimas Fatais x Velocidade Máxima da Via'
).configure_title(  # formata o titulo
    fontSize = 20,
    anchor= 'middle',   # centraliza o titulo
    color= 'black'
)
st.altair_chart(heat, use_container_width=True)

#######
scatter = alt.Chart(df_selection).mark_point().encode(x='Número de vítimas', y='velocidade_max_via')
st.altair_chart(scatter, use_container_width=True)



#Valores totais de acidentes por ano (quantidade de vezes que cada ano aparece no dataset)

lista = df.groupby('Ano')['Ano'].transform('count')
# st.write(lista) #teste visual comrpovando número de vezes que x Ano está rpesente
ano2015 = lista.loc[0] #linha 0 (inicial que é 2015) nessa 'lista' feita com o groupby
indiceDeComeco = ano2015 #indiceDeComeco seta em que linha começará o próximo ano
ano2016 = lista.loc[indiceDeComeco] #linha buscada de acordo com fim da contagem dos anos anteriores
indiceDeComeco += ano2016
ano2017 = lista.loc[indiceDeComeco]
indiceDeComeco += ano2017
ano2018 = lista.loc[indiceDeComeco]
indiceDeComeco += ano2018
ano2019 = lista.loc[indiceDeComeco]
indiceDeComeco += ano2019
ano2020 = lista.loc[indiceDeComeco]
indiceDeComeco += ano2020
ano2021 = lista.loc[indiceDeComeco]





hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)