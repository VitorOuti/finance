import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analise_cdi(inf, cdi):
    print('- ajustando dados')

    # Renomear coluna e atualizar o DataFrame no lugar
    inf.rename(columns={'DT_COMPTC':'Data'}, inplace=True)
    inf['Data'] = pd.to_datetime(inf['Data'])
    inf['Data'] = inf['Data'].dt.strftime('%d/%m/%Y')

    # Ajustando tipo de dado
    cdi['CDI'] = cdi['CDI'].astype(float)

    # Ajustando a coluna de data:
    inf['Data'] = pd.to_datetime(inf['Data'], format='%d/%m/%Y')
    cdi['Data'] = pd.to_datetime(cdi['Data'], format='%d/%m/%Y')

    # Ordenando os DataFrames por Data
    inf = inf.sort_values('Data')
    cdi = cdi.sort_values('Data')

    # Pivotando e normalizando os dados
    fundo = inf[inf['NR_COTST'] >= 100].pivot(index='Data', columns='CNPJ_FUNDO', values=['VL_QUOTA'])
    fundo = (fundo['VL_QUOTA'] / fundo['VL_QUOTA'].iloc[0] -1) * 100
    fundo = pd.merge(fundo,cdi,on='Data',how='left')
    fundo['acumulado_cdi'] = fundo['CDI'].cumsum()
  
    return fundo

def analise_retorno(df):
    df = df.pivot(index='Data', columns='CNPJ_FUNDO', values=['VL_QUOTA'])
    df = df.iloc[:-1]
    cnpjs_cols = [col for col in df.columns]

    # Calculando a rentabilidade para cada CNPJ no período
    retorno = (df[cnpjs_cols].iloc[-1] - df[cnpjs_cols].iloc[0]) / df[cnpjs_cols].iloc[0]

    return retorno
    
def acima_cdi(df):
    # Inicializando uma lista para armazenar os resultados
    resultado = []
    
    # Iterando pelas colunas do DataFrame, excluindo as colunas 'Data', 'CDI' e 'acumulado_cdi'
    for col in df.columns:
        if col not in ['Data', 'CDI', 'acumulado_cdi']:
            # Contando os dias em que o valor da coluna (CNPJ_FUNDO) é maior que o valor em 'acumulado_cdi'
            count = (df[col] > df['acumulado_cdi']).sum()
            resultado.append({'CNPJ_FUNDO': col, 'Dias_Acima_do_CDI': count})
            
    # Convertendo a lista de dicionários para um DataFrame
    resultado_df = pd.DataFrame(resultado)
    
    return resultado_df

def consolidar(df1,df2,cad):
    df2 = df2.reset_index()
    df2.columns = ['Categoria', 'CNPJ_FUNDO', 'Valor']
    
    merged = pd.merge(df1, df2[['CNPJ_FUNDO', 'Valor']], on='CNPJ_FUNDO', how='left')
    merged.replace([np.inf, -np.inf], np.nan, inplace=True)
    merged.dropna(inplace=True)
    merged_info = pd.merge(merged,cad,on='CNPJ_FUNDO',how='left')
    merged_info.fillna('-', inplace=True)

    

    print(merged_info.info())
    return merged_info
    