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

#Tratar natureza_acidente
#Define 0 para None e outros valores errados
df['natureza_acidente'] = df['natureza_acidente'].fillna(0)
df['natureza_acidente'] = df['natureza_acidente'].replace('0', 0)
df['natureza_acidente'] = df['natureza_acidente'].replace('1', 0)


#Tratar situacao
#Define 0 para None
df['situacao'] = df['situacao'].fillna(0)

#Tratar bairro
#Define 0 para None e outros valores errados
df['bairro'] = df['bairro'].fillna(0)
df['bairro'] = df['bairro'].replace('BAIRRO DO RECIFE', 'RECIFE')
df['bairro'] = df['bairro'].replace('BOA  VIAGEM', 'BOA VIAGEM')
df['bairro'] = df['bairro'].replace('BOMBA DO HEMETERIO', 'BOMBA DO HEMETÉRIO')
df['bairro'] = df['bairro'].replace('FABIO', 0)
df['bairro'] = df['bairro'].replace('IPESEP', 'IPSEP')
df['bairro'] = df['bairro'].replace('JOANA BEZERRA', 'ILHA JOANA BEZERRA')
df['bairro'] = df['bairro'].replace('MARCELO', 0)
df['bairro'] = df['bairro'].astype(str)

# endereco
df['endereco'] = df['endereco'].astype(str)

# detalhe_endereco_acidente
df['detalhe_endereco_acidente'] = df['detalhe_endereco_acidente'].astype(str)

# complemento
df['complemento'] = df['complemento'].astype(str)

# bairro_cruzamento
df['bairro_cruzamento'] = df['bairro_cruzamento'].astype(str)

# sentido_via
df['sentido_via'] = df['sentido_via'].astype(str)

# acidente_verificado
df['acidente_verificado'] = df['acidente_verificado'].astype(str)

# situacao_semaforo
df['situacao_semaforo'] = df['situacao_semaforo'].astype(str)

# ponto_controle
df['ponto_controle'] = df['ponto_controle'].astype(str)

# situacao_placa
df['situacao_placa'] = df['situacao_placa'].astype(str)

#Tratar vitimas
#Define 0 para None
df['vitimas'] = df['vitimas'].fillna(0)
df['vitimas'] = df['vitimas'].astype('int64')


#Tratar vitimasfatais
#Define 0 para None
df['vitimasfatais'] = df['vitimasfatais'].fillna(0)
df['vitimasfatais'] = df['vitimasfatais'].astype('int64')

#Tratar sentido_via
#Define 0 para None
df['sentido_via'] = df['sentido_via'].fillna(0)

#Tratar tipo
#Define 0 para None e outros valores errados
df['tipo'] = df['tipo'].fillna(0)
df['tipo'] = df['tipo'].replace('0', 0)
df['tipo'] = df['tipo'].replace('APOIO COMPESA', 0)
df['tipo'] = df['tipo'].replace('ATROPELAMENTO DE PESSOA', 'ATROPELAMENTO')
df['tipo'] = df['tipo'].replace('ATROPELAMENTO ANIMAL', 'ATROPELAMENTO DE ANIMAL')
df['tipo'] = df['tipo'].replace('COLISAO', 'COLISÃO')
df['tipo'] = df['tipo'].replace('FISCALIZAÇÃO', 0)
df['tipo'] = df['tipo'].replace('MONITORAMENTO', 0)
df['tipo'] = df['tipo'].replace('MMMMMMMMMMMMNNNNNNNNNNNNNNC', 0)
df['tipo'] = df['tipo'].replace('OUTROS APOIOS', 'OUTROS')
df['tipo'] = df['tipo'].replace('SANTO AMARO', 0)
df['tipo'] = df['tipo'].replace('SEMÁFORO', 0)
df['tipo'] = df['tipo'].replace('SUBURBIO', 0)