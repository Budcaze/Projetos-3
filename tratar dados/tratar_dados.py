import pandas as pd

df = pd.read_parquet('data/DataSetAcidentesRecife.parquet')

################# REMOVE OS VALORES VAZIOS OU ERRADOS #################

# Remover a coluna Unnamed: 0
df = df.drop('Unnamed: 0', axis=1)

#Tratar data
#Define 0 para None
df['data'] = df['data'].fillna(0)
df['data'] = pd.to_datetime(df['data'])

#Tratar hora
#Define 0 para None
df['hora'] = df['hora'].fillna(0)
df['hora'] = df['hora'].astype(str)