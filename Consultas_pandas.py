import pandas as pd
    # Abertura do DataSet
df = pd.read_excel("data/DataSetAcidentesRecife.xlsx")
df.rename(columns={'auto':'carro'}, inplace=True) # Alteração de nome de coluna

    # Resultado quantitavo anual de vitimas e vitimas fatais. Filtro = Ano
print(df.groupby(['Ano']).sum()[['vitimas', 'vitimasfatais']].sort_values(by='Ano'))

    # Resultado quantitativo anual de acidentes por tipo de veiculo. Filtro = Veiculo
print(df.groupby(['Ano']).sum()[['moto', 'carro', 'caminhao','onibus']].sort_values(by='Ano'))

    # Resultado quantitativo anual de acidentes por tipo de veiculo. Filtro = Condição da via
print(df.groupby(['Ano', 'condicao_via']).sum()[['moto', 'carro', 'caminhao','onibus']].sort_values(by='Ano'))