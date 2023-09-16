import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def associate(cdi,cvm,cad):
    cvm['Data'] = pd.to_datetime(cvm['Data'])
    cdi['Data'] = pd.to_datetime(cdi['Data'])

    df = pd.merge(cvm,cad,on='CNPJ',how='left')
    df = df[['Data','DENOM_SOCIAL','Retorno']]
    df = pd.merge(df,cdi,on='Data',how='left').dropna()
    df = df.drop(columns=['CDI'])

    # Use os índices para obter as linhas correspondentes do DataFrame
    result = df.loc[df.groupby('DENOM_SOCIAL')['Data'].idxmax()].sort_values(by='Retorno', ascending=False)
    result = result[['DENOM_SOCIAL','Retorno']]
    print(result)
   

    df['dias acima cdi'] = df['Retorno'] > df['cdi_acumulado']
    df = df.groupby('DENOM_SOCIAL')['dias acima cdi'].sum().reset_index()
    estabilidade = df.sort_values(by='dias acima cdi', ascending=False).reset_index(drop=True)
    print(estabilidade)

    df = pd.merge(estabilidade,result,on='DENOM_SOCIAL', how='left')
    print(df)
  
    plt.scatter(df['dias acima cdi'], df['Retorno'])

    plt.xlabel('Dias acima CDI')
    plt.ylabel('Retorno')
    plt.title('Scatter Plot de Dias acima CDI vs Retorno')

    plt.grid(True)
    plt.show()