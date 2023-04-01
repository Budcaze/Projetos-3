import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sklearn.preprocessing import scale

%matplotlib inline

df = pd.read_parquet("data/DataSetAcidentesRecife.parquet")

df['vitimas'] = df['vitimas'].fillna(0)
df['vitimasfatais'] = df['vitimasfatais'].fillna(0)

#Elbow Method (técnica do cotovelo)
k_rng = range(1,10)
sse = []
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df[['vitimas','vitimasfatais']])
    sse.append(km.inertia_)
plt.xlabel('K')
plt.ylabel('SSE (Sum Squared Error)')
plt.plot(k_rng, sse)  #exibir o gráfico

plt.scatter(df['vitimas'],df['vitimasfatais'])  #analisar as duas variaveis (descartavel)

#Colocar os dados em scala
df['vitimasfatais'] = scale(df.vitimasfatais)
df['vitimas'] = scale(df.vitimas)

#Criar uma nova coluna 'ypred' para o treinamento
km = KMeans(n_clusters=3)
y_predict = km.fit_predict(df[['vitimas','vitimasfatais']])
df['ypred'] = y_predict
#df.head()

#Plotar o gráfico com a separação por cores
cores = np.array(['green', 'red', 'blue'])
plt.scatter(x=df['vitimas'],
            y=df['vitimasfatais'],
            c=cores[df.ypred], s=50)