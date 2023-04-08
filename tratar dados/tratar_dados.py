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

#Tratar auto
#Define 0 para None
df['auto'] = df['auto'].fillna(0)
df['auto'] = df['auto'].astype('int64')

#Tratar moto
#Define 0 para None
df['moto'] = df['moto'].fillna(0)
df['moto'] = df['moto'].astype('int64')

#Tratar ciclom
#Define 0 para None
df['ciclom'] = df['ciclom'].fillna(0)
df['ciclom'] = df['ciclom'].astype('int64')

#Tratar ciclista
#Define 0 para None
df['ciclista'] = df['ciclista'].fillna(0)
df['ciclista'] = df['ciclista'].astype('int64')

#Tratar pedestre
#Define 0 para None
df['pedestre'] = df['pedestre'].fillna(0)
df['pedestre'] = df['pedestre'].astype('int64')

#Tratar onibus
#Define 0 para None
df['onibus'] = df['onibus'].fillna(0)
df['onibus'] = df['onibus'].astype('int64')

#Tratar caminhao
#Define 0 para None
df['caminhao'] = df['caminhao'].fillna(0)
df['caminhao'] = df['caminhao'].astype('int64')

#Tratar viatura
#Define 0 para None
df['viatura'] = df['viatura'].fillna(0)
df['viatura'] = df['viatura'].astype('int64')

#Tratar outros
#Define 0 para None
df['outros'] = df['outros'].fillna(0)
df['outros'] = df['outros'].astype('int64')

#Tratar acidente_verificado
#Define 0 para None
df['acidente_verificado'] = df['acidente_verificado'].fillna(0)

#Tratar tempo_clima
#Define 0 para None
df['tempo_clima'] = df['tempo_clima'].fillna(0)

#Tratar situacao_semaforo
#Define 0 para None
df['situacao_semaforo'] = df['situacao_semaforo'].fillna(0)

#Tratar sinalizacao
#Define 0 para None
df['sinalizacao'] = df['sinalizacao'].fillna(0)

#Tratar condicao_via
#Define 0 para None
df['condicao_via'] = df['condicao_via'].fillna(0)

#Tratar conservacao_via
#Define 0 para None
df['conservacao_via'] = df['conservacao_via'].fillna(0)

#Tratar ponto_controle
#Define 0 para None
df['ponto_controle'] = df['ponto_controle'].fillna(0)

#Tratar situacao_placa
#Define 0 para None
df['situacao_placa'] = df['situacao_placa'].fillna(0)

#Tratar velocidade_max_via
#Define 0 para None
#Remover o Km/h da coluna velocidade_max_via
df['velocidade_max_via'].replace({'km/h':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'KM/H':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'km':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'KM':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'N/I':0},regex=True,inplace=True)
df['velocidade_max_via'].replace({'n/i':0},regex=True,inplace=True)
df['velocidade_max_via'].replace({'/h':''},regex=True,inplace=True)
df['velocidade_max_via'].replace({'30 e 40':40},regex=True,inplace=True)
df['velocidade_max_via'].replace({'':0},regex=True,inplace=True)
df['velocidade_max_via'] = df['velocidade_max_via'].fillna(0) # substitui o vazio por 0
df['velocidade_max_via'] = df['velocidade_max_via'].astype('int64') # Converte para inteiro

#Tratar mao_direcao
#Define 0 para None
df['mao_direcao'] = df['mao_direcao'].fillna(0)

#Tratar divisao_via1
#Define 0 para None
df['divisao_via1'] = df['divisao_via1'].fillna(0)


#Tratar divisao_via2
#Define 0 para None
df['divisao_via2'] = df['divisao_via2'].fillna(0)

#Tratar divisao_via3
#Define 0 para None
df['divisao_via3'] = df['divisao_via3'].fillna(0)

#display(df['velocidade_max_via'].unique())
#display(df)
#df.to_csv('C:/Users/igory/Documents/4_periodo_UFRPE/Projeto_3/datasets/dados_tratados/DataSetAcidentesRecifeTratado.csv')
#df.to_parquet('DataSetAcidentesRecifeTratado.parquet')
#display(df.dtypes)
#coluna = df['natureza_acidente'].unique()
#display(coluna)

######################## Conversão de variáveis categóricas em numéricas ##########################

# natureza_acidente
df['natureza_acidente'] = df['natureza_acidente'].replace(['APOIO', 'CHOQUE', 'COM VÍTIMA', 'ENTRADA E SAÍDA', 'OUTROS', 'SEM VÍTIMA', 'VÍTIMA FATAL'], [1, 2, 3, 4, 5, 6, 7])

# situacao
df['situacao'] = df['situacao'].replace(['CANCELADA', 'CRUZAMENTO COM A AV NORTE', 'DUPLICIDADE', 'EM ABERTO', 'EM ATENDIMENTO', 'EQUIPE EM DESLOCAMENTO', 'EQUIPE NO LOCAL', 'EVADIU-SE', 'FINALIZADA', 'PENDENTE']
, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# tipo
df['tipo'] = df['tipo'].replace(['ABALROAMENTO LONGITUDINAL', 'ABALROAMENTO TRANSVERSAL', 'ACID. DE PERCURSO', 'ALAGAMENTO', 'ATROPELAMENTO', 'ATROPELAMENTO DE ANIMAL', 'CAPOTAMENTO', 'CHOQUE', 'CHOQUE OBJETO FIXO', 'CHOQUE VEÍCULO PARADO', 'COLISÃO', 'COLISÃO COM CICLISTA', 'COLISÃO FRONTAL', 'COLISÃO LATERAL', 'COLISÃO TRANSVERSAL', 'COLISÃO TRASEIRA', 'ENGAVETAMENTO', 'NATUREZA', 'OUTROS', 'QUEDA', 'QUEDA DE ÁRVORE', 'TOMBAMENTO'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

# tempo_clima
df['tempo_clima'] = df['tempo_clima'].replace(['Bom', 'Chuvoso', 'Nublado'],[1, 2, 3])

# sinalizacao
df['sinalizacao'] = df['sinalizacao'].replace(['Ilegível', 'Incompleta', 'Não existente', 'Perfeito estado'], [1, 2, 3, 4])

# condicao_via
df['condicao_via'] = df['condicao_via'].replace(['Molhada', 'Oleosa', 'Outros', 'Seca'], [1, 2, 3, 4])

# conservacao_via
df['conservacao_via'] = df['conservacao_via'].replace(['Mal conservada', 'Mal iluminada', 'Não há', 'Outros', 'Perfeito estado'], [1, 2, 3, 4, 5])

# mao_direcao
df['mao_direcao'] = df['mao_direcao'].replace(['Dupla', 'Inglesa', 'Única'], [1, 2, 3])

# divisao_via1
df['divisao_via1'] = df['divisao_via1'].replace(['Blocos', 'Canal', 'Canteiro central', 'Faixa', 'Faixa contínua', 'Faixa seccionada', 'Não existe', 'Outros'], [1, 2, 3, 4, 5, 6, 7, 8])

# divisao_via2
df['divisao_via2'] = df['divisao_via2'].replace(['Blocos', 'Canal', 'Canteiro central', 'Faixa contínua', 'Faixa seccionada', 'Não existe', 'Outros'], [1, 2, 3, 4, 5, 6, 7])

# divisao_via3
df['divisao_via3'] = df['divisao_via3'].replace(['Blocos', 'Canal', 'Canteiro central', 'Faixa contínua', 'Não existe'], [1, 2, 3, 4, 5])