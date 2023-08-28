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
   df_norm = df['VL_QUOTA'] / df['VL_QUOTA'].iloc[0]
   
   return df_norm
   
def get_best(frame, cadastro):
    """
    Retorna os fundos com os melhores retornos no período.
    
    Parameters:
    - frame: DataFrame contendo os valores dos fundos.
    - cadastro: DataFrame contendo informações adicionais dos fundos.
    
    Returns:
    - final: DataFrame contendo os 5 fundos com os melhores retornos e suas informações correspondentes.
    """
    
    # Filtra as colunas relevantes do DataFrame cadastro.
    info = cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_CANCEL', 'CLASSE', 'VL_PATRIM_LIQ', 'DT_INI_EXERC', 'DT_FIM_EXERC']]
    
    # Calcula o retorno percentual dos fundos.
    df = pd.DataFrame()
    df['retorno(%)'] = round((frame.iloc[-1].sort_values(ascending=False)[:5] - 1) * 100, 2)
    
    # Substitui valores infinitos por NaN e depois remove essas linhas.
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    # Junta o DataFrame de retorno com o DataFrame de informações do cadastro.
    final = pd.merge(df, info, how='left', on='CNPJ_FUNDO')
    
    return final
   
