import pandas as pd
import numpy as np


def cadastro_cvm():
  url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
  data = pd.read_csv(url, sep=';', encoding='ISO-8859-1')
  print(f'- Download do Cadastro CVM finalizado. {len(data)} Registros')
  return data

def informes_cvm(ano, mes):
    #print(f'Baixando dados de {mes}/{ano}')
    base_url = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{}.zip'
    url = base_url.format(ano + mes)
    return pd.read_csv(url, sep=';')

def calculate_daily_rentability(series):
    first_value = series.iloc[0]
    rentability = (series / first_value - 1) * 100
    return rentability

def process_cvm(df):
   df = df[['DT_COMPTC','CNPJ_FUNDO','VL_QUOTA']]
   df = df.pivot(index='DT_COMPTC', columns='CNPJ_FUNDO', values='VL_QUOTA')
   df.reset_index(inplace=True)
   df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])
   print(df['28.747.733/0001-03'])
   df.fillna(method='ffill', inplace=True)
   df.fillna(method='bfill', inplace=True)
   df.set_index('DT_COMPTC', inplace=True)  # Definindo 'DT_COMPTC' como o índice
   df = df.loc['2022-09-05':]
   df = df.apply(calculate_daily_rentability)
   print(df['28.747.733/0001-03'])
   

  
  

  