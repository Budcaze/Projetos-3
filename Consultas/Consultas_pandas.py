import pandas as pd
    # Abertura do DataSet
df = pd.read_parquet("data/DataSetAcidentesRecife.parquet")
df.rename(columns={'auto':'carro'}, inplace=True) # Alteração de nome de coluna
df.rename(columns={'acidente_verificado':'Localização na via'}, inplace=True)

    # Quantitativo anual de vitimas e vitimas fatais. Filtro = Ano
print(df.groupby(['Ano']).sum()[['vitimas','vitimasfatais']].sort_values(by='Ano'))

    # Quantitativo anual de acidentes por tipo de veiculo. Filtro = Veiculo
print(df.groupby(['Ano']).sum()[['moto', 'carro', 'caminhao','onibus']].sort_values(by='Ano'))

    # Quantitativo anual de acidentes por tipo de veiculo. Filtro = Condição da via
print(df.groupby(['Ano', 'condicao_via']).sum()[['moto', 'carro', 'caminhao','onibus']].sort_values(by='Ano'))

    # Quantitativo anual de acidentes com vitimas por Bairro. Filtro = Bairro
print(df.groupby(['bairro']).sum()[['vitimasfatais']].sort_values(by='bairro'))

    # Quantitativo anual de acidentes com vitimas por região da via. Filtro = Localização na via
print(df.groupby(['Localização na via']).sum()[['vitimas']].sort_values(by='Localização na via'))

"""
    Usar resultados das respectivas consultas acima para validar resultados apresentados no gráficos
"""