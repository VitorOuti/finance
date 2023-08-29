import pandas as pd
import numpy as np

def cadastro_cvm():
  url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
  return pd.read_csv(url, sep=';', encoding='ISO-8859-1')

def informes_cvm(ano, mes):
    #print(f'Baixando dados de {mes}/{ano}')
    base_url = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{}.zip'
    url = base_url.format(ano + mes)
    return pd.read_csv(url, sep=';')

def processar_cvm(informes):
   # Informes
   df = informes.pivot(index='DT_COMPTC', 
                columns='CNPJ_FUNDO', 
                values=['VL_TOTAL', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'CAPTC_DIA', 'RESG_DIA'])
   # Informes Normalizados
   df = df['VL_QUOTA'] / df['VL_QUOTA'].iloc[0] -1
   df.index.name = 'Data'

   return df
   