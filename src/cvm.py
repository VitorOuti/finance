import pandas as pd
import numpy as np


def cadastro_cvm():
  url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
  data = pd.read_csv(url, sep=';', encoding='ISO-8859-1')
  data = data.rename(columns={"CNPJ_FUNDO": "CNPJ"})
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

def format_number_with_dots(s):
    if not isinstance(s, str):
        s = str(s)
    if '.' in s:
        whole, decimal = s.split('.')
        whole = whole[::-1]  # Reverter a string para facilitar a adição dos pontos
        whole = '.'.join([whole[i:i+3] for i in range(0, len(whole), 3)])
        return whole[::-1] + '.' + decimal  # Reverter a string de volta
    else:
        s = s[::-1]  # Reverter a string para facilitar a adição dos pontos
        s = '.'.join([s[i:i+3] for i in range(0, len(s), 3)])
        return s[::-1]  # Reverter a string de volta

def pad_decimal_places(s):
    s = str(s)
    if '.' in s:
        whole, decimal = s.split('.')
        decimal = decimal.ljust(3, '0')
        return f"{whole}.{decimal}"
    else:
        return f"{s}.000"

def process_cvm(df): 
  
   df = df[df['NR_COTST'] >= 100]
   df = df[['DT_COMPTC','CNPJ_FUNDO','VL_QUOTA']]
   df = df.pivot(index='DT_COMPTC', columns='CNPJ_FUNDO', values='VL_QUOTA')
   df.reset_index(inplace=True)
   df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])
   df.fillna(method='ffill', inplace=True)
   df.fillna(method='bfill', inplace=True)
   df.set_index('DT_COMPTC', inplace=True)  
   df  = df.loc['2022-09-05':]
   df = df.apply(calculate_daily_rentability)
   df.reset_index(inplace=True)
   df = pd.melt(df, id_vars=['DT_COMPTC'], var_name='CNPJ', value_name='Retorno')
   df = df.rename(columns={"DT_COMPTC": "Data"})
   df['Retorno'] = round(df['Retorno'],2)
   return df
 
   

  
  

  